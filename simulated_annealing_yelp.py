# Note - this is written in python 3

import json
import operator
import random
import math

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
#print(data[0])

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

belmont_businesses = [business for business in data if business['city'] == 'Belmont']
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
N = 51

# Itinerary (number of meals) limit
M = 7

# List of eligible restaurants
items = belmont_rests
#print(len(items))

# Values for restaurants - in terms of star rating
stars = [x['stars'] for x in items]
#print(len(stars))

def strip_categories(categories):
	# Converts a 'Categories' string into a list of categories
	return [x.strip() for x in categories.split(',')]

def count_categories(businesses):
	# Converts a list of business items into a dictionary of categories
	# Does not include count for 'Restaurants'
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
	# Takes in a dictionary of categories and returns True if unique, else False
	# This is low-key hard. maybe constraint should be more than twice
	#return all(value == 1 for value in list(categories.values()))
	return all(value == 1 for value in list(categories.values()))

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

def neighbor_bag(bag):
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
	# try to pick an index at random and add to bag
	rand_index = random.randint(0, N - 1)
	rand_biz_ID = items[rand_index]['business_id']
	# Ensure the same business is not picked twice
	while rand_biz_ID in curr_biz_IDs:
	    rand_index = random.randint(0, N - 1)
	    rand_biz_ID = items[rand_index]['business_id']

	curr_bag.append(items[rand_index])
	curr_cats = count_categories(curr_bag)

	# Ensure that we have under M items and that genres are satisfied
	while len(curr_bag) > M or not unique_categories(curr_cats):
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
		#	if random.random() < math.exp((new_avg - old_avg) / T):
				#print ("accept bag - low star avg")
		#		return True
	#print ("not accept bag")
	return False

def simulated_annealing():
	"""
	Simulated Annealing Algorithm

	Return list of itinerary values while annealing and final bag: (vals, bag)
	"""
	TRIALS = 100
	T = 1000.0
	DECAY = 0.98

	vals = []
	sim_val = 0
	sim_bag = []

	for trial in range(TRIALS):

	    # Pick a random neighbor
	    next_bag = neighbor_bag(sim_bag)
	    next_val = star_average(next_bag)

	    # Accept with some probability
	    if accept_bag(next_bag, sim_bag, T):
	        sim_val = next_val
	        sim_bag = next_bag

	    # Update temperature
	    T *= DECAY

	    # Update vals
	    vals.append(sim_val)

	return vals, sim_bag

vals, sim_bag = simulated_annealing()
print("vals", vals)
print("sim_bag", sim_bag)
print("DONE")
