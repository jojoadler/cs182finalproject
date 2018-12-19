import csv
from backtracking_yelp import test_maker
#WRITTEN IN PYTHON 2

def data_to_csv(testcase, city, num_meals, num_con, review, star, time, rating, sat, csvname):
	with open(csvname, 'a') as csvfile:
		filewriter = csv.writer(csvfile, delimiter=',',
                            	quotechar='|', quoting=csv.QUOTE_MINIMAL)
		filewriter.writerow([testcase, city, num_meals, num_con, review, star, time, rating, sat])

def write_to_csv(test_case, name):
	data_to_csv(name, str(test_case[0]), str(test_case[3]), str(len(test_case[4]) - 1), str(test_case[1]), str(test_case[2]), str(test_maker(test_case)[1]), str(test_maker(test_case)[0]), 'TRUE', 'backtracking.csv')
"""THE BASIC BASE CASE FROM WHICH EACH TEST VARIES:
City: 'Phoenix'
Constraints: {'Unique': False, 'Mexican': 1, 'Pizza': 1}
Weights: {'reviews': 2, 'stars': 5}
num_meals = 6 (days = 2)

Therefore, we will test for different cities, constraints length, uniqueness, weights, and num_meals"""

"""Test Case Category 1 holds everything constant but the location"""
"""
TEST CASE 1a
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6 
"""
# Filter down to restaurants in Phoenix
city1a = 'Phoenix'
#rests1 = filter_restaurants(data, 'Phoenix')
num_meals1a = 6
constraints1a = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights1a = {'reviews': 2, 'stars': 5}
test_case1a = (city1a, weights1a['reviews'], weights1a['stars'], num_meals1a, constraints1a)

"""
TEST CASE 1b
	"Basic"
	City: 'Belmont'
	Constraints: {'Unique': True}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Belmont
city1b = 'Belmont'
#rests = filter_restaurants(data, 'Belmont')
num_meals1b = 6
constraints1b = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights1b = {'reviews': 2, 'stars': 5}
test_case1b = (city1b, weights1b['reviews'], weights1b['stars'], num_meals1b, constraints1b)
score1b, runtime1b = test_maker(test_case1b)

"""
TEST CASE 1c
	"Basic"
	City: 'Parma'
	Constraints: {'Unique': True}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Parma
city1c = 'Concord'
#rests = filter_restaurants(data, 'Parma')
num_meals1c = 6
constraints1c = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights1c = {'reviews': 2, 'stars': 5}
test_case1c = (city1c, weights1c['reviews'], weights1c['stars'], num_meals1c, constraints1c)
score1c, runtime1c = test_maker(test_case1c)

"""
TEST CASE 2a
	"Basic plus a few constraints"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city2a = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals2a = 6
constraints2a = {'Unique': True, 'Mexican': 0, 'Pizza': 0}
weights2a = {'reviews': 2, 'stars': 5}
test_case2a = (city2a, weights2a['reviews'], weights2a['stars'], num_meals2a, constraints2a)
score2a, runtime2a = test_maker(test_case2a)

"""
TEST CASE 2b
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city2b = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals2b = 6
constraints2b = {'Unique': True, 'Mexican': 0, 'Pizza': 0, 'Chinese': 0}
weights2b = {'reviews': 2, 'stars': 5}
test_case2b = (city2b, weights2b['reviews'], weights2b['stars'], num_meals2b, constraints2b)
score2b, runtime2b = test_maker(test_case2b)

"""
TEST CASE 2c
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city2c = 'Belmont'
num_meals2c = 6
constraints2c = {'Unique': True, 'Mexican': 0, 'Pizza': 0, 'Chinese': 0, 'Bars': 0, 'Japanese': 0}
weights2c = {'reviews': 2, 'stars': 5}
test_case2c = (city2c, weights2c['reviews'], weights2c['stars'], num_meals2c, constraints2c)
score2c, runtime2c = test_maker(test_case2c)

"""
TEST CASE 2d
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city2d = 'Belmont'
num_meals2d = 6
constraints2d = {'Unique': True, 'Mexican': 1, 'Pizza': 1, 'Chinese': 1, 'Bars': 1, 'Japanese': 1}
weights2d = {'reviews': 2, 'stars': 5}
test_case2d = (city2d, weights2d['reviews'], weights2d['stars'], num_meals2d, constraints2d)
score2d, runtime2d = test_maker(test_case2d)

"""
TEST CASE 2e
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city2e = 'Belmont'
num_meals2e = 6
constraints2e = {'Unique': True, 'Mexican': 1, 'Pizza': 0, 'Chinese': 1, 'Bars': 0, 'Japanese': 1, 'Barbecue':0}
weights2e = {'reviews': 2, 'stars': 5}
test_case2e = (city2e, weights2e['reviews'], weights2e['stars'], num_meals2e, constraints2e)

"""
TEST CASE 2f
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city2f = 'Belmont'
num_meals2f = 6
constraints2f = {'Unique': True, 'Mexican': 1, 'Pizza': 0, 'Chinese': 1, 'Bars': 0, 'Japanese': 1, 'Barbecue':0, 'Bakeries': 1, 'Food Trucks': 0, 'Taiwanese': 1, 'Donuts': 0, 'Hawaiian': 0, 'Salad': 0}
weights2f = {'reviews': 2, 'stars': 5}
test_case2f = (city2f, weights2f['reviews'], weights2f['stars'], num_meals2f, constraints2f)

"""
TEST CASE 2g
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
city2g = 'Belmont'
num_meals2g = 6
constraints2g = {'Unique': True, 'Mexican': 0, 'Pizza': 0, 'Chinese': 1, 'Bars': 0, 'Japanese': 1, 'Barbecue':0, 'Bakeries': 1, 'Food Trucks': 0, 'Taiwanese': 0, 'Donuts': 0, 'Hawaiian': 0, 'Salad': 0, 'Noodles': 0, 'Mediterranean': 0, 'Greek': 0, 'French': 1, 'Seafood': 0, 'Sandwiches': 0, 'Bagels': 0, 'British': 1}
weights2g = {'reviews': 2, 'stars': 5}
test_case2g = (city2g, weights2g['reviews'], weights2g['stars'], num_meals2g, constraints2g)

""" Test Case Category 3 is the same as Test Case Category 2 but with Unique = False"""

"""
TEST CASE 3a
	"Basic plus a few constraints"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city3a = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals3a = 6
constraints3a = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights3a = {'reviews': 2, 'stars': 5}
test_case3a = (city3a, weights3a['reviews'], weights3a['stars'], num_meals3a, constraints3a)

"""
TEST CASE 3b
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city3b = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals3b = 6
constraints3b = {'Unique': False, 'Mexican': 0, 'Pizza': 1, 'Chinese': 2}
weights3b = {'reviews': 2, 'stars': 5}
test_case3b = (city3b, weights3b['reviews'], weights3b['stars'], num_meals3b, constraints3b)

"""
TEST CASE 3c
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city3c = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals3c = 6
constraints3c = {'Unique': False, 'Mexican': 1, 'Pizza': 0, 'Chinese': 1, 'Bars': 1, 'Japanese': 2}
weights3c = {'reviews': 2, 'stars': 5}
test_case3c = (city3c, weights3c['reviews'], weights3c['stars'], num_meals3c, constraints3c)

"""
TEST CASE 4a
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 0, 'stars': 5}
	num_meals: 6 
"""
# Filter down to restaurants in Phoenix
city4a = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals4a = 6
constraints4a = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights4a = {'reviews': 0, 'stars': 5}
test_case4a = (city4a, weights4a['reviews'], weights4a['stars'], num_meals4a, constraints4a)


"""
TEST CASE 4b
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 3, 'stars': 3}
	num_meals: 6 
"""
# Filter down to restaurants in Phoenix
city4b = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals4b = 6
constraints4b = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights4b = {'reviews': 3, 'stars': 3}
test_case4b = (city4b, weights4b['reviews'], weights4b['stars'], num_meals4b, constraints4b)

"""
TEST CASE 4c
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 5, 'stars': 0}
	num_meals: 6 
"""
city4c = 'Belmont'
num_meals4c = 6
constraints4c = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights4c = {'reviews': 5, 'stars': 0}
test_case4c = (city4c, weights4c['reviews'], weights4c['stars'], num_meals4c, constraints4c)

"""
TEST CASE 4d
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 5, 'stars': 0}
	num_meals: 6 
"""
city4d = 'Belmont'
num_meals4d = 6
constraints4d = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights4d = {'reviews': 1, 'stars': 1}
test_case4d = (city4d, weights4d['reviews'], weights4d['stars'], num_meals4d, constraints4d)

"""
TEST CASE 4e
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 5, 'stars': 0}
	num_meals: 6 
"""
city4e = 'Belmont'
num_meals4e = 6
constraints4e = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights4e = {'reviews': 4, 'stars': 4}
test_case4e = (city4e, weights4e['reviews'], weights4e['stars'], num_meals4e, constraints4e)

"""
TEST CASE 4f
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 5, 'stars': 0}
	num_meals: 6 
"""
city4f = 'Belmont'
num_meals4f = 6
constraints4f = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights4f = {'reviews': 1, 'stars': 4}
test_case4f = (city4f, weights4f['reviews'], weights4f['stars'], num_meals4f, constraints4f)

"""
TEST CASE 4g
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 5, 'stars': 0}
	num_meals: 6 
"""
city4g = 'Belmont'
num_meals4g = 6
constraints4g = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights4g = {'reviews': 4, 'stars': 1}
test_case4g = (city4g, weights4g['reviews'], weights4g['stars'], num_meals4g, constraints4g)

"""
TEST CASE 5a
	"Basic"
	City: 'Phoenix'
	Constraints: Few
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 10
"""
city5a = 'Belmont'
num_meals5a = 10
constraints5a = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights5a = {'reviews': 2, 'stars': 5}
test_case5a = (city5a, weights5a['reviews'], weights5a['stars'], num_meals5a, constraints5a)

"""
TEST CASE 5b
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 50
"""
city5b = 'Belmont'
num_meals5b = 51
constraints5b = {'Unique': False, 'Mexican': 1, 'Pizza': 3, 'Sports Bars': 2, 'Japanese': 17}
weights5b = {'reviews': 2, 'stars': 5}
test_case5b = (city5b, weights5b['reviews'], weights5b['stars'], num_meals5b, constraints5b)


"""
TEST CASE 5c
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 100
"""
city5c = 'Belmont'
num_meals5c = 30
constraints5c = {'Unique': False, 'Mexican': 1, 'Pizza': 1, 'Sports Bars': 5, 'Japanese': 10, 'Chinese': 6, 'Juice': 2, 'Pubs': 1, 'Indian': 9, 'Bagels': 3}
weights5c = {'reviews': 2, 'stars': 5}
test_case5c = (city5c, weights5c['reviews'], weights5c['stars'], num_meals5c, constraints5c)

"""
TEST CASE 6a
	"Basic"
	City: 'Phoenix'
	Constraints: Few
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 10
"""
# Filter down to restaurants in Phoenix
city6a = 'Phoenix'
#rests = filter_restaurants(data, 'Phoenix')
num_meals6a = 10
constraints6a = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights6a = {'reviews': 2, 'stars': 5}
test_case6a = (city6a, weights6a['reviews'], weights6a['stars'], num_meals6a, constraints6a)

"""
TEST CASE 6b
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 50
"""
city6b = 'Phoenix'
num_meals6b = 51
constraints6b = {'Unique': False, 'Mexican': 1, 'Pizza': 3, 'Sports Bars': 2, 'Japanese': 17, }
weights6b = {'reviews': 2, 'stars': 5}
test_case6b = (city6b, weights6b['reviews'], weights6b['stars'], num_meals6b, constraints6b)


"""
TEST CASE 6c
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 100
"""
city6c = 'Phoenix'
num_meals6c = 30
constraints6c = {'Unique': False, 'Mexican': 1, 'Pizza': 1, 'Sports Bars': 5, 'Japanese': 10, 'Chinese': 6, 'Juice': 2, 'Pubs': 1, 'Indian': 9, 'Bagels': 3}
weights6c = {'reviews': 2, 'stars': 5}
test_case6c = (city6c, weights6c['reviews'], weights6c['stars'], num_meals6c, constraints6c)

"""
TEST CASE 7a
	"Basic"
	City: 'Phoenix'
	Constraints: Few
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 10
"""
# Filter down to restaurants in Phoenix
city7a = 'Concord'
#rests = filter_restaurants(data, 'Phoenix')
num_meals7a = 10
constraints7a = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights7a = {'reviews': 2, 'stars': 5}
test_case7a = (city7a, weights7a['reviews'], weights7a['stars'], num_meals7a, constraints7a)

"""
TEST CASE 7b
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 50
"""
city7b = 'Concord'
num_meals7b = 51
constraints7b = {'Unique': False, 'Mexican': 1, 'Pizza': 3, 'Sports Bars': 2, 'Japanese': 17, }
weights7b = {'reviews': 2, 'stars': 5}
test_case7b = (city7b, weights7b['reviews'], weights7b['stars'], num_meals7b, constraints7b)


"""
TEST CASE 7c
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 100
"""
city7c = 'Concord'
num_meals7c = 30
constraints7c = {'Unique': False, 'Mexican': 1, 'Pizza': 1, 'Sports Bars': 5, 'Japanese': 10, 'Chinese': 6, 'Juice': 2, 'Pubs': 1, 'Indian': 9, 'Bagels': 3}
weights7c = {'reviews': 2, 'stars': 5}
test_case7c = (city7c, weights7c['reviews'], weights7c['stars'], num_meals7c, constraints7c)

test_cases = [(test_case1a, '1a'), (test_case1b, '1b'),(test_case1c, '1c'), (test_case2a, '2a'), (test_case2b, '2b'), (test_case2c, '2c'), (test_case2d, '2d'), (test_case2e, '2e'), (test_case3a, '3a'), (test_case3b, '3b'), (test_case3c, '3c'), (test_case4a, '4a'), (test_case4b, '4b'), (test_case4c, '4c'), (test_case4d, '4d'), (test_case4e, '4e'), (test_case4f, '4f'), (test_case4g, '4g'), (test_case5a, '5a'), (test_case5b, '5b'), (test_case5c, '5c'), (test_case6a, '6a'), (test_case6b, '6b'), (test_case6c, '6c'), (test_case7a, '7a'), (test_case7b, '7b'), (test_case7c, '7c')]

for test in test_cases:
	write_to_csv(test[0], test[1])
