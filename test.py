'''this file contains the methods and event functions in order to simulate a radiology department
authors:
'''

import math
import numpy as np
import pandas as pd

#define global variables
event_queue = pd.DataFrame({"job ID", "time"})
counter = 0
routes = {1:(3,1,2,5),2:(4,1,3),3:(2,5,1,4,3), 4:(2,4,5)}

#define classes
class Job:

    def __init__(self, patient, clock):
        global counter
        counter += 1
        self.ID = counter
        self.departure_time = float("inf")
        self.arrival_time = clock
        self.location = None
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
        self.route = routes.get(self.type)


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
    nada = 0

def departure():
    nikske = 0


########################################################################################################

#Create dataframes

Processing_Times_Prob = pd.DataFrame({"Job_Type":[1,2,3,4],"1":[[12,2],[15,2],[15,3],[0,0]]
                                         ,"2":[[20,4],[0,0],[21,3],[18,3]]
                                         ,"3":[[16,4],[14,2],[10,1],[0,0]]
                                         ,"4":[[0,0],[20,3],[24,4],[13,2]]
                                         ,"5":[[25,5],[0,0],[20,3],[25,5]]})

print(Processing_Times_Prob)

Effiency_Improvement = pd.DataFrame({"Job_Type":[1,2,3,4],"Current":[[25,5],[0,0],[20,3],[25,5]]
                                        ,"Upgrade":[[20,5],[0,0],[20,3],[20,5]]
                                        ,"New_System":[[17,4],[0,0],[15,3],[16,4]]})
print(Effiency_Improvement)

class Station:
    def _init_(self, number_of_servers, id):
        self.id = id
        self.servers = pd.DataFrame(columns=["busy_time","current_job"])
        for server in number_of_servers:
            self.servers.append({"busy_time":None,"current_job":None})
        self.queue = list() #contains the jobs who are in queue


    def Update_Departure_Time(self, job):
        current_station = str(self.id)
        job_type = job.type
        distr = Processing_Times_Prob[current_station].values(job_type - 1)
        mu = distr[0]
        sigma = math.sqrt(distr[1])
        process_time = Normal_distribution(mu, sigma)
        job.process_time += process_time










