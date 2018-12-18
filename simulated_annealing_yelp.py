# Note - this is written in python 3
import json
import operator
import random
import math
import time
import csv

# Set up data
filepath = '/Users/amydanoff/Desktop/yelp_dataset/yelp_dataset/yelp_academic_dataset_business.json'

# Function that returns formatted data
def open_data(filepath):
	data = []
	with open(filepath) as f:
	    data = f.readlines()
	    data = list(map(json.loads, data)) 
	return data

# List of all businesses in dataset
data = open_data(filepath)

# Filter businesses down to restaurants in a certain location
def filter_restaurants(data, city):
	"""
	Takes in full yelp dataset and specified city,
	Returns a list of all the restaurants in that city
	"""
	businesses_by_loc = [business for business in data if business['city'] == city]
	rests, cats_split = [], []
	for rest in businesses_by_loc:
		if rest['categories']:
			cats_split = [x.strip() for x in rest['categories'].split(',')]
		if 'Restaurants' in cats_split:
			rests.append(rest)
	return rests

"""
Helper Functions
"""
def strip_categories(categories):
	"""
	Takes in a 'categories' formatted string (as from business['categories']),
	returns a list of categories from that string
	"""
	cats = []
	if categories:
		cats = [x.strip() for x in categories.split(',')]
		cats.remove('Restaurants')
	return cats

def has_category(business, category):
	"""
	Takes in a business object and a category
	Returns True if the business has that category, else False
	"""
	categories = set()
	if business['categories']:
		categories = set(strip_categories(business['categories']))
	if category in categories:
		return True 
	return False

def count_categories(businesses):
	"""
	Takes in a list of 'business' objects (i.e. Restaurants), and
	returns a dictionary of the categories in that list mapped to the
	count of times that category appears in the list
	N.B. - Does not include count for 'Restaurants' category
	"""
	categories = {}
	for business in businesses:
		cats_string = business['categories']
		cats_list = []
		if cats_string:
			cats_list = strip_categories(cats_string)
		for cat in cats_list:
			if cat != 'Restaurants':
				if cat in categories:
					categories[cat] += 1
				else:
					categories[cat] = 1
	return categories

def unique_categories(categories):
	"""
	Takes in a dictionary of category counts (as returned by count_categories).
	returns True if all categories are unique, else returns False
	"""
	return all(value == 1 for value in list(categories.values()))

def constraints_match(categories, constraints):
	"""
	Takes in a dictionary of category counts (categories) 
	and a dictionary specifying the constraints (constraints), 
	which are given as MAXIMUM counts for a certain category.
	
	Additionally, there is a category called 'Unique', 
	whereby the user can specify that they want all unique categories.

	Any category that is not specified in the constraints dictionary can have any value.

	Returns True if the constraints are satisfied, and False otherwise.
	"""
	# Iterate through constraints
	for category, val in constraints.items():
		if category != 'Unique':
			# If constraint maximum is exceeded in category counts, return False
			if val != 0:
				if category in categories:
					if categories[category] > val:
						return False
			else:
				if category in categories:
					return False

	# If 'Unique' is specified, ensure categories are unique
	if constraints['Unique']:
		return unique_categories(categories)
	# If all constraints are satisfied, return true
	return True

def star_average(businesses):
	"""
	Returns the average star rating for a list of businesses
	"""
	star_sum = 0
	star_avg = 0
	for business in businesses:
		star_sum += float(business['stars'])
	if len(businesses) > 0:
		star_avg = star_sum / float(len(businesses))
	length = len(businesses)
	return star_avg

def rating_average(businesses, weights):
	"""
	Given a list of businesses and user-inputted weights, 
	returns their average normalized 'rating' as defined by the evaluation function:
	rating = (review_weight * log(# of reviews)) * (star_weight * log(star rating)) / (total weight of inputs)
	"""
	rev_weight, star_weight = weights['reviews'], weights['stars']
	total_weight = rev_weight + star_weight
	rating_sum = sum([((rev_weight * math.log(float(business['review_count'])) + star_weight * math.log(float(business['stars'])))/float(total_weight)) for business in businesses])
	rating_avg = 0
	if len(businesses) > 0:
		rating_avg = rating_sum / float(len(businesses))
	return rating_avg

"""
Functions for simulated annealing
"""

def neighbor_state(curr_state, constraints):
	"""
	Takes in the current state (a list of restaurants) and constraints
	returns a random 'neighbor' state, such that constraints
	remain satisfied (we maintain a feasible set of items).
	Specifically, we never exceed the user specified max number of restaurants (num_meals),
	We ensure that 'Unique' and maximum category constraints are satisfied,
	and that a restaurant is never repeated.

	A neighbor state is defined as one where exactly 1 new random item (restaurant)
	is added to the state, and
	then items are deleted at random until that item 'fits' in the constraints.
	"""
	curr_bag = curr_state.copy()
	curr_cats = count_categories(curr_state) 
	# Initialize indices that have not yet been picked
	curr_biz_IDs = [x['business_id'] for x in curr_state]

	# Filter items to be picked from if any constraints are set to 0
	blocked_cats = [category for (category, val) in constraints.items() if val == 0]
	filtered_items = rests
	for category in blocked_cats:
		for item in filtered_items:
			if has_category(item, category):
				filtered_items.remove(item)

	# Pick an index at random from remaining (unfiltered) items and add to state
	rand_index = random.randint(0, len(filtered_items) - 1)
	rand_item = filtered_items[rand_index]
	# Ensure the same restaurant is not picked twice
	while rand_item in curr_bag:
	    rand_index = random.randint(0, len(filtered_items) - 1)
	    rand_item = filtered_items[rand_index]

	# Add randomly generated new item to bag
	curr_bag.append(filtered_items[rand_index])
	# Update category counts in new state
	curr_cats = count_categories(curr_bag)

	# Ensure that we have under the max number of items and that genres are satisfied
	# Delete items from bag at random until constraints are satisfied
	while len(curr_bag) > num_meals or not constraints_match(curr_cats, constraints):
		# Pick a business at random from bag
		rand_new_index = random.randint(0, len(curr_bag) - 1)
		new_rand_biz = curr_bag[rand_new_index]
		# Ensure that new business picked is not the same as the one that
		# was just added
		if new_rand_biz != rand_item:
		    del curr_bag[rand_new_index]
		curr_cats = count_categories(curr_bag)

	# Once no constraints are violated, return bag
	return curr_bag

def accept_state(new_state, old_state, T, weights):
	"""
	Given a potential new state, the old state, the current temperature T,
	and the weights given by the user, determine whether to accept the new
	bag.

	Specifically, if the rating function is higher for the new bag,
	or if the new bag is longer than the old bag,
	accept the new bag with probability 1.

	Otherwise, accept the new bag with probability
	1/e^(|100 - |new-old||/T), such that this probability
	decreases as T decreases, and increases as the old 
	rating is closer to the new rating.
	"""

	# Always accept the new state if the length is longer
	if len(new_state) > len(old_state):
		#print("accept long bag")
		return True

	else:
		# Get ratings of old and new bags
		old_rating = rating_average(old_state, weights)
		new_rating = rating_average(new_state, weights)
		
		# If the new rating is better, accept with prob = 1
		if new_rating > old_rating:
			return True
		# If the old rating is better, accept with prob
		# 1/e^(|100 - |new-old||/T)
		else:
			# Set acceptance probability
			d = abs(new_rating - old_rating) / (weights['reviews'] + weights['stars'])
			#print("d", d)
			p = 0
			if T != 0:
				p = 1 / (math.exp((abs(100-d) / T)))
			#print("p", p)
			# Accept 'worse' state with probability p
			if random.random() < p:
				return True

	# Else, do not accept bag
	return False

def simulated_annealing(constraints, weights):
	"""
	Simulated Annealing Algorithm

	Return list of itinerary values while annealing and final state and runtime: (vals, state, runtime)
	"""
	# Record start time
	start_time = time.time()

	TRIALS = 100
	T = 1000.0
	DECAY = 0.98

	vals = []
	sim_val = 0
	sim_state = []

	for trial in range(TRIALS):
	    # Pick a random neighbor and record its value
	    next_bag = neighbor_state(sim_state, constraints).copy()
	    next_val = rating_average(next_bag, weights)

	    # Accept neighbor with some probability
	    if accept_state(next_bag, sim_state, T, weights):
	        sim_val = next_val
	        sim_state = next_bag.copy()

	    # Update temperature
	    T *= DECAY

	    # Update vals
	    vals.append(sim_val)

	# Record end time
	end_time = time.time()
	run_time = (end_time - start_time)
	return vals, sim_state, run_time


"""
TESTING
"""
def format_meals(output, weights, run_time):
	"""
	Helper function for formatting testing
	"""
	length = len(output)
	star_avg = star_average(output)
	rating_avg = rating_average(output, weights)
	print("Length:", length)
	print("Star avg", star_avg)
	for meal_num in range(len(output)):
		print("Meal number", meal_num + 1)
		# Get important attributes from restaurant
		restaurant = output[meal_num]
		name = restaurant['name']
		categories = restaurant['categories']
		stars = restaurant['stars']
		review_count = restaurant['review_count']
		print("Name:", name)
		print("categories:", categories)
		print("stars:", stars)
		print("review_count:", review_count)
	print("Rating average,", rating_avg)
	print("run_time", run_time)
	print("\n")

def data_to_csv(testcase, city, num_meals, time, rating, sat, csvname):
	with open(csvname, 'a') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',',
                            	quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow([testcase, city, num_meals, time, rating, sat])
"""
TEST CASE 1
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 0, 'stars': 5}
	num_meals: 5
"""
# Filter down to restaurants in Phoenix
rests = filter_restaurants(data, 'Phoenix')
num_meals = 5
constraints = {'Unique': True}
weights = {'reviews': 0, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(sim_state, weights, run_time)

"""
TEST CASE 2
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 5
"""
# Filter down to restaurants in Phoenix
rests = filter_restaurants(data, 'Phoenix')
num_meals = 5
constraints = {'Unique': True, 'Mexican': 0, 'Pizza': 0}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
# Print output
print("TEST CASE 2 OUTPUT:")
format_meals(sim_state, weights, run_time)

"""
TEST CASE 3
	"Heavily constrained, non-unique, more weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': False, 'Mexican': 0, 'Pizza': 0, 'American (New)': 0, 'Japanese':0, 'Chinese': 1}
	Weights: {'reviews': 4, 'stars': 2}
	num_meals: 10
"""
# Filter down to restaurants in Phoenix
rests = filter_restaurants(data, 'Phoenix')
num_meals = 10
constraints = {'Unique': False, 'Mexican': 0, 'Pizza': 0, 'American (New)': 0, 'Japanese':0, 'Chinese': 1}
weights = {'reviews': 4, 'stars': 2}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
# Print output
print("TEST CASE 3 OUTPUT:")
format_meals(sim_state, weights, run_time)

"""
TEST CASE 4
	"Heavily constrained, small set, non-unique, equal weight"
	City: 'Parma'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0, 'American (New)': 0, 'Japanese':0, 'Chinese': 1}
	Weights: {'reviews': 3, 'stars': 3}
	num_meals: 8
"""
rests = filter_restaurants(data, 'Parma')
num_meals = 8
constraints = {'Unique': True, 'Mexican': 0, 'Pizza': 0, 'American (New)': 0, 'Japanese':0, 'Chinese': 1}
weights = {'reviews': 3, 'stars': 3}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
# Print output
print("TEST CASE 4 OUTPUT:")
format_meals(sim_state, weights, run_time)
print(vals[-1])

"""THE BASIC BASE CASE FROM WHICH EACH TEST VARIES:
City: 'Phoenix'
Constraints: {'Unique': False, 'Mexican': 1, 'Pizza': 1}
Weights: {'reviews': 2, 'stars': 5}
num_meals = 6 (days = 2)

Therefore, we will test for different cities, constraints length, uniqueness, weights, and num_meals"""

"""Test Case Category 1 holds everything constant but the location"""
"""
TEST CASE 1a
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6 
"""
# Filter down to restaurants in Phoenix
# Filter down to restaurants in Phoenix

city1a = 'Phoenix'
rests = filter_restaurants(data, city1a)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}
# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('1a', city1a, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 1b
	"Basic"
	City: 'Belmont'
	Constraints: {'Unique': True}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city1b = 'Belmont'
rests = filter_restaurants(data, city1b)
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}
# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('1b', city1b, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 1c
	"Basic"
	City: 'Concord'
	Constraints: {'Unique': True}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Concord
city1c = 'Concord'
rests = filter_restaurants(data, city1c)
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}
# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('1c', city1c, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""Test Case Category 2 holds everything constant but the number of constraints"""
"""
TEST CASE 2a
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city2a = 'Belmont'
rests = filter_restaurants(data, city2a)
num_meals = 6
constraints = {'Unique': True, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('2a', city2a, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 2b
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city2b = 'Belmont'
rests = filter_restaurants(data, city2b)
num_meals = 6
constraints = {'Unique': True, 'Mexican': 0, 'Pizza': 1, 'Chinese': 2}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('2b', city2b, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 2c
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Belmont
city2c = 'Belmont'
rests = filter_restaurants(data, city2c)
num_meals = 6
constraints = {'Unique': True, 'Mexican': 1, 'Pizza': 0, 'Chinese': 1, 'Bars': 1, 'Japanese': 2}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('2c', city2c, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

""" Test Case Category 3 is the same as Test Case Category 2 but with Unique = False"""
"""
TEST CASE 3a
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city3a = 'Belmont'
rests = filter_restaurants(data, city3a)
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('3a', city3a, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 3b
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city3b = 'Belmont'
rests = filter_restaurants(data, city3b)
num_meals = 6
constraints = {'Unique': False, 'Mexican': 0, 'Pizza': 1, 'Chinese': 2}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('3b', city3b, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 3c
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Belmont
city3c = 'Belmont'
rests = filter_restaurants(data, city3c)
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 0, 'Chinese': 1, 'Bars': 1, 'Japanese': 2}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('3c', city3c, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 4a
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 0, 'stars': 5}
	num_meals: 6 
"""
# Filter down to restaurants in Belmont
city4a = 'Belmont'
rests = filter_restaurants(data, city4a)
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('4a', city4a, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 4b
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 3, 'stars': 3}
	num_meals: 6 
"""
# Filter down to restaurants in Phoenix
city4b = 'Belmont'
rests = filter_restaurants(data, city4b)
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 3, 'stars': 3}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('4b', city4b, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 4c
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 5, 'stars': 0}
	num_meals: 6 
"""
city4c = 'Belmont'
rests = filter_restaurants(data, city4c)
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 5, 'stars': 0}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('4c', city4c, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 5a
	"Basic"
	City: 'Phoenix'
	Constraints: Few
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 10
"""
city5a = 'Belmont'
rests = filter_restaurants(data, city5a)
num_meals = 10
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('5a', city5a, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 5b
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 50
"""
city5b = 'Belmont'
rests = filter_restaurants(data, city5b)
num_meals = 51
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 3, 'Sports Bars': 2, 'Japanese': 17}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('5b', city5b, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')

"""
TEST CASE 5c
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 100
"""
city5c = 'Belmont'
rests = filter_restaurants(data, city5c)
num_meals = 99
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1, 'Sports Bars': 5, 'Japanese': 10, 'Chinese': 6, 'Juice': 2, 'Pubs': 1, 'Indian': 9, 'Bagels': 3}
weights = {'reviews': 2, 'stars': 5}

# Get output
vals, sim_state, run_time = simulated_annealing(constraints, weights)
sat = (num_meals == len(sim_state))

data_to_csv('5c', city5c, str(num_meals), str(run_time), str(vals[-1]), str(sat), 'sim_anneal.csv')