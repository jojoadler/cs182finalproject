"""
File to explore the yelp dataset, in order to effectively pick cities and constraints

Written in Python 3
"""
import json

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

def strip_categories(categories):
	# Converts a 'Categories' string into a list of categories
	cats = []
	if categories:
		cats = [x.strip() for x in categories.split(',')]
	return cats

def is_restaurant(business):
	cats = strip_categories(business['categories'])
	if 'Restaurants' in cats:
		return True
	return False

# get a list of all the different cities in dataset, sorted by number of restaurants
cities = {}
for business in data:
	if is_restaurant(business):
		city = business['city']
		if city in cities:
			cities[city] += 1
		else:
			cities[city] = 1
sorted_cities = sorted(cities.items(), key=lambda kv: kv[1], reverse=True)
print("Cities by restaurants", sorted_cities)

num_businesses = sum(cities.values())
print("num_businesses", num_businesses)
# Toronto, Vegas, Phoenix have the most