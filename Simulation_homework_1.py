import numpy as np
import queue
import copy
import matplotlib.pyplot as plt

#Parameters
lambda_ = 1.8
mu_1 = 1
mu_2 = 2
time_horizon = 100 #hours

np.random.seed(10)

#Initialize Parameters
qu1 = queue.Queue() #station1 
qu2 = queue.Queue() #station2
station_1_server1_current_customer = None
station_1_server2_current_customer = None
station_2_current_customer = None
t_1 = [] #interarrival time sequence of station1
t_2 = [] #interarrival time sequence of station2
x_1 = [] #service time sequence of station1 
x_2 = [] #service time sequence of station2
tau_1 = [] #arrival time sequence of station1
tau_2 = [] #arrival time sequence of station2
wait_time_1 = [] #wait time sequence of station1
wait_time_2 = [] #wait time sequence of station2
station1_server1_busy = False
station1_server2_busy = False
station2_server_busy = False
list_wait = []
list_system_time = []

total_customers_num = int(np.random.poisson(lambda_) * time_horizon)
customers_served_num = 0

#Generate interarrival time sequence
for i in range(total_customers_num):
    ti = np.random.exponential(1/lambda_)*60*60
    if i==0:
        t_1.append(0)
    else:
        t_1.append(int(ti - ti%1)) #make sure that event happen in integer second

#Generate service time sequence
while not len(x_1) == total_customers_num:
    xi = np.random.exponential(1/mu_1)*60*60
    if not int(xi - xi%1) < 1:
        x_1.append(int(xi - xi%1))

#Generate service time sequence
while not len(x_2) == total_customers_num:
    xi = np.random.exponential(1/mu_2)*60*60
    if not int(xi - xi%1) < 1:
        x_2.append(int(xi - xi%1))

x_1_copy = copy.deepcopy(x_1)
x_2_copy = copy.deepcopy(x_2)

#Generate arrival time sequence
for i in range(total_customers_num):
    if i == 0:
        tau_1.append(0)
    else:
        tau_1.append(tau_1[i-1] + t_1[i])
    wait_time_1.append(0)
    wait_time_2.append(0)

#Start to simulate the Queueing System
for i in range(time_horizon*60*60):
    if station1_server1_busy and station1_server2_busy:
        for item in list(qu1.queue):
             wait_time_1[item] = wait_time_1[item] + 1
        x_1[station_1_server1_current_customer] = x_1[station_1_server1_current_customer] - 1
        x_1[station_1_server2_current_customer] = x_1[station_1_server2_current_customer] - 1
        if x_1[station_1_server1_current_customer] == 0:
            station1_server1_busy = False
            tau_2.append(i)
        if x_1[station_1_server2_current_customer] == 0:
            station1_server2_busy = False
            tau_2.append(i)
    
    for j in range(total_customers_num):
        if i == tau_1[j]: #customer j arrive 
            qu1.put(j)
    
    if  not station1_server1_busy and not qu1.empty():
        station_1_server1_current_customer = qu1.get()
        station1_server1_busy = True

    if  not station1_server2_busy and not qu1.empty():
        station_1_server2_current_customer = qu1.get()
        station1_server2_busy = True
    
    if station2_server_busy:
        for item in list(qu2.queue):
            wait_time_2[item] = wait_time_2[item] + 1
        x_2[station_2_current_customer] = x_2[station_2_current_customer] - 1
        if x_2[station_2_current_customer] == 0:
            station2_server_busy = False
            customers_served_num = customers_served_num + 1
    
    for j in range(len(tau_2)):
        if i == tau_2[j]: #customer j arrive 
            qu2.put(j)
    
    if not station2_server_busy and not qu2.empty():
        station_2_current_customer = qu2.get() #start to serve new customer
        station2_server_busy = True
    
    sum_wait = 0
    sum_system_time = 0

    wait_time = list(np.array(wait_time_1)+np.array(wait_time_2))
    service_time = list(np.array(x_1_copy)+np.array(x_2_copy))

    for i in range(customers_served_num):
        sum_wait = sum_wait + wait_time[i]
        sum_system_time = sum_system_time + wait_time[i] + service_time[i]
    
    if customers_served_num == 0:
        list_wait.append(0)
        list_system_time.append(0)
    else:
        list_wait.append(sum_wait/(customers_served_num*60*60))
        list_system_time.append(sum_system_time/(customers_served_num*60*60))

plt.plot([i+1 for i in range(time_horizon*60*60)],list_wait)
plt.ylabel("Avg Wait Time")
plt.show()

plt.plot([i+1 for i in range(time_horizon*60*60)],list_system_time)
plt.ylabel("Avg System Time")
plt.show()

#key metrics:
total_wait_time = list(np.array(wait_time_1)+np.array(wait_time_2))
print("Customers' wait time is:",total_wait_time)
system_time = list(np.array(total_wait_time)+np.array(x_1_copy)+np.array(x_2_copy))
print("Customers' system_time is:",system_time)



    
    


        




