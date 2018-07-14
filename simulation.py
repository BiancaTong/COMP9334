"""

Input parameters:
1. mode: string type, to control whether your program will run simulation using randomly generated arrival and service times, or in trace driven mode. The value that the parameter mode can take is either random or trace.
2. arrival: supplying arrival information to the program. The meaning of arrival depends on mode.
3. service: supplying service time information to the program. The meaning of service depends on mode.
4. m: the number of servers, a positive integer.
5. setup_time: setup time, a positive ﬂoating point number.
6. delayedoff_time: the initial value of the countdown timer Tc, a positive ﬂoating point number.
7. time_end: stops the simulation if the master clock exceeds this value, only relevant when mode is random, a positive ﬂoating point number.
8. test_index: the index of the input test file, in order to name the output files.
9. random_seed: the random seed of random function, only relevant when mode is random.


Server states:
1. [0]OFF: the server is powered oﬀ and cannot process a job.
2. [1]SETUP: a server in the OFF state is powered on and cannot process a job,  'setup_time' refer to the time needed to boot up the server.
3. [2]BUSY: the server is processing a job.
4. [3]DELAYEDOFF: during a countdown timer 'delayedoff_time', the server is still powered on, after that without any job come in, turn to OFF, otherwise, turn to BUSY.


Four events:
1. [0]An arrival event:
The dispatcher cannot send a job to a server in OFF, SETUP or BUSY state.
next_arrival_time = the time at which the next customer arrives
service_time_next_arrival = the service time of the next arrival

2. [1]A departure event:
next_departure_time = the time at which the next departure occurs
arrival_time_next_departure = the time at which the next departing customer arrives at the system

3. [2]A SETUP finished event:
This server will take a MARKED job oﬀ the queue.
next_setup_finished_time = the time the status of the server will change from SETUP to BUSY

4. [3]A DELAYEDOFF expired event:
next_delayedoff_expiried_time = the time the status of the server will change from DELAYEDOFF to OFF

"""

from math import *
from random import *

def simulation_program(mode, arrival, service, m, setup_time, delayedoff_time, time_end, test_index, random_seed):
    # The cumulative response time
    response_time_cumulative = 0
    # number of completed customers at the end of the simulation
    num_customer_served = 0
    # departure time of an event
    departure_time = []
    # arrival time of a departure event
    arrival_time_departure = []

    #### Type of mode ####
    if mode == 'random':
        ### Initialising the seed number
        seed(random_seed)

        ### Initialising the arrival event ###
        # arrival = λ. the mean arrival rate of the jobs is λ, the inter-arrival probability distribution is exponentially distributed with parameter λ.
        mean_arrival_rate = arrival
        next_arrival_time = -log(1.0-uniform(0,1))/mean_arrival_rate

        # service = µ. sk = s1k + s2k + s3k, where s1k, s2k and s3k are exponentially distributed random numbers with parameter µ.
        mean_service_rate = service
        s_1 = -log(1.0-uniform(0,1))/mean_service_rate
        s_2 = -log(1.0-uniform(0,1))/mean_service_rate
        s_3 = -log(1.0-uniform(0,1))/mean_service_rate
        service_time_next_arrival = s_1 + s_2 + s_3
        #print(next_arrival_time,service_time_next_arrival)
        #service_time_next_arrival = (-log(1.0-random())/mean_service_rate)+(-log(1.0-random())/mean_service_rate)+(-log(1.0-random())/mean_service_rate)

        ### Initialise both departure events to empty ###
        next_departure_time = [inf]*m

        ### Initialise SETUP finished events ###
        next_setup_finished_time = [inf]*m

        ### Initialise DELAYEDOFF expiried events ###
        next_delayedoff_expiried_time = [inf]*m

        #### Initialising the Master clock, server status, queue_length, buffer_content ####
        # Intialise the master clock
        master_clock = 0
        # Intialise server status
        server = [0]*m #OFF
        arrival_time_next_departure = [inf]*m
        # Initialise buffer
        buffer_content = []
        queue_length = 0
        response_time_list = [0]
        k_list = [0]
        #### Start iteration until the end time ####
        while master_clock < time_end:

            ### New event ###
            # next_departure
            first_departure_time = min(next_departure_time)
            first_departure_server = next_departure_time.index(min(next_departure_time))
            # next_setup_finished
            first_setup_finished_time = min(next_setup_finished_time)
            first_setup_finished_server = next_setup_finished_time.index(min(next_setup_finished_time))
            # next_delayedoff_expiried
            first_delayedoff_expiried_time = min(next_delayedoff_expiried_time)
            first_delayedoff_expiried_server = next_delayedoff_expiried_time.index(min(next_delayedoff_expiried_time))

            ### Type of new event ###
            if next_arrival_time == min([next_arrival_time,first_departure_time,first_setup_finished_time,first_delayedoff_expiried_time]):
                next_event_type = 0 # arrival event
                next_event_time = next_arrival_time
            elif first_departure_time == min([next_arrival_time,first_departure_time,first_setup_finished_time,first_delayedoff_expiried_time]):
                next_event_type = 1 # departure event
                next_event_time = first_departure_time
            elif first_setup_finished_time == min([next_arrival_time,first_departure_time,first_setup_finished_time,first_delayedoff_expiried_time]):
                next_event_type = 2 # SETUP finished event
                next_event_time = first_setup_finished_time
            else:
                next_event_type = 3 # DELAYEDOFF expiried event
                next_event_time = first_delayedoff_expiried_time

            ### Update master_clock ###
            master_clock = next_event_time

            ### Take actions depending on the event type ###
            # arrival
            if next_event_type == 0:
                # at least a server in the DELAYEDOFF state
                if 3 in server:
                    # choose a server with the highest value in the countdown timer
                    countdown_timer_list = [x for x in next_delayedoff_expiried_time if x != inf]
                    server_choosed = next_delayedoff_expiried_time.index(max(countdown_timer_list))
                    # the selected server will change its state to BUSY
                    server[server_choosed] = 2
                    # the selected server will cancel its countdown timer
                    next_delayedoff_expiried_time[server_choosed] = inf
                    # update the property of this server
                    next_departure_time[server_choosed] = next_arrival_time + service_time_next_arrival
                    arrival_time_next_departure[server_choosed] = next_arrival_time
                else:
                    # at least a server in the OFF state
                    if 0 in server:
                        # select one of OFF servers and turn it on
                        server_choosed = server.index(0)
                        # the selected server will change its state to SETUP
                        server[server_choosed] = 1
                        # put the job in the queue and mark the job
                        buffer_content.append([next_arrival_time,service_time_next_arrival,'MARKED'])
                        queue_length += 1
                        # update the property of this server
                        next_setup_finished_time[server_choosed] = master_clock + setup_time
                    # all the servers are either in BUSY or SETUP state
                    else:
                        # the job is put in the queue and is UNMARKED
                        buffer_content.append([next_arrival_time,service_time_next_arrival,'UNMARKED'])
                        queue_length += 1

                # generate a new job and schedule its arrival
                next_arrival_time = master_clock -log(1.0-uniform(0,1))/mean_arrival_rate
                s_1 = -log(1.0-uniform(0,1))/mean_service_rate
                s_2 = -log(1.0-uniform(0,1))/mean_service_rate
                s_3 = -log(1.0-uniform(0,1))/mean_service_rate
                service_time_next_arrival = s_1 + s_2 + s_3
                #print(next_arrival_time,service_time_next_arrival)
                #next_arrival_time = master_clock -log(1.0-random())/mean_arrival_rate
                #service_time_next_arrival = (-log(1.0-random())/mean_service_rate)+(-log(1.0-random())/mean_service_rate)+(-log(1.0-random())/mean_service_rate)
            # departure
            elif next_event_type == 1:

                # Update the variables: Cumulative response time T; Number of departed customers N
                response_time_cumulative += master_clock - arrival_time_next_departure[first_departure_server]
                num_customer_served += 1
                departure_time.append(master_clock)
                arrival_time_departure.append(arrival_time_next_departure[first_departure_server])
                if num_customer_served % 5 == 0 or num_customer_served < 10:
                    response_time_list.append(response_time_cumulative/num_customer_served)
                    k_list.append(num_customer_served)

                #  the dispatcher queue is empty
                if queue_length == 0:
                    # the server will change its state from BUSY to DELAYEDOFF
                    server[first_departure_server] = 3
                    # start the countdown timer
                    next_delayedoff_expiried_time[first_departure_server] = master_clock + delayedoff_time
                    # update the property of this server
                    next_departure_time[first_departure_server] = inf
                    arrival_time_next_departure[first_departure_server] = inf
                # at least one job at the queue
                else:
                    if buffer_content[0][2] == 'UNMARKED':
                        # update the property of this server
                        next_departure_time[first_departure_server] = master_clock + buffer_content[0][1]
                        arrival_time_next_departure[first_departure_server] = buffer_content[0][0]
                        buffer_content = buffer_content[1:]
                        queue_length -= 1
                    else:
                        # update the property of this server
                        next_departure_time[first_departure_server] = master_clock + buffer_content[0][1]
                        arrival_time_next_departure[first_departure_server] = buffer_content[0][0]
                        buffer_content = buffer_content[1:]
                        queue_length -= 1
                        # check whether there is an UMARKED job in its queue
                        unmark_flag = False
                        for b in buffer_content:
                            # at least a UNMARKED job
                            if 'UNMARKED' in b:
                                unmark_flag = True
                                b[2] = 'MARKED'
                                break
                        # no UNMARKED jobs
                        if unmark_flag == False:
                            # turn oﬀ the server with the longest remaining setup time
                            setup_timer_list = [x for x in next_setup_finished_time if x != inf]
                            server_choosed = next_setup_finished_time.index(max(setup_timer_list))
                            # the selected server will change from SETUP to OFF
                            server[server_choosed] = 0
                            # update the property of this server
                            next_setup_finished_time[server_choosed] = inf

            # setup_finished
            elif next_event_type == 2:
                # the server will change from SETUP to BUSY
                server[first_setup_finished_server] = 2
                # update the property of this server
                next_departure_time[first_setup_finished_server] = master_clock + buffer_content[0][1]
                arrival_time_next_departure[first_setup_finished_server] = buffer_content[0][0]
                next_setup_finished_time[first_setup_finished_server] = inf
                # take a MARKED job oﬀ the queue
                buffer_content = buffer_content[1:]
                queue_length -= 1
            # delayedoff expiried
            else:
                # the server will change from DELAYEDOFF to OFF
                server[first_delayedoff_expiried_server] = 0
                # the selected server will cancel its countdown timer
                next_delayedoff_expiried_time[first_delayedoff_expiried_server] = inf


        # Write the output files
        if num_customer_served not in k_list:
            response_time_list.append(response_time_cumulative/num_customer_served)
            k_list.append(num_customer_served)

        avg_response_time = response_time_cumulative/num_customer_served
        response_file = open('mrt_'+str(test_index)+'.txt','w')
        response_file.write(str("%.3f" % round(avg_response_time,3))+'\n')
        response_file.close()

        departure_file = open('departure_'+str(test_index)+'.txt','w')
        for i in range(0, len(departure_time)):
            departure_file.write(str("%.3f" % round(arrival_time_departure[i],3))+'	 '+str("%.3f" % round(departure_time[i],3))+'\n')
        departure_file.close()
        """
        # test for transient and steady part
        rf = open('rf_'+str(test_index)+'.txt','w')
        for i in range(0, len(response_time_list)):
            rf.write(str(response_time_list[i])+'\n')
        rf.close()

        kf = open('kf_'+str(test_index)+'.txt','w')
        for i in range(0, len(k_list)):
            kf.write(str(k_list[i])+'\n')
        kf.close()
        """
    if mode == 'trace':

        ### Initialising the arrival event ###
        arrival_index = 0
        next_arrival_time = arrival[arrival_index]
        service_time_next_arrival = service[arrival_index]

        ### Initialise both departure events to empty ###
        next_departure_time = [inf]*m

        ### Initialise SETUP finished events ###
        next_setup_finished_time = [inf]*m

        ### Initialise DELAYEDOFF expiried events ###
        next_delayedoff_expiried_time = [inf]*m

        #### Initialising the Master clock, server status, queue_length, buffer_content ####
        # Intialise the master clock
        master_clock = 0.0
        # Intialise server status
        server = [0]*m #OFF
        arrival_time_next_departure = [inf]*m
        # Initialise buffer
        buffer_content = []
        queue_length = 0
        """
        print('Master clock    Dispatcher                       Servers')
        print("t={}          {}                               {}".format(master_clock,buffer_content,server))
        """
        #### Start iteration until the end time ####
        while True:

            ### Finished point ###
            # If the last arrival event has departured then break
            #if len(arrival_time_departure) != 0 and arrival_time_departure[-1] == arrival[-1]:
            if len(arrival_time_departure) == len(arrival):
                break

            ### New event ###
            # next_departure
            first_departure_time = min(next_departure_time)
            first_departure_server = next_departure_time.index(min(next_departure_time))
            # next_setup_finished
            first_setup_finished_time = min(next_setup_finished_time)
            first_setup_finished_server = next_setup_finished_time.index(min(next_setup_finished_time))
            # next_delayedoff_expiried
            first_delayedoff_expiried_time = min(next_delayedoff_expiried_time)
            first_delayedoff_expiried_server = next_delayedoff_expiried_time.index(min(next_delayedoff_expiried_time))

            ### Type of new event ###
            if next_arrival_time == min([next_arrival_time,first_departure_time,first_setup_finished_time,first_delayedoff_expiried_time]):
                next_event_type = 0 # arrival event
                next_event_time = next_arrival_time
            elif first_departure_time == min([next_arrival_time,first_departure_time,first_setup_finished_time,first_delayedoff_expiried_time]):
                next_event_type = 1 # departure event
                next_event_time = first_departure_time
            elif first_setup_finished_time == min([next_arrival_time,first_departure_time,first_setup_finished_time,first_delayedoff_expiried_time]):
                next_event_type = 2 # SETUP finished event
                next_event_time = first_setup_finished_time
            else:
                next_event_type = 3 # DELAYEDOFF expiried event
                next_event_time = first_delayedoff_expiried_time

            ### Update master_clock ###
            master_clock = next_event_time

            ### Take actions depending on the event type ###
            # arrival
            if next_event_type == 0:
                # at least a server in the DELAYEDOFF state
                if 3 in server:
                    # choose a server with the highest value in the countdown timer
                    countdown_timer_list = [x for x in next_delayedoff_expiried_time if x != inf]
                    server_choosed = next_delayedoff_expiried_time.index(max(countdown_timer_list))
                    # the selected server will change its state to BUSY
                    server[server_choosed] = 2
                    # the selected server will cancel its countdown timer
                    next_delayedoff_expiried_time[server_choosed] = inf
                    # update the property of this server
                    next_departure_time[server_choosed] = next_arrival_time + service_time_next_arrival
                    arrival_time_next_departure[server_choosed] = next_arrival_time
                else:
                    # at least a server in the OFF state
                    if 0 in server:
                        # select one of OFF servers and turn it on
                        server_choosed = server.index(0)
                        # the selected server will change its state to SETUP
                        server[server_choosed] = 1
                        # put the job in the queue and mark the job
                        buffer_content.append([next_arrival_time,service_time_next_arrival,'MARKED'])
                        queue_length += 1
                        # update the property of this server
                        next_setup_finished_time[server_choosed] = master_clock + setup_time
                    # all the servers are either in BUSY or SETUP state
                    else:
                        # the job is put in the queue and is UNMARKED
                        buffer_content.append([next_arrival_time,service_time_next_arrival,'UNMARKED'])
                        queue_length += 1

                # generate a new job and schedule its arrival
                arrival_index += 1
                if arrival_index < len(arrival):
                    next_arrival_time = arrival[arrival_index]
                    service_time_next_arrival = service[arrival_index]
                else:
                    # no arrival event at all
                    arrival_index -= 1
                    next_arrival_time = inf
                    service_time_next_arrival = inf
            # departure
            elif next_event_type == 1:

                # Update the variables
                response_time_cumulative += master_clock - arrival_time_next_departure[first_departure_server]
                num_customer_served += 1
                departure_time.append(master_clock)
                arrival_time_departure.append(arrival_time_next_departure[first_departure_server])

                #  the dispatcher queue is empty
                if queue_length == 0:
                    # the server will change its state from BUSY to DELAYEDOFF
                    server[first_departure_server] = 3
                    # start the countdown timer
                    next_delayedoff_expiried_time[first_departure_server] = master_clock + delayedoff_time
                    # update the property of this server
                    next_departure_time[first_departure_server] = inf
                    arrival_time_next_departure[first_departure_server] = inf
                # at least one job at the queue
                else:
                    if buffer_content[0][2] == 'UNMARKED':
                        # update the property of this server
                        next_departure_time[first_departure_server] = master_clock + buffer_content[0][1]
                        arrival_time_next_departure[first_departure_server] = buffer_content[0][0]
                        buffer_content = buffer_content[1:]
                        queue_length -= 1
                    else:
                        # update the property of this server
                        next_departure_time[first_departure_server] = master_clock + buffer_content[0][1]
                        arrival_time_next_departure[first_departure_server] = buffer_content[0][0]
                        buffer_content = buffer_content[1:]
                        queue_length -= 1
                        # check whether there is an UMARKED job in its queue
                        unmark_flag = False
                        for b in buffer_content:
                            # at least a UNMARKED job
                            if 'UNMARKED' in b:
                                unmark_flag = True
                                b[2] = 'MARKED'
                                break
                        # no UNMARKED jobs
                        if unmark_flag == False:
                            # turn oﬀ the server with the longest remaining setup time
                            setup_timer_list = [x for x in next_setup_finished_time if x != inf]
                            server_choosed = next_setup_finished_time.index(max(setup_timer_list))
                            # the selected server will change from SETUP to OFF
                            server[server_choosed] = 0
                            # update the property of this server
                            next_setup_finished_time[server_choosed] = inf

            # setup_finished
            elif next_event_type == 2:
                # the server will change from SETUP to BUSY
                server[first_setup_finished_server] = 2
                # update the property of this server
                next_departure_time[first_setup_finished_server] = master_clock + buffer_content[0][1]
                arrival_time_next_departure[first_setup_finished_server] = buffer_content[0][0]
                next_setup_finished_time[first_setup_finished_server] = inf
                # take a MARKED job oﬀ the queue
                buffer_content = buffer_content[1:]
                queue_length -= 1
            # delayedoff expiried
            else:
                # the server will change from DELAYEDOFF to OFF
                server[first_delayedoff_expiried_server] = 0
                # the selected server will cancel its countdown timer
                next_delayedoff_expiried_time[first_delayedoff_expiried_server] = inf
            """
            if len(buffer_content)>0:
                print("t={}          {}            {}".format(master_clock,buffer_content[0],server))
                for i in range(1, len(buffer_content)):
                    print("                {}".format(buffer_content[i]))
            else:
                print("t={}          {}                               {}".format(master_clock,buffer_content,server))
            """
        # Write the output files
        avg_response_time = response_time_cumulative/num_customer_served
        response_file = open('mrt_'+str(test_index)+'.txt','w')
        response_file.write(str("%.3f" % round(avg_response_time,3))+'\n')
        response_file.close()

        departure_file = open('departure_'+str(test_index)+'.txt','w')
        for i in range(0, len(departure_time)):
            departure_file.write(str("%.3f" % round(arrival_time_departure[i],3))+'   '+str("%.3f" % round(departure_time[i],3))+'\n')
        departure_file.close()
