import tarfile
import zipfile
import json
import copy
import random
import math

#WRITTEN IN PYTHON 2

# CHANGE DIRECTORY HERE
#filepath = '/Users/jojoadler/Desktop/yelp_academic_dataset_business.json'
filepath = '/Users/amydanoff/Desktop/yelp_dataset/yelp_dataset/yelp_academic_dataset_business.json'

"""****************************************************************************************
	CODE FOR DATA CLEANING
   ****************************************************************************************"""

def open_data(filepath):
	"""
	Function that returns formatted data
	"""
	data = []
	with open(filepath) as f:
	    data = f.readlines()
	    data = list(map(json.loads, data)) 
	return data

# List of all businesses in dataset
data = open_data(filepath)

#Will contain a list of dictionaries for restaurants only
restaurant_data = []

# sorts through data and extracts only those with category 'restaurants'
for restaurant in data[0:len(data)]:
	if restaurant['categories'] != None:
		# turns unicode into strings
		cats = ''.join([cat.encode('UTF8') for cat in restaurant['categories']])
		catswords = cats.split(', ')
		if 'Restaurants' in catswords:
			restaurant_data.append(restaurant)

def test_maker((loc, reviewweight, starweight, num_meals, constraints)):
	import time
	start = time.time()
	def city_businesses(city): return [business for business in data if business['city'] == city]

	# create states
	states = {}
	# each state will be a tuple defined by the day and the meal (1,2) = sedond day dinner (indexed at 0)
	for day in range(num_meals/3):
		for meal in range(3):
			states[(day,meal)] = None

	# neighboring states
	neighbors = dict.fromkeys(copy.deepcopy(states), [])
	for state in states:
		day, meal = state
		for i in range(1,3):
			if meal - i >= 0:
				neighbors[state].append((day, meal - i))
			if meal + i <= 2:
				neighbors[state].append((day, meal + i))

	state_domains = dict.fromkeys(copy.deepcopy(states), city_businesses(loc))

	def strip_categories(categories):
		"""
		Converts a 'Categories' string into a list of categories
		"""
		categorieslist = []
		for category in categories:
			# turns unicode into strings
			cats = (''.join(''.join([cat.encode('UTF8') for cat in category]))).split(', ')
			categorieslist.append(catswords)
		return categorieslist[1]

	def has_category(business, category):
		"""
		Takes in a business object and a category, returns True if the business has that category
		and False otherwise
		"""
		categories = set()
		if business['categories']:
			categories = set(strip_categories(business['categories']))
		if category in categories:
			return True 
		return False

	def count_categories(businesses):
		"""
		Converts a list of business items into a dictionary of categories
		Does not include count for 'Restaurants'
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
		Takes in a dictionary of categories and returns True if unique, else False
		"""
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


	"""****************************************************************************************
		CODE FOR AC-3
	   ****************************************************************************************"""
	def constraint_generator(states):
		"""
			Creates a dictionary of each arc and True is the constraint 
			that two states cannot be equal is satisfied, False otherwise
		"""	
		constraints = {}
		states_not_checked1 = copy.deepcopy(states)
		for state1 in states:
			del states_not_checked1[state1]
			for state2 in states_not_checked1:
				constraints[(state1,state2)] = (states[state1] != states[state2])
		return constraints

	def check_sol (statess, bigX, littleX, bigY, littleY):
		"""
			Will return True is any two hypothetical states satisfy constraints,
			returns False otherwise
		"""
		checkstates = copy.deepcopy(statess)
		checkstates[bigX] = littleX
		checkstates[bigY] = littleY
		returnval = constraint_generator(checkstates).get((bigX,bigY), False)
		return returnval

	def runAC3 (stts, domain, neighbs, queue = None):
		def constraint (x, y): return (x != y)
		def arcs (stts, neighbors): return [(statei, statek) for statei in stts for statek in neighbors[statei]]
		def AC3 (stts, domain, neighbs, queue = None):
			if queue == None:
				queue = arcs(stts, neighbs)
			while queue:
				(statei, statej) = queue.pop()
				if remove_arcs(stts, domain, neighbs, statei, statej):
					"""if len(domain[statei]) == 0:
						return False"""
					for statek in neighbs[statei]:
						queue.append((statek, statei))

		def remove_arcs(stts, domain, neighbs, statei, statej):
			"""
				For each value in the domain of statei, remove any state from the domain of 
				state i that conflicts with the constraints for every value in the domain of 
				state j
			"""
			gone = False
			for restaurantx in domain[statei]:
				arc_checker = (map(lambda restauranty: not check_sol(states, statei, restaurantx, statej, restauranty), domain[statej]))
				if arc_checker == [False for x in range(len(arc_checker))]:
					domain[statei].remove(restaurantx)
					gone = True
			return gone

	runAC3(states, state_domains, neighbors)

	"""****************************************************************************************
		CODE FOR BACKTRACKING WITH FORWARD CHECK
	   ****************************************************************************************"""
	unassigned = copy.deepcopy(states.keys())
	curr_domains = copy.deepcopy(state_domains)
	curr_deleted = {}
	for state in states:
		curr_deleted[state] = []

	#MAKE THESE USER INPUT SOMEHOW
	star_weight = starweight
	reviews_weight = reviewweight

	def stardomain(var, curr_domains):
		"""
			Sorts the domains in terms of the user's input weightings
		"""
		if curr_domains:
			stardomain = sorted(curr_domains[state], key = lambda restaurant: (star_weight*math.log10(restaurant['stars']) + reviews_weight*math.log10(restaurant['review_count']))/(star_weight + reviews_weight))
			stardomain.reverse()
		else:
			stardomain = sorted(state_domains[state], key = lambda restaurant: (star_weight*math.log10(restaurant['stars']) + reviews_weight*math.log10(restaurant['review_count']))/(star_weight + reviews_weight))
			stardomain.reverse()
		return stardomain

	def backtrack(states, domains, neighbors, user_dict):
		"""
			CSP Backtrack
		"""
		counter = 0
		curr_domains = copy.deepcopy(domains)
		for meal in states:
			curr_deleted[meal] = []
		return recurse({}, states, domains, neighbors, user_dict)

	#Sets global, mutable var for recurse function
	varr = [None]
	def recurse(assignment, states, domains, neighbors, user_dict):
		"""
			Recursive part of backtracking call.
		"""
		if len(unassigned) == 0:
			return assignment

		varr[0] = randomchooseanddelete()

		for val in stardomain(varr[0], curr_domains):
			assignment[varr[0]] = val
			forwardcheck(varr[0], val, assignment, user_dict)
			nextstep = recurse(assignment, states, domains, neighbors, user_dict)
			if nextstep != None:
				return nextstep
		return None

	def forwardcheck(var, val, assignment, user_dict):
		"""
			Forward check heuristic to make domains of other variables consistent with
			the one that has been most recently set
		"""
		if curr_domains:
			for (meal, restaurant) in curr_deleted[var]:
				curr_domains[meal].append(restaurant)
			curr_deleted[var] = []

			for meal in neighbors[var]:
				if meal not in assignment:
					for restaurant in curr_domains[meal][:]:
						num_cats = count_categories(assignment.values())
						if not constraints_match(num_cats, user_dict):
						#if not user_solution_checker(user_dict, meal, restaurant, assignment):
							curr_domains[meal].remove(restaurant)
							curr_deleted[var].append((meal, restaurant))

	def randomchooseanddelete():
		"""
			Will randomly choose the next variable to assigne and remove it from the 
			unassigned list
		"""
		var = random.choice(unassigned)
		unassigned.remove(var)
		return var

	def fitness (assignment):
		def func(avgs, avgr) : return (star_weight*math.log10(avgs) + reviews_weight*math.log10(avgr))/(star_weight + reviews_weight)
		avgstar = 0
		avgreview = 0
		for restaurant in assignment.values():
			l = len(assignment.values())
			avgstar += restaurant['stars']/l
			avgreview += restaurant['review_count']/l
		avgfit = func(avgstar, avgreview)
		return avgfit
	
	solution = backtrack(states, state_domains, neighbors, constraints)
	total_fitness = fitness(solution)
	time = time.time() - start

	return (total_fitness , time)

# Filter down to restaurants in Phoenix
city1a = 'Phoenix'
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals1a = 6
constraints1a = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights1a = {'reviews': 2, 'stars': 5}
test_case1a = (city1a, weights1a['reviews'], weights1a['stars'], num_meals1a, constraints1a)

test_maker(test_case1a)
