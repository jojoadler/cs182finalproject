# Written in python 3
import json
import random

"""
Constraints:
	-7 restaurants overall
	-cannot eat at the same genre restaurant more than 2 times
	-must all be in belmont
	-trying to find max stars
"""

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
	businesses_by_loc = [business for business in data if business['city'] == city]
	rests, cats_split = [], []
	for rest in businesses_by_loc:
		if rest['categories']:
			cats_split = [x.strip() for x in rest['categories'].split(',')]
		if 'Restaurants' in cats_split:
			rests.append(rest)
	return rests

def strip_categories(categories):
	# Converts a 'Categories' string into a list of categories
	cats = [x.strip() for x in categories.split(',')]
	cats.remove('Restaurants')
	return cats

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

# make greedy assignment
"""
def make_greedy(num_meals, maxtimes, data):
	curr_rests = [data[0]]
	while len(curr_rests) < num_meals:
		curr_cats = count_categories(curr_rests)
"""
def make_greedy(data, num_meals):
	return data[0:num_meals]

def star_average(businesses):
	# Returns average star rating for all businesses in a list
	star_sum = 0
	star_avg = 0
	for business in businesses:
		star_sum += float(business['stars'])
	if len(businesses) > 0:
		star_avg = star_sum / float(len(businesses))
	length = len(businesses)
	return star_avg

def check_csp(businesses, num_meals):
	categories = count_categories(businesses)
	if len(businesses) == num_meals and unique_categories(categories):
		return True
	return False

def min_conflicts(max_steps, curr_state, num_meals):
	for trial in range(max_steps):
		# If current assignment satisfies the CSP, then return assignment
		if check_csp(curr_state, num_meals):
			print("true")
			return curr_state
		else:
			# Find which vars have conflicts
			conflict_vars = []
			cat_counts = count_categories(curr_state)
			print("cat_counts", cat_counts)
			for business in curr_state:
				cats = strip_categories(business['categories'])
				for cat in cats:
					if cat_counts[cat] > 1 and business not in conflict_vars:
						conflict_vars.append(business)
			print("conflict_vars", conflict_vars)
			# Pick value at random from conflicted variables
			rand_index = 0
			if len(conflict_vars) > 1:
				rand_index = random.randint(0, len(conflict_vars) - 1)
			rand_var = conflict_vars[rand_index]
			# delete this variable from the current state
			curr_state.remove(rand_var)
			# update category count
			cat_counts = count_categories(curr_state)
			# Pick replacement with fewest conflicts w remaining vars
			# specifically, pick a replacement whose categories do not already exist in categories
			# Create list of all vars w min conflicts and pick one w highest rating greedily
			min_conflict_vars = []
			for item in belmont_rests:
				if item not in curr_state and item != rand_var:
					cats = strip_categories(item['categories'])
					not_unique = any([cat in cat_counts for cat in cats])
					if not not_unique:
						min_conflict_vars.append(item)
			# Greedily pick one with highest rating
			min_conflict_vars_sorted = sorted(min_conflict_vars, key=lambda d: float(d['stars']), reverse=True)
			curr_state.append(min_conflict_vars_sorted[0])


# Filter down to restaurants in Belmont
belmont_rests = filter_restaurants(data, 'Belmont')
print(len(belmont_rests))

# Make initial greedy assignment - first 7 meals
# M - number of meals in itinerary
num_meals = 7
TRIALS = 1000

curr_rests = make_greedy(belmont_rests, num_meals)
finalstate = min_conflicts(TRIALS, curr_rests, 7)
print("finalstate", finalstate)
staravg = star_average(finalstate)
print("star_average", staravg)