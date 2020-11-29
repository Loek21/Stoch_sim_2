import random
import simpy
from datetime import datetime
import numpy as np
import sys
import csv

# Max simulation time, different arrival rates and number of servers
T_end = 5000
lambda_list = [0.8, 0.85, 0.9, 0.95]
n_list = [1, 2, 4]

def customer(env, counter, mu):
    """
    Customers arrive into the system after which the service time is detemined from an hyperexponential distribution.
    The time the customer has to wait in the queue is recorded.
    """
    # Gets current time
    arrive = env.now

    # requests counter position (FIFO)
    with counter.request() as req:
        yield req

        wait = env.now - arrive

        # Determines service time based on a hyperexponential distribution
        tis = 0.5*np.random.exponential(0.5) + 0.5*np.random.exponential(1.5)
        yield env.timeout(tis)

    wait_times.append(wait)


def simulate(n, lambd):
    """
    Performs the steps to carry out a single simulation
    """
    # Setup and start the simulation
    # Random seed is set to current time, so each simulation is different
    random.seed(datetime.now())
    env = simpy.Environment()

    # Start processes and run
    counter = simpy.Resource(env, capacity=n)
    env.process(source(env, n*lambd, counter))
    env.run()

# loops through all arrival rates and server numbers
mean_wait_list = []
conf = 10
runs = 0
for lambd in lambda_list:
    for n in n_list:

        # Sets desired confidence radii (1% of theoretical mean)
        if n == 1:
            conf_radius = 0.03
        elif n == 2:
            conf_radius = 0.045
        else:
            conf_radius = 0.0197

        # Performs simulations untill the desired confidence has been attained
        while conf > conf_radius or runs <= 100:
            wait_times = []
            simulate(n, lambd)

            mean_wait = np.mean(wait_times)
            mean_wait_list.append(mean_wait)
            conf = 1.96 * np.std(mean_wait_list) / np.sqrt(len(mean_wait_list))
            runs += 1

        mean = np.mean(mean_wait_list)
        std =  np.std(mean_wait_list)

        # Logs number of servers, arrival rate, required runs, mean, std and confidence
        with open('longtail.csv', 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow([n, lambd, runs, mean, std, 1.96*std/np.sqrt(runs)])

        mean_wait_list = []
        runs = 0
        conf = 10
