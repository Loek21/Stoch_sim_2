# Queueing simulations
This repository contains several files for different simulations:
- fifo.py contains a simulation for several, system loads, number of servers for a FIFO queueing system with exponential distributions for arrival and service rates.
- priority.py contains a simulation for several, system loads, number of servers for a priority queueing system based on shortest jobs first with exponential distributions for arrival and service rates.
- longtail.py contains a simulation for several, system loads, number of servers for a FIFO queueing system with exponential distributions for arrival and a hyperexponential distribution for service rates.
- deterministic.py contains a simulation for several, system loads, number of servers for a FIFO queueing system with exponential distributions for arrival and a deterministic distribution for service rates.
- convergence.py shows the covergence of the mean waiting time for a FIFO queueing system with 1 server and a system load of 0.9.

All files produce a csv file containing the: number of servers, arrival rate, required runs to attain desired confidence radius, mean, std and confidence radius. Theses values can later be used for analysis.

Authors:
-Loek van Steijn
-Sebastiaan Kruize
