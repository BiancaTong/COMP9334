"""
Name: Bingxin Tong
zid:  z5093617

This code is written for COMP9334 Project, using Python3.5.

This code is used to test my simulation function code, which is 'pro.py'.
Thus, you need to put these two files in a same folder.

You can run command below to run this code:
python3 wrapper.py

All you need to do is to put this code and the simulation function code into a same folder with all configuration files,
such as: num_tests.txt, mode_*.txt, para_*.txt, arrival_*.txt, service_*.txt.

There will be two kinds of output files in the same directory:
mrt_*.txt: containing the mean response time
departure_*.txt:  containing the arrival time and departure time of jobs

"""

from math import *
from simulation import *
#import matplotlib.pyplot as plt

# Read the file num_tests.txt to determine the number of tests
file_num_test = open('num_tests.txt', 'r')
test_num = int(file_num_test.read())
for test_index in range(1, test_num+1):

    # Read in the configuration files for the test_index
    file_mode = open('mode_'+str(test_index)+'.txt', 'r')
    file_para = open('para_'+str(test_index)+'.txt', 'r')
    file_arrival = open('arrival_'+str(test_index)+'.txt', 'r')
    file_service = open('service_'+str(test_index)+'.txt', 'r')

    # Set the simulation mode and parameter values
    mode = file_mode.read().strip()
    if mode == 'trace':
        m = int(file_para.readline().strip())
        setup_time = float(file_para.readline().strip())
        delayedoff_time = float(file_para.readline().strip())
        arrival = file_arrival.readlines()
        arrival = [float(x.strip()) for x in arrival]
        service = file_service.readlines()
        service = [float(x.strip()) for x in service]
        time_end = inf
        random_seed = 0 # no use in trace mode
        # Call simulation function
        simulation_program(mode, arrival, service, m, setup_time, delayedoff_time, time_end, test_index, random_seed)

    else:
        m = int(file_para.readline().strip())
        setup_time = float(file_para.readline().strip())
        delayedoff_time = float(file_para.readline().strip())
        time_end = float(file_para.readline().strip())
        arrival = float(file_arrival.readline().strip())
        service = float(file_service.readline().strip())
        random_seed = 100
        # Call simulation function
        simulation_program(mode, arrival, service, m, setup_time, delayedoff_time, time_end, test_index, random_seed)
    file_mode.close()
    file_para.close()
    file_arrival.close()
    file_service.close()
"""
t = []
d = []
ll = [0.1,1.1,2.1,3.1,4.1,5.1,6.1,7.1,8.1,9.1,10.1,11.1,12.1,13.1,14.1,15.1,16.1,17.1,18.1,19.1]
for delayedoff_time in ll:
    d.append(delayedoff_time)
    simulation_program('random', float(0.35), float(1.0), 5, 5, delayedoff_time, 10000, 1, 0)
    mrt = open('mrt_1.txt','r')
    t.append(float(mrt.readline().strip()))
    mrt.close()
plt.plot(d,t,linewidth=2)
plt.xlabel('Tc -- delayedoff time')
plt.ylabel('Mean response time')
plt.show()
"""
