import numpy as np
import queue
import copy
import matplotlib.pyplot as plt

#Parameters
lambda_ = 1.8
mu_1 = 1
mu_2 = 2
time_horizon = 5000 #seconds

#random seed
np.random.seed(10)

#Initialize Parameters
qu1 = queue.Queue() #station1 
qu2 = queue.Queue() #station2
station_1_server1_current_customer = None
station_1_server2_current_customer = None
station_2_current_customer = None
wait_time_1 = [] #wait time sequence of station1
wait_time_2 = [] #wait time sequence of station2
station1_server1_busy = False
station1_server2_busy = False
station2_server_busy = False
list_wait = []
list_system_time = []
customers_served_num = 0 #number of customers servedustomers
next_station1_arrive = np.random.exponential(1/lambda_) 
next_station1_server1_finish = np.inf
next_station1_server2_finish = np.inf
next_station2_finish = np.inf
clock = 0

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
        if not station1_server1_busy and not qu1.empty():
            station_1_server1_current_customer = qu1.get()
            station1_server1_busy = True
            next_station1_server1_finish = clock + np.random.exponential(1/mu_1)
        if not station1_server2_busy and not qu1.empty():
            station_1_server2_current_customer = qu1.get()
            station1_server2_busy = True
            next_station1_server2_finish = clock + np.random.exponential(1/mu_1)
        if not station1_server1_busy and qu1.empty():
            next_station1_server1_finish = np.inf
        if not station1_server2_busy and qu1.empty():
            next_station1_server2_finish = np.inf
        next_station1_arrive = clock + np.random.exponential(1/lambda_)
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
            next_station1_server1_finish = clock + np.random.exponential(1/mu_1)
        else:
            next_station1_server1_finish = np.inf
        qu2.put(i)
        if not station2_server_busy and not qu2.empty():
            station_2_current_customer = qu2.get()
            station2_server_busy = True
            next_station2_finish = clock + np.random.exponential(1/mu_2)
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
            next_station1_server2_finish = clock + np.random.exponential(1/mu_1)
        else:
            next_station1_server2_finish = np.inf
        qu2.put(i)
        if not station2_server_busy and not qu2.empty():
            station_2_current_customer = qu2.get()
            station2_server_busy = True
            next_station2_finish = clock + np.random.exponential(1/mu_2)
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
            next_station2_finish = clock + np.random.exponential(1/mu_2)
        else:
            next_station2_finish = np.inf
    last_event_time = clock

wait_time = np.array(wait_time_1 + wait_time_2)

plt.plot(range(len(wait_time)),wait_time)
plt.show()

    # sum_wait = 0
    # sum_system_time = 0

#     wait_time = list(np.array(wait_time_1)+np.array(wait_time_2))
#     service_time = list(np.array(x_1_copy)+np.array(x_2_copy))

#     for i in range(customers_served_num):
#         sum_wait = sum_wait + wait_time[i]
#         sum_system_time = sum_system_time + wait_time[i] + service_time[i]
    
#     if customers_served_num == 0:
#         list_wait.append(0)
#         list_system_time.append(0)
#     else:
#         list_wait.append(sum_wait/(customers_served_num))
#         list_system_time.append(sum_system_time/(customers_served_num))

# plt.plot([i+1 for i in range(time_horizon)],list_wait)
# plt.ylabel("Avg Wait Time")
# plt.show()

# plt.plot([i+1 for i in range(time_horizon)],list_system_time)
# plt.ylabel("Avg System Time")
# plt.show()

#key metrics:
# total_wait_time = list(np.array(wait_time_1)+np.array(wait_time_2))
# print("Customers' wait time is:",total_wait_time)
# system_time = list(np.array(total_wait_time)+np.array(x_1_copy)+np.array(x_2_copy))
# print("Customers' system_time is:",system_time)



    
    


        




