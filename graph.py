import matplotlib.pyplot as plt 
import csv
import numpy as np

#### For the convergence in T ####

# save the data
T_list = []
T_data = []
T_std = []

# get data from csv file
with open('resultstime.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        T_list.append(float(row[0]))
        T_data.append(float(row[2]))
        T_std.append(float(row[3]))

# create the confidence intervals as errors
T_max = list(np.array(T_data) + np.array(T_std))
T_min = list(np.array(T_data) - np.array(T_std))

# plot figure
fig, ax3 = plt.subplots()
ax3.semilogx(T_list, T_data)
ax3.fill_between(T_list, T_max, T_min, alpha=0.3)
ax3.set_ylabel('Mean waiting time')
ax3.set_xlabel('Max T')
ax3.set_title('Mean waiting time convergence')
plt.grid()
#plt.show()

#################################


#### For exercise 2/3 ####

# save data
rho = [0.8, 0.85, 0.9, 0.95]
n1 = []
n2 = []
n4 = []
n1_prio = []

# get data from csv file
with open('results.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        if int(row[0]) == 1:
            n1.append((float(row[3]), float(row[4]), float(row[2])))
        elif int(row[0]) == 2:
            n2.append((float(row[3]), float(row[4]), float(row[2])))
        else:
            n4.append((float(row[3]), float(row[4]), float(row[2])))

# get the data for exercise 3, priority queue
with open('ex3results.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        n1_prio.append((float(row[3]), float(row[4]), float(row[2])))

# plot data
fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax1.plot(rho, [x[0] for x in n1], label='1 server')
ax1.fill_between(rho, [x[0]+x[1] for x in n1], [x[0]-x[1] for x in n1], alpha=0.3)
ax1.plot(rho, [x[0] for x in n2], label='2 servers')
ax1.fill_between(rho, [x[0]+x[1] for x in n2], [x[0]-x[1] for x in n2], alpha=0.3)
ax1.plot(rho, [x[0] for x in n4], label='4 servers')
ax1.fill_between(rho, [x[0]+x[1] for x in n4], [x[0]-x[1] for x in n4], alpha=0.3)
ax1.plot(rho, [x[0] for x in n1_prio], label='1 server (prio)')
ax1.fill_between(rho, [x[0]+x[1] for x in n1_prio], [x[0]-x[1] for x in n1_prio], alpha=0.3)
ax1.grid()
ax1.set_title('.', color='white')
ax1.set_xlabel('ρ')
ax1.set_ylabel('Mean waiting time')
ax1.legend(loc='upper left')
ax2 = fig.add_subplot(1,2,2)
ax2.semilogy(rho, [x[2] for x in n1])
ax2.semilogy(rho, [x[2] for x in n2])
ax2.semilogy(rho, [x[2] for x in n4])
ax2.semilogy(rho, [x[2] for x in n1_prio])
ax2.grid()
ax2.set_xlabel('ρ')
ax2.set_ylabel('Measurements')
plt.tight_layout()
plt.suptitle('Server capacity and queuing method comparison', y=0.97)
plt.show()

########################

#### Exercise 4 ####

# first get the new data for the deterministic and longtail queues for rho=0.9

# save data
rho = [0.8, 0.85, 0.9, 0.95]
longtail = []
deterministic = []

# get data from csv file
with open('ex4results_longtail.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        if float(row[1]) == 0.9:
            longtail.append((float(row[3]), float(row[4])))

with open('ex4results_deterministic.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        if float(row[1]) == 0.9:
            deterministic.append((float(row[3]), float(row[4])))

# get previous data from exercise 2 into correct form for new plot
new_data = [n1[2][:2], n2[2][:2], n4[2][:2]]
servers = [1,2,4]

# plot data
fig = plt.figure()
ax4 = fig.add_subplot(1,1,1)
ax4.plot(servers, [x[0] for x in new_data], label='Exponential')
ax4.fill_between(servers, [x[0]+x[1] for x in new_data], [x[0]-x[1] for x in new_data], alpha=0.3)
ax4.plot(servers, [x[0] for x in deterministic], label='Deterministic')
ax4.fill_between(servers, [x[0]+x[1] for x in deterministic], [x[0]-x[1] for x in deterministic], alpha=0.3)
ax4.plot(servers, [x[0] for x in longtail], label='Hyperexponential')
ax4.fill_between(servers, [x[0]+x[1] for x in longtail], [x[0]-x[1] for x in longtail], alpha=0.3)
ax4.grid()
ax4.set_xlabel('n Servers')
ax4.set_xticks([1, 2, 3, 4])
ax4.set_ylabel('Mean waiting time')
ax4.legend(loc='upper right')
ax4.set_title('Service rate distribution comparison')
plt.show()

