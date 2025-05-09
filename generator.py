from itertools import product, permutations
import json
import time
import subprocess
import os
from config import numoflets  
from config import include_numbers

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(numoflets)
list1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

if include_numbers:
    list1 += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
combinedlist = product(list1, repeat=numoflets)
combinedlist = [''.join(combination) for combination in combinedlist]

perm_list = [''.join(p) for p in permutations(list1, numoflets)]

combinedlist.extend(perm_list)

file_path = 'plates.json'

if os.stat(file_path).st_size == 0:
    oldlist = []
else:
    with open(file_path, 'r') as file:
        try:
            oldlist = json.load(file)
        except json.JSONDecodeError:
            oldlist = []

oldlist[:] = combinedlist

with open(file_path, 'w') as file:
    json.dump(list(set(oldlist)), file) 



time.sleep(1)

subprocess.run(["python", "inputfunction.py"])
