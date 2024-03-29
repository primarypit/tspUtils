import random
import os
import tsplib95
from TspLoader import *

Tspfolder = 'tspdata/'

type_set = set()

tsp_test_data = {}

sample_200 = []
#sample_1000 = []
sample_ohter = []
for filename in os.listdir(Tspfolder):
    if filename.endswith('.tsp'):
        problem = tsplib95.load(Tspfolder + filename)
        if problem.dimension <= 200:
            sample_200.append(filename)
        #elif problem.dimension <= 5000:
            #sample_1000.append(filename)
        else:
            sample_ohter.append(filename)

sample_files = []
sample_files += random.sample(sample_200,4)
sample_files += random.sample(sample_ohter,2)
left_files = list(set(os.listdir(Tspfolder)) - set(sample_files))

minv = 0
maxv = None

for f in sample_files:
    tmp = TspToMatrix(Tspfolder + f)
    tmp_matrix = tmp.return_matrix()
    tsp_test_data[f.split('.')[0]] = tmp_matrix / np.max(tmp_matrix) # normalize to [0,1]

with open('tspTestset.py', 'w') as file:
    # Write the dictionary as code to the file
    file.write("import numpy as np\n\n")
    file.write("sample_files = " + str(sample_files) + "\n\n")
    file.write("left_files = " + str(left_files) + "\n\n")
    file.write('tsp_test_data = {\n')
    for key, value in tsp_test_data.items():
        file.write("    \"{}\": np.array({}),\n".format(key,value.tolist()))
    file.write('}')