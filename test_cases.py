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

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)"""

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

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)"""

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

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)"""

"""Test Case Category 2 holds everything constant but the number of constraints"""
"""
TEST CASE 2
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city2 = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals2 = 6
constraints2 = {'Unique': True, 'Mexican': 1, 'Pizza': 1}
weights2 = {'reviews': 2, 'stars': 5}
test_case2 = (city2, weights2['reviews'], weights2['stars'], num_meals2, constraints2)

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 2 OUTPUT:")
format_meals(output, weights, run_time)"""

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
constraints2a = {'Unique': True, 'Mexican': 1, 'Pizza': 1}
weights2a = {'reviews': 2, 'stars': 5}
test_case2a = (city2a, weights2a['reviews'], weights2a['stars'], num_meals2a, constraints2a)

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 2 OUTPUT:")
format_meals(output, weights, run_time)"""

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
constraints2b = {'Unique': True, 'Mexican': 0, 'Pizza': 1, 'Chinese': 2}
weights2b = {'reviews': 2, 'stars': 5}
test_case2b = (city2b, weights2b['reviews'], weights2b['stars'], num_meals2b, constraints2b)

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 2 OUTPUT:")
format_meals(output, weights, run_time)"""

"""
TEST CASE 2c
	"Basic plus a few constraints, some weight on reviews"
	City: 'Phoenix'
	Constraints: {'Unique': True, 'Mexican': 0, 'Pizza': 0}
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 6
"""
# Filter down to restaurants in Phoenix
city2c = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals2c = 6
constraints2c = {'Unique': True, 'Mexican': 1, 'Pizza': 0, 'Chinese': 1, 'Bars': 1, 'Japanese': 2}
weights2c = {'reviews': 2, 'stars': 5}
test_case2c = (city2c, weights2c['reviews'], weights2c['stars'], num_meals2c, constraints2c)

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 2 OUTPUT:")
format_meals(output, weights, run_time)"""

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

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 2 OUTPUT:")
format_meals(output, weights, run_time)"""

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

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 2 OUTPUT:")
format_meals(output, weights, run_time)"""

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

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 2 OUTPUT:")
format_meals(output, weights, run_time)"""

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

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)"""

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

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)"""

"""
TEST CASE 4c
	"Basic"
	City: 'Phoenix'
	Constraints: {'Unique': True}
	Weights: {'reviews': 5, 'stars': 0}
	num_meals: 6 
"""
# Filter down to restaurants in Phoenix
city4c = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals4c = 6
constraints4c = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights4c = {'reviews': 5, 'stars': 0}
test_case4c = (city4a, weights4c['reviews'], weights4c['stars'], num_meals4c, constraints4c)

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)"""

"""
TEST CASE 5a
	"Basic"
	City: 'Phoenix'
	Constraints: Few
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 10
"""
# Filter down to restaurants in Phoenix
city5a = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals5a = 10
constraints5a = {'Unique': False, 'Mexican': 1, 'Pizza': 1}
weights5a = {'reviews': 2, 'stars': 5}
test_case5a = (city5a, weights5a['reviews'], weights5a['stars'], num_meals5a, constraints5a)

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)"""

"""
TEST CASE 5b
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 50
"""
# Filter down to restaurants in Phoenix
city5b = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals5b = 51
constraints5b = {'Unique': False, 'Mexican': 1, 'Pizza': 3, 'Sports Bars': 2, 'Japanese': 17, }
weights5b = {'reviews': 2, 'stars': 5}
test_case5b = (city5b, weights5b['reviews'], weights5b['stars'], num_meals5b, constraints5b)

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)"""

"""
TEST CASE 5c
	"Basic"
	City: 'Phoenix'
	Constraints: Many
	Weights: {'reviews': 2, 'stars': 5}
	num_meals: 100
"""
# Filter down to restaurants in Phoenix
city5c = 'Belmont'
#rests = filter_restaurants(data, 'Phoenix')
num_meals5c = 30
constraints5c = {'Unique': False, 'Mexican': 1, 'Pizza': 1, 'Sports Bars': 5, 'Japanese': 10, 'Chinese': 6, 'Juice': 2, 'Pubs': 1, 'Indian': 9, 'Bagels': 3}
weights5c = {'reviews': 2, 'stars': 5}
test_case5c = (city5c, weights5c['reviews'], weights5c['stars'], num_meals5c, constraints5c)

"""# Make initial greedy assignment
curr_rests = make_greedy(rests, num_meals, weights)
# Get output
output, run_time = min_conflicts(curr_rests, num_meals, constraints, weights)
# Print output
print("TEST CASE 1 OUTPUT:")
format_meals(output, weights, run_time)"""