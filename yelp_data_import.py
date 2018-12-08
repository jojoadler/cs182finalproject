import tarfile
import zipfile
import json
import geopy.distance
import copy
import random

# Track filepath - note that this will need to be changed
filepath = '/Users/jojoadler/Desktop/yelp_academic_dataset_business.json'

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
user_inputs = {'days': [3], 'state': ['AZ'], 'city': ['Phoenix'], 'cuisines': [['Mexican', 1],['Italian', 2]], 'base_location': [(33.4484,-112.0740)], 'maxDist': [10]}
# constraints for the sample problem, for now this is hardcoded, but should be automatically constructed
constraints = [('Mexican', 'Italian'), ('Italian', 'Mexican')]

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

state_domains = dict.fromkeys(copy.deepcopy(states), possible_restaurants)

# creating arcs
def constraint_generator(states):
	constraints = {}
	states_not_checked1 = copy.deepcopy(states)
	for state1 in states:
		del states_not_checked1[state1]
		for state2 in states_not_checked1:
			constraints[(state1,state2)] = states[state1] != states[state2]
	return constraints

weirdlist = [(state1, state2) for state1 in states for state2 in neighbors[state1]]
def AC3 (stts, domain, neighbs, queue = None):
	if queue == None:
		queue = weirdlist
	while queue:
		(state1, state2) = queue.pop()
		if remove_arcs(stts, domain, neighbs, state1, state2):
			if len(domain[state1]) ==0:
				return False
			for state3 in neighbors[state1]:
				queue.append((state3, state1))
	return queue

def remove_arcs(stts, domain, neighbs, state1, state2):
	#figure out what the fuck [:] means and change it to your own syntax 
	def consistent(state1, state2):
		for poss_value in domain[state2]:
			if state2 in neighbors[state1]: #& poss_val !=x:
				return True
		return False

	gone = False

	for restaurant in domain[state1]:
		if not consistent(state1, state2):
			states[state1] = restaurant
			gone = True

	return gone
	"""for state in domain[state1][:]:
		if every(lambda y: not constraint_generator(states)[(state1,state2)], state_domains[state2]):
			domain[state1].remove(state)
			gone = True
	return gone"""

def min_conflicts(stts, domain, neighbs, maxx):
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
			newRest = random.choice()



# should the constraints be the actual restaurants or the exact user input?
# if it were exact restaurants, all mexican and italian restaurants would have 
# to be included



