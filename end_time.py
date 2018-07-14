"""
This file using two extra output files from simulation.py, which are rf_*.txt and kf_*.txt.
The code generate these two files in simulation.py are commented, you should uncommented them before run this file.
rf_*.txt records the mean response time of first k jobs and kf_*.txt records the number of jobs.

Each time you need to change the end time in para.txt
then run wrapper.py first and then run end_time.py to get plot.
"""

import matplotlib.pyplot as plt

file_num_test = open('num_tests.txt', 'r')
test_num = int(file_num_test.read())

for test_index in range(1, test_num+1):
    rf = open('rf_'+str(test_index)+'.txt', 'r')
    kf = open('kf_'+str(test_index)+'.txt', 'r')
    r = rf.readlines()
    r = [float(x.strip()) for x in r]
    k = kf.readlines()
    k = [float(x.strip()) for x in k]
    plt.plot(k,r,linewidth=2)
    plt.xlabel('k -- number of jobs')
    plt.ylabel('Mean response time of first k jobs')
    plt.title('End time is 10000 s')
    plt.show()
    rf.close()
    kf.close()
