'''this file contains the methods and event functions in order to simulate a radiology department
authors:
'''

import math
import numpy as np
import pandas as pd

# DEFINE GLOBAL VARIABLES

event_queue = pd.DataFrame({"job ID": [], "time": [], "type": []})
counter = 0
clock = 0
routes = {1: (3, 1, 2, 5), 2: (4, 1, 3), 3: (2, 5, 1, 4, 3), 4: (2, 4, 5)}
Processing_Times_Prob = pd.DataFrame({"Job_Type": [1, 2, 3, 4], "1": [[12, 2], [15, 2], [15, 3], [0, 0]]
                                         , "2": [[20, 4], [0, 0], [21, 3], [18, 3]]
                                         , "3": [[16, 4], [14, 2], [10, 1], [0, 0]]
                                         , "4": [[0, 0], [20, 3], [24, 4], [13, 2]]
                                         , "5": [[25, 5], [0, 0], [20, 3], [25, 5]]})

Efficiency_Improvement = pd.DataFrame({"Job_Type": [1, 2, 3, 4], "Current": [[25, 5], [0, 0], [20, 3], [25, 5]]
                                          , "Upgrade": [[20, 5], [0, 0], [20, 3], [20, 5]]
                                          , "New_System": [[17, 4], [0, 0], [15, 3], [16, 4]]})


# DEFINE CLASSES

class Job:
    """ this class has as attributes:
            id              :a unique ID (int)
            patient         :stores whether job arrived from a patient or from another department (boolean)
            departure_time  :system departure time (float)
            arrival_time    :system arrival time (float)
            process type    :time spent being processed (not in queue)
            location        :current location of the job (int for the relevant station)
            :type           :type of job (X-ray, PET, CT, MRI as int: 1,2,3,4)
            route           :stations left to visit (tuple of int)
    """

    # the initialisation will assign a unique id and determine type and routes. The method requires patient (boolean)
    # to determine whether the job comes from a patient (=True) or from another department (= False) and sets arrival
    # time of the job to the current clock
    def __init__(self, patient, arrival_time):
        global counter, clock
        counter += 1
        self.id = counter
        self.patient = patient
        self.departure_time = float("inf")
        self.arrival_time = arrival_time
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

    # this method gets the next stop in the route of the job
    def next_stop(self):
        return self.route[0]

    # departure event handling: this method pops the first element of the route tuple, returns True if after
    # departing there are still stations in the route tuple
    def depart(self):
        self.route = self.route[1:]
        return len(self.route) > 0

    # method returns amount of stops remaining
    def stops_remaining(self):
        return len(self.route)


class Server:
    """
    this class has attributes
        busy_time       :total busy time of the server (float)
        current_job     :the job.id of the job currently being processed
    """
    def __init__(self):
        self.busy_time = 0.0
        self.current_job = None


class Station:
    """ this class has as attributes:

                id              :a unique ID (int)
                servers         :a dataframe that shows which servers in that station are busy
                                and which job each server is processing (df)
                queue           :this list contains all jobs that are in the queue of a certain station (list)

        """

    def __init__(self, number_of_servers, id):
        self.id = id
        self.serverlist = []
        for s in range(0, number_of_servers):
            self.serverlist.append(Server())
        self.queue = list()  # contains the jobs who are in queue


    def update_departure_time(self, job):
        """
        this method creates a departure event and updates the server busy time based on the jobtype of the passed job
        object
        variable: job :the job for which a departure event needs to be created (Job)
        """

        global event_queue, clock
        current_station = str(self.id)
        job_type = job.type
        distr = Processing_Times_Prob[current_station].iloc[job_type - 1]
        mu = distr[0]
        sigma = math.sqrt(distr[1])
        process_time = normal_distributions(mu, sigma)
        job.process_time += process_time
        for server in self.serverlist:
            if job.id == server.current_job:
                server.busy_time += process_time
        departure_time = process_time + clock
        event_queue = event_queue.append({"job ID": job.id, "time": departure_time, "type": 'departure'},
                                         ignore_index=True)


# DEFINE DISTRIBUTIONS


def exponential_distribution(lambdaValue):
    j1 = np.random.uniform(0, 1)
    if (j1 == 0): j1 += 0.0001
    j2 = -math.log(j1) / lambdaValue
    return j2


def normal_distributions(mean, stdev):
    # TO MODEL BASED ON CUMULATIVE DENSITY FUNCTION OF NORMAL DISTRIBUTION BASED ON BOOK OF SHELDON ROSS, Simulation,
    # The polar method, p80.

    t = 0
    while t >= 1 or t == 0:
        r1 = np.random.uniform(0, 1) * 2 - 1  # randomNumber 1
        r2 = np.random.uniform(0, 1) * 2 - 1
        t = r1 * r1 + r2 * r2

    multiplier = math.sqrt(-2 * math.log(t) / t)
    x = r1 * multiplier * stdev + mean
    return x


# DEFINE METHODS FOR PROGRAM FLOW


def generate_arrival(patient):
    """
    this generates the next two arrivals if the event queue is empty, otherwise it generates the next arrival
    according to whether the next arrival comes from a patient arriving or another department
    variable:   patient: whether the next arrival is a patient or from another department (boolean)
    """
    global clock, event_queue
    if event_queue.empty:  # generate first arrivals
        t_a1 = clock + exponential_distribution(1 / 0.25) * 60  # interarrival rate = 0.25; arrival rate = 1/0.25 = 4
        t_a2 = clock + exponential_distribution(1) * 60  # interarrival rate = 1; arrival rate = 1/1 = 1
        newjob1 = Job(True, t_a1)
        newjob2 = Job(False, t_a2)
        add = pd.DataFrame({"job ID": [newjob1.id, newjob2.id], "time": [newjob1.arrival_time, newjob2.arrival_time],
                            "type": ['arrival', 'arrival']})
        event_queue = event_queue.append(add, ignore_index=True)
        return
    elif patient:  # generate new patient arrival
        t_a = clock + exponential_distribution(1 / 0.25) * 60
        newjob = Job(True, t_a)
    else:  # generate other arrival
        t_a = clock + exponential_distribution(1) * 60
        newjob = Job(False, t_a)
    event_queue = event_queue.append(
        {"job ID": newjob.id, "time": newjob.arrival_time,
         "type": 'arrival'}, ignore_index=True)


def get_next_event():
    global event_queue
    return event_queue[0]


def update_clock():
    global event_queue, clock
    event_queue = event_queue.sort_values(by=["time"], ignore_index=True)
    clock = event_queue.loc[0, "time"]


def departure():
    nikske = None
