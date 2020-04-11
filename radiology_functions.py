'''this file contains the methods and event functions in order to simulate a radiology department
authors:
'''

import math
import numpy as np
import pandas as pd

# define global variables
event_queue = pd.DataFrame({"job ID":[], "time":[]})
counter = 0
routes = {1: (3, 1, 2, 5), 2: (4, 1, 3), 3: (2, 5, 1, 4, 3), 4: (2, 4, 5)}
Processing_Times_Prob = pd.DataFrame({"Job_Type": [1, 2, 3, 4], "Distribution_WS1": [[12, 2], [15, 2], [15, 3], [0, 0]]
                                         , "Distribution_WS2": [[20, 4], [0, 0], [21, 3], [18, 3]]
                                         , "Distribution_WS3": [[16, 4], [14, 2], [10, 1], [0, 0]]
                                         , "Distribtuion_WS4": [[0, 0], [20, 3], [24, 4], [13, 2]]
                                         , "Distribution_WS5": [[25, 5], [0, 0], [20, 3], [25, 5]]})


# define classes
class Job:
    """ this class has as attributes:
            ID              :a unique ID (int)
            departure_time  :system departure time (float)
            arrival_time    :system arrival time (float)
            location        :current location of the job (int for the relevant station)
            :type           :type of job (X-ray, PET, CT, MRI as int: 1,2,3,4)
            route           :stations left to visit (tuple of int)
    """

    # the initialisation will assign a unique id and determine type and routes
    def __init__(self, patient, clock):
        global counter
        counter += 1
        self.ID = counter
        self.departure_time = float("inf")
        self.arrival_time = float(clock)
        self.process_time = 0
        self.location = None
        if patient:
            r = np.random.uniform(0, 1)
            if 0 < r <= 0.2:
                self.type = 1
            elif 0.2 < r <= 0.4:
                self.type = 2
            elif 0.4 < r <= 0.5:
                self.type = 3
            else:
                self.type = 4
        else:
            r = np.random.uniform(0, 1)
            if 0 < r <= 0.4:
                self.type = 2
            else:
                self.type = 4
        self.route = routes.get(self.type)

    def next_stop(self):
        return self.route[0]

    def depart(self):
        self.route = self.route[1:]

    def remaining_stops(self):
        return len(self.route)





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
    nada = None


def departure():
    nikske = None
