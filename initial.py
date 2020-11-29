import random
import simpy
from datetime import datetime
import numpy as np
import sys
import csv

T_end = 5000
#INTERVAL_CUSTOMERS = 0.9 # Generate new customers per x seconds
lambda_list = [0.8]
n_list = [1]

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

        tib = np.random.exponential(1.0 / mu)
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

time_to_mean_list = []
for lambd in lambda_list:
    for n in n_list:
        for i in range(100):
            wait_times = []
            simulate(n, lambd)

            time_to_mean = 0
            for wait_time in wait_times:
                if wait_time >= np.mean(wait_times):
                    break
                time_to_mean += 1
            time_to_mean_list.append(time_to_mean)
            print(len(wait_times))

            mean_wait = np.mean(wait_times)
            std_wait = np.std(wait_times)
            conf = 1.96 * np.std(wait_times) / np.sqrt(len(wait_times))

        # print(wait_times)
        # print(len(wait_times))
        # print(time_to_mean)
        # print(mean_wait)
        print(np.mean(time_to_mean_list))

        # with open('initial.csv', 'a') as csv_file:
        #     writer = csv.writer(csv_file, delimiter=';')
        #     writer.writerow([n, lambd, runs, mean, std, 1.96*std/np.sqrt(runs)])
