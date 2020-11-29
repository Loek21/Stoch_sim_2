import random
import simpy
from datetime import datetime
import numpy as np
import sys
import csv

T_end = 5000
#INTERVAL_CUSTOMERS = 0.9 # Generate new customers per x seconds
lambda_list = [0.8, 0.85, 0.9, 0.95]
n_list = [1, 2, 4]

def source(env, interval, counter):
    """Source generates customers randomly"""
    k = 0
    while env.now < T_end:
        mu = 1
        c = customer(env, 'Customer%02d' % k, counter, mu)
        env.process(c)
        t = np.random.exponential(1/interval)
        k += 1
        yield env.timeout(t)


def customer(env, name, counter, mu):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    #print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        yield req

        wait = env.now - arrive
        #print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

        tib = 0.5*np.random.exponential(0.5) + 0.5*np.random.exponential(1.5)
        yield env.timeout(tib)
        #print('%7.4f %s: Finished' % (env.now, name))

    wait_times.append(wait)


def simulate(n, lambd):
    
    # Setup and start the simulation
    random.seed(datetime.now())
    env = simpy.Environment()

    # Start processes and run
    counter = simpy.Resource(env, capacity=n)
    env.process(source(env, n*lambd, counter))
    env.run()

mean_wait_list = []
conf = 10
runs = 0
for lambd in lambda_list:
    for n in n_list:
        if n == 1: 
            conf_radius = 0.09
        elif n == 2: 
            conf_radius = 0.045
        else:
            conf_radius = 0.0197
        while conf > conf_radius or runs <= 100:
            wait_times = []
            simulate(n, lambd)

            mean_wait = np.mean(wait_times)
            mean_wait_list.append(mean_wait)
            conf = 1.96 * np.std(mean_wait_list) / np.sqrt(len(mean_wait_list))
            #print(mean_wait, conf, len(mean_wait_list))
            runs += 1

        #print(mean_wait_list)
        #print(runs)
        mean = np.mean(mean_wait_list)
        std =  np.std(mean_wait_list)
        #print(np.mean(mean_wait_list), np.std(mean_wait_list))

        with open('ex4results_longtail.csv', 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow([n, lambd, runs, mean, std, 1.96*std/np.sqrt(runs)])

        mean_wait_list = []
        runs = 0
        conf = 10
