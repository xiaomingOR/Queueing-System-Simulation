import numpy as np
import queue
import copy
import matplotlib.pyplot as plt

#Parameters
lambda_ = 1.8
mu_1 = 1
mu_2 = 2
time_horizon = 10000 #seconds
exponential_serve_rate = True
average_system_time = []

for i in range(50):
    np.random.seed(i)#random seed
    #Initialize Parameters
    qu1 = queue.Queue() #station1 
    qu2 = queue.Queue() #station2
    station_1_server1_current_customer = None
    station_1_server2_current_customer = None
    station_2_current_customer = None
    arrival_time = [] #arrive time sequence 
    wait_time_1 = [] #wait time sequence of station1
    wait_time_2 = [] #wait time sequence of station2
    service_time = [] #total service time sequence of station1 and station2
    station1_server1_busy = False
    station1_server2_busy = False
    station2_server_busy = False
    customers_served_num = 0 #number of customers served 
    next_station1_arrive = np.random.exponential(1/lambda_) 
    next_station1_server1_finish = np.inf
    next_station1_server2_finish = np.inf
    next_station2_finish = np.inf
    arrival_time.append(next_station1_arrive)
    clock = 0
    last_event_time = 0

    #Start to simulate the Queueing System
    j = 0 #count num of customers in system
    while clock < time_horizon:
        next_event_time = min(next_station1_arrive,next_station1_server1_finish,next_station1_server2_finish,next_station2_finish)
        next_event = np.argmin(np.array([next_station1_arrive,next_station1_server1_finish,next_station1_server2_finish,next_station2_finish]))
        clock = next_event_time
        
        if next_event == 0:
            for item in list(qu1.queue):
                wait_time_1[item-1] = wait_time_1[item-1] + (clock-last_event_time)
            for item in list(qu2.queue):
                wait_time_2[item-1] = wait_time_2[item-1] + (clock-last_event_time)
            j = j+1
            qu1.put(j)
            wait_time_1.append(0)
            wait_time_2.append(0)
            service_time.append(0)
            if not station1_server1_busy and not qu1.empty():
                station_1_server1_current_customer = qu1.get()
                station1_server1_busy = True
                servetime = np.random.exponential(1/mu_1)
                service_time[station_1_server1_current_customer-1] = service_time[station_1_server1_current_customer-1]+servetime
                next_station1_server1_finish = clock + servetime
            if not station1_server2_busy and not qu1.empty():
                station_1_server2_current_customer = qu1.get()
                station1_server2_busy = True
                servetime = np.random.exponential(1/mu_1)
                service_time[station_1_server2_current_customer-1] = service_time[station_1_server2_current_customer-1]+servetime
                next_station1_server2_finish = clock + servetime
            if not station1_server1_busy and qu1.empty():
                next_station1_server1_finish = np.inf
            if not station1_server2_busy and qu1.empty():
                next_station1_server2_finish = np.inf
            arive_time = np.random.exponential(1/lambda_)
            next_station1_arrive = clock + arive_time
            arrival_time.append(next_station1_arrive)
        elif next_event == 1:
            i = station_1_server1_current_customer # customers finished from station1 server1
            station1_server1_busy = False
            for item in list(qu1.queue):
                wait_time_1[item-1] = wait_time_1[item-1] + (clock-last_event_time)
            for item in list(qu2.queue):
                wait_time_2[item-1] = wait_time_2[item-1] + (clock-last_event_time)
            if not qu1.empty():
                station_1_server1_current_customer = qu1.get()
                station1_server1_busy = True
                servetime = np.random.exponential(1/mu_1)
                service_time[station_1_server1_current_customer-1] = service_time[station_1_server1_current_customer-1]+servetime
                next_station1_server1_finish = clock + servetime
            else:
                next_station1_server1_finish = np.inf
            qu2.put(i)
            if not station2_server_busy and not qu2.empty():
                station_2_current_customer = qu2.get()
                station2_server_busy = True
                if exponential_serve_rate:
                    servetime = np.random.exponential(1/mu_2) #Question1
                else:
                    servetime = np.random.normal(loc=0.5,scale=0.15) #Question2
                    while servetime < 0:
                        servetime = np.random.normal(loc=0.5,scale=0.15) #make sure that servetime is nonnegative
                service_time[station_2_current_customer-1] = service_time[station_2_current_customer-1]+servetime
                next_station2_finish = clock + servetime
            if not station2_server_busy and qu2.empty():
                next_station2_finish = np.inf
        elif next_event == 2:
            station1_server2_busy = False
            i = station_1_server2_current_customer # customers finished from station1 server2
            for item in list(qu1.queue):
                wait_time_1[item-1] = wait_time_1[item-1] + (clock-last_event_time)
            for item in list(qu2.queue):
                wait_time_2[item-1] = wait_time_2[item-1] + (clock-last_event_time)
            if not qu1.empty():
                station_1_server2_current_customer = qu1.get()
                station1_server2_busy = True
                servetime = np.random.exponential(1/mu_1)
                service_time[station_1_server2_current_customer-1] = service_time[station_1_server2_current_customer-1]+servetime
                next_station1_server2_finish = clock + servetime
            else:
                next_station1_server2_finish = np.inf
            qu2.put(i)
            if not station2_server_busy and not qu2.empty():
                station_2_current_customer = qu2.get()
                station2_server_busy = True
                if exponential_serve_rate:
                    servetime = np.random.exponential(1/mu_2) #Question1
                else:
                    servetime = np.random.normal(loc=0.5,scale=0.15) #Question2
                    while servetime < 0:
                        servetime = np.random.normal(loc=0.5,scale=0.15) #make sure that servetime is nonnegative
                service_time[station_2_current_customer-1] = service_time[station_2_current_customer-1]+servetime
                next_station2_finish = clock + servetime
            if not station2_server_busy and qu2.empty():
                next_station2_finish = np.inf
        elif next_event == 3:
            station2_server_busy = False
            for item in list(qu1.queue):
                wait_time_1[item-1] = wait_time_1[item-1] + (clock-last_event_time)
            for item in list(qu2.queue):
                wait_time_2[item-1] = wait_time_2[item-1] + (clock-last_event_time)
            customers_served_num = customers_served_num + 1
            if not qu2.empty():
                station_2_current_customer = qu2.get()
                station2_server_busy = True
                if exponential_serve_rate:
                    servetime = np.random.exponential(1/mu_2) #Question1
                else:
                    servetime = np.random.normal(loc=0.5,scale=0.15) #Question2
                    while servetime < 0:
                        servetime = np.random.normal(loc=0.5,scale=0.15) #make sure that servetime is nonnegative
                service_time[station_2_current_customer-1] = service_time[station_2_current_customer-1]+servetime
                next_station2_finish = clock + servetime
            else:
                next_station2_finish = np.inf
        last_event_time = clock

    wait_time = np.array(wait_time_1) + np.array(wait_time_2)
    system_time = wait_time + np.array(service_time)
    n = min(np.where(np.array(arrival_time)>3000)[0]) #the first customer who arrives 3000 time units later
    average_system_time.append(np.mean(system_time[n:len(system_time)]))

print("The average sojourn time is:",np.mean(average_system_time))
#confidence inverval
print("The up bound of 95% CI is:",np.mean(average_system_time)+1.98*np.std(average_system_time))
print("The low bound of 95% CI is:",np.mean(average_system_time)-1.98*np.std(average_system_time))

#plot the figure of sojurn time
plt.figure()
plt.hist(average_system_time)
plt.xlabel('Customer sojourn time')
plt.ylabel('Number of experiments')
plt.savefig(f'./exponential_{exponential_serve_rate}_sojurn_time_different_seed',dpi=500)





    
    


        




