import random
import simpy
from datetime import datetime
import numpy as np
import sys

T_end = 5000
INTERVAL_CUSTOMERS = 0.9  # Generate new customers per x seconds

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


def simulate(n):
    
    # Setup and start the simulation
    random.seed(datetime.now())
    env = simpy.Environment()

    # Start processes and run
    counter = simpy.Resource(env, capacity=n)
    env.process(source(env, INTERVAL_CUSTOMERS, counter))
    env.run()

mean_wait_list = []
conf = 10
runs = 0
while conf > 0.1 or runs <= 100:
    wait_times = []
    simulate(1)

    mean_wait = np.mean(wait_times)
    mean_wait_list.append(mean_wait)
    conf = 1.96 * np.std(mean_wait_list) / np.sqrt(len(mean_wait_list))
    print(mean_wait, conf, len(mean_wait_list))
    runs += 1

#print(mean_wait_list)
print(runs)
print(np.mean(mean_wait_list))