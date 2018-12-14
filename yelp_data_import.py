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
	#return queue

def remove_arcs(stts, domain, neighbs, statei, statej):
	#figure out what the fuck [:] means and change it to your own syntax 
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
	print gone

	return gone

practice_domains = {'a':[1,2,3,4],'b':[1,2,3,4],'c':[1,2,3,4],'d':[1,2,3,4]} 
practice_states = {'a':None,'b':None,'c':None,'d':None} 
practice_neighbors = {'a':['b','d'],'b':['a','c'],'c':['b','d',],'d':['a','c']}

"""for state in domain[state1][:]:
	if every(lambda y: not constraint_generator(states)[(state1,state2)], state_domains[state2]):
		domain[state1].remove(state)
		gone = True
return gone"""

"""def num_conflicts(states, domain, state):
	counter = 0
	relevant_constraints = {}
	for key in states.keys():
		s1, s2 = key
		if s1 == state:
			relevant_constraints[(s1,s2)] = copy.deepcopy(constraints[(s1,s2)])
		if s2 == state:
			relevant_constraints[(s1,s2)] = copy.deepcopy(constraints[(s1,s2)])

	for constraint in relevant_constraints:
		if constraint == False
			counter += 1
	return counter"""

"""def min_conflicts(stts, domain, neighbs, maxx):
	current = {} 
	for state in states:
		#should be least conflicts assignment but get to that later
		current[state] = random.choice(domain[state])
	for step in range(maxx):
		for state in states:
			conflicted = None
			if not conflicted:
				return current
			newState = random.choice(conflicted)
			newRest = random.choice()"""

"""def is_solution (states):
	val = 0
	for constraint in constraint_generator(states):
		if constraint_generator(states) == False:
			val += 1
	if val == 0:
		return True
	else:
		return False

def backtracking (states, domains, forwardcheck = True):
	if is_solution(states):
		return states
	else: """






# should the constraints be the actual restaurants or the exact user input?
# if it were exact restaurants, all mexican and italian restaurants would have 
# to be included



