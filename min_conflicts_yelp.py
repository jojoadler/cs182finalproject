# Written in python 3
import json
import random
import time
import math


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
	cats = []
	if categories:
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
def make_greedy(data, num_meals, weights):
	"""
	Makes an initial "greedy" assignment of the data, based on the weights given by the user
	"""
	rev_weight, star_weight = weights['reviews'], weights['stars']
	total_weight = rev_weight + star_weight
	data_sorted = sorted(data, key=lambda d: (rev_weight * math.log(float(d['review_count'])) + star_weight * math.log(float(d['stars'])))/float(total_weight), reverse=True)
	#print("Data sorted", data_sorted)
	return data_sorted[0:num_meals]

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

def rating_average(businesses, weights):
	"""
	Given a list of businesses, returns their average 'rating' as defined by
	the evaluation function:
	rating = log(# of reviews) * star rating
	"""
	rev_weight, star_weight = weights['reviews'], weights['stars']
	total_weight = rev_weight + star_weight
	rating_sum = sum([((rev_weight * math.log(float(business['review_count'])) + star_weight * math.log(float(business['stars'])))/float(total_weight)) for business in businesses])
	rating_avg = 0
	if len(businesses) > 0:
		rating_avg = rating_sum / float(len(businesses))
	return rating_avg

def check_csp(businesses, num_meals):
	categories = count_categories(businesses)
	if len(businesses) == num_meals and unique_categories(categories):
		return True
	return False

def constraints_match(categories, constraints):
	"""
	Takes in a dictionary of category counts and a dictionary specifying the constraints, which are given as MAXIMUMS
	and returns True if the constraints are satisfied, and False otherwise.
	Any category that is not specified in the constraints dictionary can have any value.
	Additionally, there is a category called 'Unique', whereby the user can specify that they want all unique categories.
	"""

	# Else, iterate through categories and ensure maximums are satisfied
	for category, val in constraints.items():
		print("category, val", category, val)
		if category != 'Unique':
			# If category maximum is exceeded, return False
			if val != 0:
				if category in categories:
					if categories[category] > val:
						print(categories[category], val)
						print("exceeded max")
						return False
			else:
				if category in categories:
					print("one when should be 0", category, categories[category])
					return False

	# If 'Unique' is specified, ensure categories are unique
	if constraints['Unique']:
		print("unique_categories check", unique_categories(categories))
		return unique_categories(categories)
	print("constraints match")
	return True


def min_conflicts(max_steps, curr_state, num_meals, constraints, weights):
	star_weight = weights['stars']
	rev_weight = weights['reviews']
	total_weight = star_weight + rev_weight
	start = time.time()
	for trial in range(max_steps):
		# If current assignment satisfies the CSP, then return assignment
		#if check_csp(curr_state, num_meals):
		curr_counts = count_categories(curr_state)
		if constraints_match(curr_counts, constraints):
			#print("true")
			print("iteration num", trial)
			end = time.time()
			run_time = end - start
			return curr_state, run_time
		else:
			#print("blerrghhhhhh")
			# Find which vars have conflicts
			conflict_vars = []
			cat_counts = count_categories(curr_state)
			#print("cat_counts", cat_counts)
			for business in curr_state:
				cats = strip_categories(business['categories'])
				for cat in cats:
					if constraints['Unique']:
						if cat_counts[cat] > 1 and business not in conflict_vars:
							conflict_vars.append(business)
					if cat in constraints:
						if cat_counts[cat] > constraints[cat] and business not in conflict_vars:
							conflict_vars.append(business)
			print("conflict_vars", len(conflict_vars))
			# Pick value at random from conflicted variables
			rand_index = 0
			if len(conflict_vars) > 1:
				rand_index = random.randint(0, len(conflict_vars) - 1)
			rand_var = conflict_vars[rand_index]
			# delete this variable from the current state
			print("randvar", rand_var)
			curr_state.remove(rand_var)
			# update category count
			cat_counts = count_categories(curr_state)
			# Pick replacement with fewest conflicts w remaining vars
			# specifically, pick a replacement whose categories do not already exist in categories if unique
			# OR whose categories are not in constraints
			# OR whose categories have highest count in constraints
			# Create list of all vars w min conflicts and pick one w highest rating greedily
			min_conflict_vars = []
			for item in belmont_rests:
				if item not in curr_state and item != rand_var:
					cats = strip_categories(item['categories'])
					if constraints['Unique']:
						# Check if unique with any category in current counts
						not_unique = any([cat in cat_counts for cat in cats])
						# check if blocked by any category
						blocked = False
						for cat in cats:
							if cat in constraints:
								if constraints[cat] == 0:
									blocked = True
						if not not_unique and not blocked:
							min_conflict_vars.append(item)
					# If not constrained by uniqueness, pick vars with highest maximum in constraints
					# or unconstrained
					else:
						constraints_ints = constraints.copy()
						#print("constraints_ints.items()", constraints_ints.items())
						del constraints_ints['Unique']
						limited_cats = [cat for (cat, val) in constraints_ints.items() if val == 0]
						more_lim_cats = [cat for (cat, val) in constraints_ints.items() if cat in cat_counts and cat_counts[cat] + 1 >= val]
						#print("more_lim_cats", more_lim_cats)
						limited_cats += more_lim_cats
						#print("limited_cats", limited_cats)
						#print("nonlimited_cats", nonlimited_cats)
						unconstrained_biz = all([cat not in limited_cats for cat in cats])
						#print()
						if unconstrained_biz:
							min_conflict_vars.append(item)


			#print("min_conflict_vars", min_conflict_vars)
			# Greedily pick one with highest rating
			min_conflict_vars_sorted = sorted(min_conflict_vars, key=lambda d: (rev_weight * math.log(float(d['review_count'])) + star_weight * math.log(float(d['stars'])))/float(total_weight), reverse=True)
			print("min conflict vars", len(min_conflict_vars_sorted))
			curr_state.append(min_conflict_vars_sorted[0])
			print("OK?", constraints_match(count_categories(curr_state), constraints))
		# If we reach the end of our trials and we have not reached an acceptable solution, return current state
	print("NO CSP SOL FOUND")
	end = time.time()
	run_time = end - start
	return curr_state, run_time


# Filter down to restaurants in Belmont
belmont_rests = filter_restaurants(data, 'Phoenix')
#print(len(belmont_rests))

# Make initial greedy assignment - first 7 meals
# M - number of meals in itinerary
num_meals = 7
TRIALS = 1000

unique_constraints = {'Unique': True}
mexican_constraints = {'Unique': False, 'Mexican': 0, 'Pizza': 0, 'American (New)': 0, 'Japanese':0, 'Chinese': 1}
no_mexican_constraints = {'Unique': True, 'Mexican': 0, 'Pizza': 0}

weights = {'reviews': 4, 'stars': 2}

curr_rests = make_greedy(belmont_rests, num_meals, weights)
finalstate, run_time = min_conflicts(TRIALS, curr_rests, 7, no_mexican_constraints, weights)
#print("finalstate", finalstate)
staravg = star_average(finalstate)
rating_avg = rating_average(finalstate, weights)
print("star_average", staravg)
print("rating_average", rating_avg)
print("run_time", run_time)