# Written in python 3
import json
import random
import time
import math
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


def make_greedy(data, num_meals, weights):
	"""
	Makes an initial "greedy" assignment of the data, based on the weights given by the user
	"""
	rev_weight, star_weight = weights['reviews'], weights['stars']
	total_weight = rev_weight + star_weight
	# Sort data by evaluation function, given weights
	data_sorted = sorted(data, key=lambda d: (rev_weight * math.log(float(d['review_count'])) + star_weight * math.log(float(d['stars'])))/float(total_weight), reverse=True)
	# Return greedy assignment of highest rated restaurants
	return data_sorted[0:num_meals]

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
						#print(categories[category], val)
						#print("exceeded max")
						return False
			else:
				if category in categories:
					#print("one when should be 0", category, categories[category])
					return False

	# If 'Unique' is specified, ensure categories are unique
	if constraints['Unique']:
		#print("unique_categories check", unique_categories(categories))
		return unique_categories(categories)
	# If all constraints are satisfied, return true
	return True


def min_conflicts(curr_state, num_meals, constraints, weights):
	"""
	Main min_conflicts algorithm.
	Takes in:
		curr_state - the starting (greedy allocation) state
		num_meals - the total number of desired meals in the itinerary
		constraints - a dictionary specifying the user-inputted constraints
		weights - a dictionary specifying the user-inputted weights
				  for the evaluation function
	Returns:
		A final csp solution, algorithm runtime
	"""
	# Start time
	start = time.time()

	# Define max number of trials
	max_steps = 1000

	# Define weights
	star_weight = weights['stars']
	rev_weight = weights['reviews']
	total_weight = star_weight + rev_weight

	for trial in range(max_steps):
		# If current assignment satisfies the CSP, then return this assignment as 'final state'
		curr_counts = count_categories(curr_state)
		if constraints_match(curr_counts, constraints):
			# Calculate final runtime
			end = time.time()
			run_time = end - start
			# Return satisfied CSP solution and runtime
			sat = True
			return curr_state, run_time, sat
		# If current assignment does not satisfy CSP, perform min-conflicts
		else:
			# Find which variables from current state have conflicts
			conflict_vars = []
			cat_counts = count_categories(curr_state)
			for business in curr_state:
				cats = strip_categories(business['categories'])
				for cat in cats:
					if constraints['Unique']:
						if cat_counts[cat] > 1 and business not in conflict_vars:
							conflict_vars.append(business)
					if cat in constraints:
						if cat_counts[cat] > constraints[cat] and business not in conflict_vars:
							conflict_vars.append(business)

			# Pick value at random from conflicted variables to remove
			rand_index = 0
			if len(conflict_vars) > 1:
				rand_index = random.randint(0, len(conflict_vars) - 1)
			rand_var = conflict_vars[rand_index]
			# Remove this conflicted variable from the current state
			curr_state.remove(rand_var)
			# Update category count of new state
			cat_counts = count_categories(curr_state)

			# Pick a replacement for deleted with fewest conflicts with remaining variables
			# Specifically, pick a replacement whose categories do not already exist in categories IF unique
			# OR whose categories are not in constraints
			# OR whose categories have highest count in constraints
			# Create list of all vars w min conflicts and pick one w highest rating greedily
			min_conflict_vars = []
			for item in rests:
				if item not in curr_state and item != rand_var:
					cats = strip_categories(item['categories'])
					# If 'Unique' is specified as a constraint, ensure uniqueness
					if constraints['Unique']:
						# Check if unique with any category in current counts
						not_unique = any([cat in cat_counts for cat in cats])
						# Check if blocked by any category in constraints
						blocked = False
						for cat in cats:
							if cat in constraints:
								if constraints[cat] == 0:
									blocked = True
						if not not_unique and not blocked:
							min_conflict_vars.append(item)
					# If not constrained by uniqueness, pick vars with highest maximum in constraints
					# or unconstrained entirely
					else:
						# Create list of categories 'limited' by constraints or existing variables
						constraints_ints = constraints.copy()
						del constraints_ints['Unique']
						limited_cats = [cat for (cat, val) in constraints_ints.items() if val == 0]
						more_lim_cats = [cat for (cat, val) in constraints_ints.items() if cat in cat_counts and cat_counts[cat] + 1 >= val]
						limited_cats += more_lim_cats

						# list of unconstrained businesses
						unconstrained_biz = all([cat not in limited_cats for cat in cats])
						if unconstrained_biz:
							min_conflict_vars.append(item)

			# If there are no min conflicted variables, return failure
			if len(min_conflict_vars) == 0:
				sat = False
				end = time.time()
				run_time = end - start
				return curr_state, run_time, sat
			# Greedily pick min-conflicted variable with highest rating, per evaluation function,
			# append to current state
			min_conflict_vars_sorted = sorted(min_conflict_vars, key=lambda d: (rev_weight * math.log(float(d['review_count'])) + star_weight * math.log(float(d['stars'])))/float(total_weight), reverse=True)
			curr_state.append(min_conflict_vars_sorted[0])
	# If we reach the end of our trials and we have not reached an acceptable solution, 
	# notify user that NO CSP solution was found, and return current state
	print("NO CSP SOL FOUND")
	end = time.time()
	run_time = end - start
	sat = False
	return curr_state, run_time, sat



"""
Testing

User inputs:
	City: str
	Constraints: dict
		{'Unique': bool, 'category': count, ... , 'category': count}
	Weights: dict
		{'reviews': 0-5, 'stars': 0-5}
	num_meals: integer
"""
def format_meals(output, weights, run_time):
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
THE BASIC BASE CASE FROM WHICH EACH TEST VARIES:
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
city1a = 'Phoenix'
rests = filter_restaurants(data, city1a)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('1a', city1a, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

"""
TEST CASE 1b
	"Basic"
	City: 'Belmont'
	Constraints: {'Unique': True}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city1b = 'Belmont'
rests = filter_restaurants(data, city1b)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('1b', city1b, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

"""
TEST CASE 1c
	"Basic"
	City: 'Parma'
	Constraints: {'Unique': True}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Concord
city1c = 'Concord'
rests = filter_restaurants(data, city1c)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('1c', city1c, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

"""Test Case Category 2 holds everything constant but the number of constraints"""
"""
TEST CASE 2a
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Belmont
city2a = 'Belmont'
rests = filter_restaurants(data, city2a)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': True, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('2a', city2a, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

"""
TEST CASE 2b
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city2a = 'Belmont'
rests = filter_restaurants(data, city2a)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': True, 'Mexican': 0, 'Pizza': 1, 'Chinese': 2}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('2b', city2a, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

"""
TEST CASE 2c
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city2c = 'Belmont'
rests = filter_restaurants(data, city2c)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': True, 'Mexican': 1, 'Pizza': 0, 'Chinese': 1, 'Bars': 1, 'Japanese': 2}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('2c', city2c, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

""" Test Case Category 3 is the same as Test Case Category 2 but with Unique = False"""

"""
TEST CASE 3a
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Belmont
city3a = 'Belmont'
rests = filter_restaurants(data, city3a)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('3a', city3a, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

"""
TEST CASE 3b
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city3b = 'Belmont'
rests = filter_restaurants(data, city3b)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 0, 'Pizza': 1, 'Chinese': 2}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('3b', city3b, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

"""
TEST CASE 2c
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city3c = 'Belmont'
rests = filter_restaurants(data, city3c)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 0, 'Chinese': 1, 'Bars': 1, 'Japanese': 2}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('3c', city3c, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

"""
TEST CASE 4a
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 0, 'stars': 5}
	num_meals: 6 
"""
city4a = 'Belmont'
rests = filter_restaurants(data, city4a)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 0, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('4a', city4a, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')


"""
TEST CASE 4b
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 3, 'stars': 3}
	num_meals: 6 
"""
city4b = 'Belmont'
rests = filter_restaurants(data, city4b)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 3, 'stars': 3}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('4b', city4b, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

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
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 6
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 5, 'stars': 0}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('4c', city4c, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

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
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 10
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('5a', city5a, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')


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
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 51
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 3, 'Sports Bars': 2, 'Japanese': 17}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('5b', city5b, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

"""
TEST CASE 5c
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 100
"""
city5b = 'Belmont'
rests = filter_restaurants(data, city5b)
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals = 30
constraints = {'Unique': False, 'Mexican': 1, 'Pizza': 1, 'Sports Bars': 5, 'Japanese': 10, 'Chinese': 6, 'Juice': 2, 'Pubs': 1, 'Indian': 9, 'Bagels': 3}
weights = {'reviews': 2, 'stars': 5}

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
val = rating_average(output, weights)

data_to_csv('5c', city5b, str(num_meals), str(run_time), str(val), str(sat), 'results_min_conflict.csv')

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

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)

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

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 2 OUTPUT:")
format_meals(output, weights, run_time)

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

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 3 OUTPUT:")
format_meals(output, weights, run_time)

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

# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time, sat = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 3 OUTPUT:")
format_meals(output, weights, run_time)