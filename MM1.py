import numpy as np
import queue
import copy
import matplotlib.pyplot as plt

#Parameters
lambda_ = 200
mu = 300
rho = lambda_/mu
time_horizon = 15 #hours

np.random.seed(10)

#Initialize Parameters
qu = queue.Queue()
current_customer = None
t = [] #interarrival time sequence
x = [] #service time sequence
tau = [] #arrival time sequcece
wait_time = [] #wait time sequence
wait_time_offline = []
server_busy = False
list_wait = []
list_system_time = []
average_n_t = [] #average num of customers in the system

total_customers_num = int(np.random.poisson(lambda_) * time_horizon)
customers_served_num = 0
n_t = 0
sum_n_t = 0

#Generate interarrival time sequence
for i in range(total_customers_num):
    ti = np.random.exponential(1/lambda_)*60*60
    if i==0:
        t.append(0)
    else:
        t.append(int(ti - ti%1)) #make sure that event happen in integer second

#Generate service time sequence
while not len(x) == total_customers_num:
    xi = np.random.exponential(1/mu)*60*60
    if not int(xi - xi%1) < 1:
        x.append(int(xi - xi%1))

x_copy = copy.deepcopy(x)

#Generate arrival time sequence
for i in range(total_customers_num):
    if i == 0:
        tau.append(0)
    else:
        tau.append(tau[i-1] + t[i])
    wait_time.append(0)

#Compute waiting time offline sequence
# for i in range(total_customers_num):
#     if i==0:
#         wait_time_offline.append(0)
#     else:
#         wait_time_offline.append(np.maximum((wait_time_offline[i-1]+x[i-1]-t[i]),0))

#Start to simulate the M/M/1 Queueing System
for i in range(time_horizon*60*60):
    if server_busy:
        for item in list(qu.queue):
            wait_time[item] = wait_time[item] + 1
        x[current_customer] = x[current_customer] - 1
        if x[current_customer] == 0:
            server_busy = False
            customers_served_num = customers_served_num + 1
            n_t = n_t - 1
            n_t_state = n_t

    for j in range(total_customers_num):
        if i == tau[j]: #customer j arrive 
            qu.put(j)
            n_t = n_t + 1
            n_t_state = n_t
    
    if not server_busy and not qu.empty():
        current_customer = qu.get() #start to serve new customer
        server_busy = True
    
    sum_wait = 0
    sum_system_time = 0
    sum_n_t = sum_n_t + n_t_state

    if i == 0:
        if tau[0] == 0: #the first customer arrive in 0 seconds
            average_n_t.append(1)
        else:
            average_n_t.append(0)
    else:
        average_n_t.append(sum_n_t/i)

    for i in range(customers_served_num):
        sum_wait = sum_wait + wait_time[i]
        sum_system_time = sum_system_time + wait_time[i] + x_copy[i]
    
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
print("Customers' wait time is:",wait_time)
system_time = list(np.array(wait_time)+np.array(x_copy))
print("Customers' system_time is:",system_time)
plt.plot(range(len(average_n_t)),average_n_t)
plt.ylabel("Avg N(t)")
plt.show()




    







    

