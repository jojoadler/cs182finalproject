import tarfile
import zipfile
import json

# Track filepath - note that this will need to be changed
filepath = '/Users/amydanoff/Desktop/yelp_dataset/dataset_business.json'

# Function that returns formatted data
def open_data(filepath):
	data = []
	with open(filepath) as f:
	    data = f.readlines()
	    data = list(map(json.loads, data)) 
	return data

#Test
data = open_data(filepath)
print(data[0]['categories'])