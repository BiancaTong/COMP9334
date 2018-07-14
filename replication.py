"""
This file using two extra output files from simulation.py, which are rf_*.txt and kf_*.txt.
The code generate these two files in simulation.py are commented, you should uncommented them before run this file.
rf_*.txt records the mean response time of first k jobs and kf_*.txt records the number of jobs.

Each time we need to run wrapper.py with different seed first
and then run replication.py to get mean response time which is removing the transient before 400.
"""

import matplotlib.pyplot as plt
from math import *

file_num_test = open('num_tests.txt', 'r')
test_num = int(file_num_test.read())

for test_index in range(1, test_num+1):
    rf = open('rf_'+str(test_index)+'.txt', 'r')
    kf = open('kf_'+str(test_index)+'.txt', 'r')
    r = rf.readlines()
    r = [float(x.strip()) for x in r]
    k = kf.readlines()
    k = [float(x.strip()) for x in k]
    sum_time = r[-1]*k[-1]-r[k.index(400)]*400
    k_num = k[-1]-k[k.index(400)]
    response_time = sum_time/k_num
    print("seed = 0, mean_response_time = {}".format(response_time))
    rf.close()
    kf.close()
"""
# code below is used to compute the confident interval

L1 = [3.757,3.752,3.822,3.861,3.805,3.916,3.853,3.841,3.720,3.820,3.850,3.813,3.874,3.857,3.736,3.888,3.835,3.873,3.845,3.770]

l =  sum(L)/20
LL = [(x-l)*(x-l) for x in L]
print(sqrt(sum(LL)/19))


L2 = [6.055,6.018,6.062,6.126,6.024,6.087,6.022,6.071,5.994,6.000,6.058,6.102,6.148,6.095,5.914,6.104,6.044,6.031,6.031,6.126]

print(sum(L))
l =  sum(L)/20
print(l)
LL = [(x-l)*(x-l) for x in L]
print(sqrt(sum(LL)/19))

L3 = []
for i in range(0, len(L1)):
    L3.append(L2[i]-L1[i])
print(sum(L3)/20)
LL = [(x-sum(L3)/20)*(x-sum(L3)/20) for x in L3]
print(sqrt(sum(LL)/19))
"""
