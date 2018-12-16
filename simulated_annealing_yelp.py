# Note - this is written in python 3
import json
import operator
import random
import math
import time

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

"""
# get a list of all the different cities
cities = {}
for business in data:
	city = business['city']
	if city in cities:
		cities[city] += 1
	else:
		cities[city] = 1
sorted_cities = sorted(cities.items(), key=lambda kv: kv[1])
#print(len(cities))
#print(cities)
#print(len(sorted_cities)) # 1111
#print("sorted_cities", sorted_cities) # Cities w/ the most are: Las Vegas, Phoenix, Toronto, Charlotte
# A city with ~200 entries is  'Belmont' (158 entries)
"""

belmont_businesses = [business for business in data if business['city'] == 'Phoenix']
#print(len(belmont_rests))
#print(belmont_rests)
#for rest in belmont_rests:
	#print(rest['categories'])

# Find all categories in belmont restaurants
	# we are ONLY interested in businesses that have the "restaurant" tag. 
	# This cuts down our options further
belmont_cats = {}
cats_split = []
belmont_rests = []
for rest in belmont_businesses:
	if rest['categories']:
		cats_split = [x.strip() for x in rest['categories'].split(',')]
	if 'Restaurants' in cats_split:
		belmont_rests.append(rest)
		for cat in cats_split:
			if cat in belmont_cats:
				belmont_cats[cat] += 1
			else:
				belmont_cats[cat] = 1
#print(belmont_cats)
# Note - for Belmont, filtering by restaurants cuts our list down to 51 businesses

# try a small simulated annealing problem w the following constraints:
# 3 meals
# food category - must all be different - note that to format categories, we split by comma
# rating is impt
#print(belmont_rests[0])
cats_split = [x.strip() for x in belmont_rests[0]['categories'].split(',')]
#print('categories belmont:', cats_split)

# SIMULATED ANNEALING PROBLEM IS HERE VVV

# number of items
N = len(belmont_rests)

# Itinerary (number of meals) limit
M = 7

# List of eligible restaurants
items = belmont_rests
#print(len(items))

# Values for restaurants - in terms of star rating
#stars = [x['stars'] for x in items]
#print(len(stars))

def strip_categories(categories):
	# Converts a 'Categories' string into a list of categories
	return [x.strip() for x in categories.split(',')]

def has_category(business, category):
	# Takes in a business object and a category, returns True if the business has that category
	# and False otherwise
	categories = set()
	if business['categories']:
		categories = set(strip_categories(business['categories']))
	if category in categories:
		return True 
	return False

def count_categories(businesses):
	# Converts a list of business items into a dictionary of categories
	# Does not include count for 'Restaurants'
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
	# Takes in a dictionary of categories and returns True if unique, else False
	# This is low-key hard. maybe constraint should be more than twice
	#return all(value == 1 for value in list(categories.values()))
	return all(value < 3 for value in list(categories.values()))

def constraints_match(categories, constraints):
	"""
	Takes in a dictionary of category counts and a dictionary specifying the constraints, which are given as MAXIMUMS
	and returns True if the constraints are satisfied, and False otherwise.
	Any category that is not specified in the constraints dictionary can have any value.
	Additionally, there is a category called 'Unique', whereby the user can specify that they want all unique categories.
	"""

	# Else, iterate through categories and ensure maximums are satisfied
	for category, val in constraints.items():
		if category != 'Unique':
			# If category maximum is exceeded, return False
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
	return True

def star_average(businesses):
	# Returns average star rating for all businesses in a list
	star_sum = 0
	star_avg = 0
	for business in businesses:
		star_sum += float(business['stars'])
	if len(businesses) > 0:
		star_avg = star_sum / float(len(businesses))
	length = len(businesses)
	#print("business length,", length) 
	#print(businesses)
	#print ("star_avg", star_avg)
	return star_avg

def neighbor_bag(bag, constraints):
	curr_bag = bag.copy()
	#curr_len = len(bag) # never exceed M items
	curr_cats = count_categories(bag) #count_categories(list(bag.values()))
	# Initialize indices that have not yet been picked
	#print(curr_cats)
	curr_biz_IDs = [x['business_id'] for x in bag]
	"""
	Return a "neighbor" of the current bag.

	In generating the neighbor bag, we maintain a feasible set of items such that
	constraints are checked before the accept_bag function. Specifically,
	in generating a neighbor bag:
	 -We never exceed M items
	 -We never have restaurants from the same 'genre'
	 -We never have the same restaurant twice
	 #-We must always have one 'Fast Food' restaurant
	 ~~~~~~ ask monica about how to satisfy multiple constraints in simulated annealing?

	bags
	Algorithm:
	-Select an item from the unchosen items at random (check against business ID)
	-If it violates any constaints, delete from the bag at random amongst violated items until constraints are satisfied
	"""
	# Filter items if any constraints are set to 0
	start = time.time()
	blocked_cats = [category for (category, val) in constraints.items() if val == 0]
	filtered_items = items
	for category in blocked_cats:
		for item in filtered_items:
			if has_category(item, category):
				filtered_items.remove(item)
	end = time.time()
	print("filter time:",(end - start))

	# try to pick an index at random from remaining items and add to bag
	rand_index = random.randint(0, len(filtered_items) - 1)
	rand_biz_ID = filtered_items[rand_index]['business_id']
	# Ensure the same business is not picked twice
	while rand_biz_ID in curr_biz_IDs:
	    rand_index = random.randint(0, len(filtered_items) - 1)
	    rand_biz_ID = filtered_items[rand_index]['business_id']

	curr_bag.append(filtered_items[rand_index])
	curr_cats = count_categories(curr_bag)

	# Ensure that we have under M items and that genres are satisfied
	while len(curr_bag) > M or not constraints_match(curr_cats, constraints):
		#print("pick again")
		# pick a business at random from bag
		rand_new_index = random.randint(0, len(curr_bag) - 1)
		rand_biz = curr_bag[rand_new_index]
		# ensure that business picked is not the same as the one from before
		new_biz_ID = rand_biz['business_id']
		if new_biz_ID != rand_biz_ID:
		    del curr_bag[rand_new_index]
		curr_cats = count_categories(curr_bag)

	#print ("neighbor bag is same", curr_bag == old_bag)
	return curr_bag

#neighbor_bag(belmont_rests)

def accept_bag(new_bag, old_bag, T):
	# Always accept the bag if the length is longer (probability = 1)
	# accept with some probability if the length is the same, but the avg star rating is lower
	#print("IN ACCEPT BAG")
	#print("new bag", new_bag)
	#print("bags are same", new_bag == old_bag)
	#print("new bag length", len(new_bag))
	#print("new bag star avg", star_average(new_bag))
	#print("old bag", old_bag)
	#print("old bag length", len(old_bag))
	#print("old bag star avg", star_average(old_bag))

	if len(new_bag) > len(old_bag):
		#print ("Accept long bag")
		return True
	else:
		old_avg = star_average(old_bag)
		new_avg = star_average(new_bag)
		if new_avg > old_avg:
			#print ("accept bag - high star avg")
			return True
		#else:
			#if random.random() < math.exp((new_avg - old_avg) / T):
				#print ("accept bag - low star avg")
				#return True
	#print ("not accept bag")
	return False

def simulated_annealing(constraints):
	"""
	Simulated Annealing Algorithm

	Return list of itinerary values while annealing and final bag: (vals, bag)
	"""
	# Record start time
	start_time = time.time()

	TRIALS = 1000
	T = 1000.0
	DECAY = 0.98

	vals = []
	sim_val = 0
	sim_bag = []

	for trial in range(TRIALS):

	    # Pick a random neighbor
	    next_bag = neighbor_bag(sim_bag, constraints).copy()
	    next_val = star_average(next_bag)

	    # Accept with some probability
	    if accept_bag(next_bag, sim_bag, T):
	        sim_val = next_val
	        sim_bag = next_bag.copy()

	    # Update temperature
	    T *= DECAY

	    # Update vals
	    vals.append(sim_val)

	# Record end time
	end_time = time.time()
	run_time = (end_time - start_time)
	print("run_time", str(run_time))
	return vals, sim_bag, run_time


unique_constraints = {'Unique': True}
mexican_constraints = {'Unique': False, 'Mexican': 3}
no_mexican_constraints = {'Unique': True, 'Mexican': 0, 'Pizza': 0}
vals, sim_bag, run_time = simulated_annealing(no_mexican_constraints)
print("FINAL vals", vals)
print("sim_bag", sim_bag)
print("length sim bag", str(len(sim_bag)))
print("run_time", str(run_time))
print("DONE")