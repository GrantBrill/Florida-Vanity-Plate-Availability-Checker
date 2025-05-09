from itertools import product
import json
import time
import subprocess
import os

from openme import numoflets  

list1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


combinedlist = product(list1, repeat=numoflets)
combinedlist = [''.join(combination) for combination in combinedlist]

file_path = 'Florida License Plate Project/plates.json'

# Check if the file is empty
if os.stat(file_path).st_size == 0:
    print(f"{file_path} is empty. Continuing with an empty list.")
    oldlist = []  # Initialize as an empty list
else:
    # If file is not empty, load the existing data
    with open(file_path, 'r') as file:
        try:
            oldlist = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON in {file_path}. Continuing with an empty list.")
            oldlist = []

oldlist[:] = combinedlist

with open(file_path, 'w') as file:
    json.dump(oldlist, file) 

time.sleep(1)

subprocess.run(["python", "Florida License Plate Project/inputfunction.py"])
