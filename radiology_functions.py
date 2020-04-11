'''this file contains the methods and event functions in order to simulate a radiology department
authors:
'''

import math
import numpy as np
import pandas as pd

#define global variables
event_queue = pd.DataFrame({"job ID", "time"})


#define classes
class Job:
    global counter

    def _init_(self, patient, clock):
        counter += 1
        self.ID = counter
        self.departure_time = 0
        self.arrival_time = clock
        self.location
        if patient:
            r = np.random.uniform(0, 1)
            if 0<r<=0.2:
                self.type = 1
            elif 0.2<r<=0.4:
                self.type = 2
            elif 0.4<r<=0.5:
                self.type = 3
            else:
                self.type = 4
        else:
            r = np.random.uniform(0, 1)
            if 0<r<=0.4:
                self.type = 2
            else:
                self.type = 4
        self.route

class Station:
    def _init_(self, servers):
        self.queue = list()
        self.servers = servers
        self.servers_busy = 0



def Exponential_distribution(lambdaValue):
    j1 = np.random.uniform(0, 1)
    if (j1 == 0): j1 += 0.0001
    j2 = -math.log(j1) / lambdaValue
    return j2


def Normal_distribution(mean, stdev):
    # TO MODEL BASED ON CUMULATIVE DENSITY FUNCTION OF NORMAL DISTRIBUTION BASED ON BOOK OF SHELDON ROSS, Simulation, The polar method, p80.

    t = 0
    while (t >= 1 or t == 0):
        r1 = np.random.uniform(0, 1) * 2 - 1  # randomNumber 1
        r2 = np.random.uniform(0, 1) * 2 - 1
        t = r1 * r1 + r2 * r2

    multiplier = math.sqrt(-2 * math.log(t) / t)
    x = r1 * multiplier * stdev + mean
    return x

def arrival():


def departure():

