import tarfile
import zipfile
import json
import geopy.distance
import copy
import random

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

	"""def state_setter (state):
		highest_star = -float('inf')
		best_rest = None
		for restaurant in state_domains[state]:
			if restaurant['stars'] > highest_star:
				best_rest = restaurant
		return best_rest

	for state in states:
		states[state] = state_setter(state)

	return states"""

assigned = []
unassigned = copy.deepcopy(states.keys())

curr_domains = {}
curr_deleted = {}

stardomains = {sorted(state_domains[state], key = lambda restaurant: restaurant['stars']).reverse() for state in state_domains}
statedomain = (sorted(state_domains[(0,1)], key = lambda restaurant: restaurant['stars'])).reverse()

for state in state_domains:
	for restaurant in state_domains[state]:


def backtrack(states, domains, neighbors):
	curr_domains = copy.deepcopy(domains)
	for meal in states:
		curr_deleted[meal] = []
	return recurse({}, states, domains, neighbors)


def recurse(assignment, states, domains, neighbors):
	if len(unassigned) == 0:
		return states

	var = random.choice(unassigned)

	for val in stardomains[var]:
		assignment[var] = val
		unassigned.remove(var)
		if curr_domains:
			forwardcheck(var, val, assignment)
		nextstep = recurse(assignment, states, domains, neighbors)
		if nextstep != None:
			return nextstep
	return None

#do the variable ordering and order th
	def forwardcheck(var, val, assignment):
		if curr_domains:
			for (meal, restaurant) in curr_deleted[var]:
				curr_domains[meal].append(restaurant)
			pruned[var] = []

			for meal in neaighbors[var]:
				if meal not in assignment:
					for restaurant in curr_domains[meal][:]:
						if not check_sol(var, val, meal, restaurant):
							curr_domains[meal].remove(restaurant)
							curr_deleted[var].append((meal, restaurant))

practice_domains = {'a':[1,2,3,4],'b':[1,2,3,4],'c':[1,2,3,4],'d':[1,2,3,4]} 
practice_states = {'a':None,'b':None,'c':None,'d':None} 
practice_neighbors = {'a':['b','d'],'b':['a','c'],'c':['b','d',],'d':['a','c']}
