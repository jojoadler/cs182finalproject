import tarfile
import zipfile
import json
import geopy.distance
import copy
import random
import math

# Track filepath - note that this will need to be changed
filepath = '/Users/jojoadler/Desktop/yelp_academic_dataset_business.json'
#filepath = '/Users/amydanoff/Desktop/yelp_dataset/yelp_dataset/yelp_academic_dataset_business.json'

# Function that returns formatted data
def open_data(filepath):
	data = []
	with open(filepath) as f:
	    data = f.readlines()
	    data = list(map(json.loads, data)) 
	return data

# List of all businesses in dataset
data = open_data(filepath)

# will contain a list of dictionaries for restaurants only
restaurant_data = []

# sorts through data and extracts only those with category 'restaurants'
for restaurant in data[0:len(data)]:
	if restaurant['categories'] != None:
		# turns unicode into strings
		cats = ''.join([cat.encode('UTF8') for cat in restaurant['categories']])
		catswords = cats.split(', ')
		if 'Restaurants' in catswords:
			restaurant_data.append(restaurant)

#inputs for a sample problem
user_inputs = {'days': [3], 'state': ['NC'], 'city': ['Belmont'], 'cuisines': [['Mexican', 1],['Italian', 2]], 'base_location': [(33.4484,-112.0740)], 'maxDist': [10]}
# constraints for the sample problem, for now this is hardcoded, but should be automatically constructed
constraints = [('Mexican', 'Italian'), ('Italian', 'Mexican')]

belmont_businesses = [business for business in data if business['city'] == 'Belmont']

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

# create states
states = {}
# each state will be a tuple defined by the day and the meal (1,2) = sedond day dinner (indexed at 0)
for day in range(user_inputs['days'][0]):
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


# all possible values, ie domain
possible_restaurants = []
# check for every restaurant
for restaurant in restaurant_data:
	# check for every restaurant in the location of the user
	for loc in ['state', 'city']:
		if restaurant[loc] == user_inputs[loc][0]:
			rest_to_base = geopy.distance.vincenty(user_inputs['base_location'][0], (restaurant['latitude'], restaurant['longitude']))
			if rest_to_base <= user_inputs['maxDist']:
				possible_restaurants.append(restaurant)

state_domains = dict.fromkeys(copy.deepcopy(states), possible_restaurants[:50])

def strip_categories(categories):
	# Converts a 'Categories' string into a list of categories
	#	THIS FUNCTION DOES NOT WORK
	categorieslist = []
	for category in categories:
		# turns unicode into strings
		cats = (''.join(''.join([cat.encode('UTF8') for cat in category]))).split(', ')
		#if 'Restaurants' in catswords:
		categorieslist.append(catswords)
	return categorieslist[1]

def category_list_maker(restaurants):
	# Makes a dict of each restaurant, the list of categories they have
	restaurant_categories = {}
	for restaurant in restaurants:
		restaurant_categories[(restaurant['business_id'])] = strip_categories(restaurant['categories'])
	return restaurant_categories

def category_counter(restaurants):
	categories = {}
	for restaurant in restaurants:
		for category in category_list_maker(restaurant)['business_id']:
			if categories.get(category, None) == None:
				categories[category] = 1
			else:
				categories[category] += 1
	return categories

def user_solution_checker(user_dict, bigX, littleX, assignment, unique = False):
	restaurant_categories = category_list_maker(assignment.values())
	checker = copy.deepcopy(assignment)
	if unique:
		for category in user_dict.keys():
			if category_counter(checker.values())[category] > 1:
				return False
	else:
		for category in user_dict.keys():
			if category_counter(checker.values())[category] > user_dict[category]:
				return False
	return True

#def strip_categories(categories):
	# Converts a 'Categories' string into a list of categories
	#return [x.strip() for x in categories.split(',')]

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


# creating arcs
def constraint_generator(states):
	constraints = {}
	states_not_checked1 = copy.deepcopy(states)
	for state1 in states:
		del states_not_checked1[state1]
		for state2 in states_not_checked1:
			constraints[(state1,state2)] = (states[state1] != states[state2])
	return constraints

def check_sol (statess, bigX, littleX, bigY, littleY):
	checkstates = copy.deepcopy(statess)
	checkstates[bigX] = littleX
	checkstates[bigY] = littleY
	returnval = constraint_generator(checkstates).get((bigX,bigY), False)
	return returnval

def runAC3 (stts, domain, neighbs, queue = None):
	def constraint (x, y): return (x != y)
	def weirdlist (stts, neighbors): return [(statei, statek) for statei in stts for statek in neighbors[statei]]
	def AC3 (stts, domain, neighbs, queue = None):
		if queue == None:
			queue = weirdlist(stts, neighbs)
		while queue:
			(statei, statej) = queue.pop()
			if remove_arcs(stts, domain, neighbs, statei, statej):
				"""if len(domain[statei]) == 0:
					return False"""
				for statek in neighbs[statei]:
					queue.append((statek, statei))

	def remove_arcs(stts, domain, neighbs, statei, statej):
		"""def consistent(state1, state2):
			for poss_value in domain[state2]:
				if state2 in neighbors[state1]: #& poss_val !=x:
					return True
			return False"""
		gone = False
		for restaurantx in domain[statei]:
			arc_checker = (map(lambda restauranty: not (restaurantx != restauranty), domain[statej]))
			if arc_checker == [False for x in range(len(arc_checker))]:
				#print not map(lambda restauranty: check_sol(stts, statei, restaurantx, statej, restauranty), domain[statej])
				#print domain
				domain[statei].remove(restaurantx)
				gone = True
		return gone

unassigned = copy.deepcopy(states.keys())
curr_domains = copy.deepcopy(state_domains)
curr_deleted = {}
for state in states:
	curr_deleted[state] = []

star_weight = 4
reviews_weight = 3

def stardomain(var, curr_domains):
	if curr_domains:
		stardomain = sorted(curr_domains[state], key = lambda restaurant: (star_weight*math.log10(restaurant['stars']) + reviews_weight*math.log10(restaurant['review_count']))/(star_weight + reviews_weight))
		stardomain.reverse()
	else:
		stardomain = sorted(state_domains[state], key = lambda restaurant: (star_weight*math.log10(restaurant['stars']) + reviews_weight*math.log10(restaurant['review_count']))/(star_weight + reviews_weight))
		stardomain.reverse()
	return stardomain

def backtrack(states, domains, neighbors, user_dict):
	counter = 0
	curr_domains = copy.deepcopy(domains)
	for meal in states:
		curr_deleted[meal] = []
	return recurse({}, states, domains, neighbors, user_dict)

varr = [None]
def recurse(assignment, states, domains, neighbors, user_dict):
	if len(unassigned) == 0:
		return assignment

	varr[0] = literallyjustchoosearandomvariablebecauseforsomereasonwhatimdoingisntworking()

	for val in stardomain(varr[0], curr_domains):
		assignment[varr[0]] = val
		forwardcheck(varr[0], val, assignment, user_dict)
		nextstep = recurse(assignment, states, domains, neighbors, user_dict)
		if nextstep != None:
			return nextstep
	return None

def forwardcheck(var, val, assignment, user_dict):
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

no_mexican_constraints = {'Unique': True, 'Mexican': 0, 'Pizza': 0}

def literallyjustchoosearandomvariablebecauseforsomereasonwhatimdoingisntworking():
	var = random.choice(unassigned)
	unassigned.remove(var)
	return var
