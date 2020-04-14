'''this file contains the methods and event functions in order to simulate a radiology department
authors:
'''

import math
import numpy as np
import pandas as pd

# DEFINE GLOBAL VARIABLES

event_queue = pd.DataFrame({"job": [], "time": [], "type": []})
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
            location        :current location of the job (Station)
            :type           :type of job (X-ray, PET, CT, MRI as int: 1,2,3,4)
            route           :stations left to visit (tuple of int)
    """

    # the initialisation will assign a unique id and determine type and routes. The method requires patient (boolean)
    # to determine whether the job comes from a patient (=True) or from another department (= False) and sets arrival
    # time of the job to the current clock
    def __init__(self, patient, arrival_time):
        global counter
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

    def update_location(self,station):
        self.location = station



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

    def is_free(self):
        if len(self.queue) > 0:
            return(False)
        else:
            for server in self.serverlist:
                if server.current_job == None:
                    return(True)
            return(False)

    def add_to_queue(self,job):
        self.queue = self.queue.append(job)


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
        t_a1 = clock + exponential_distribution(0.25) * 60  # interarrival rate = 0.25; arrival rate = 1/0.25 = 4
        t_a2 = clock + exponential_distribution(1) * 60  # interarrival rate = 1; arrival rate = 1/1 = 1
        newjob1 = Job(True, t_a1)
        newjob2 = Job(False, t_a2)
        add = pd.DataFrame({"job": [newjob1, newjob2], "time": [newjob1.arrival_time, newjob2.arrival_time],
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
        {"job": newjob, "time": newjob.arrival_time,
         "type": 'arrival'}, ignore_index=True)


def create_departure_event(job):
    """
    this method creates a departure event and updates the server busy time based on the jobtype of the passed job
    object. It also applies the depart method for the given job.
    variables:
                job         :the job for which a departure event needs to be created (Job)

    """

    global event_queue, clock
    station = job.location  # we use the location attribute to determine where the job currently is
    current_station = str(station.id)
    job_type = job.type
    distr = Processing_Times_Prob[current_station].iloc[job_type - 1]
    mu = distr[0]
    sigma = math.sqrt(distr[1])
    process_time = normal_distributions(mu, sigma)
    job.process_time += process_time
    job.depart()
    for server in station.serverlist:
        if job.id == server.current_job:
            server.busy_time += process_time
    departure_time = process_time + clock
    event_queue = event_queue.append({"job": job.id, "time": departure_time, "type": 'departure'},
                                     ignore_index=True)


def get_next_event():
    global event_queue
    return event_queue[0]


def update_clock():
    global event_queue, clock
    event_queue = event_queue.sort_values(by=["time"], ignore_index=True)
    clock = event_queue.loc[0, "time"]


def departure():
    nikske = None


def simulate(*kwargs):
    """
    this function implements all the functions above in order to correctly simulate the workings of a radiology
    department
    """
    global event_queue
    global clock
    global counter
    number_of_runs = 1
    for run in range(0,number_of_runs):
        # set parameters = 0
        clock = 0
        counter = 0
        event_queue = event_queue.iloc[0:0]

        # Create stations
        station_1 = Station(3, 1)
        station_2 = Station(2, 2)
        station_3 = Station(4, 3)
        station_4 = Station(3, 4)
        station_5 = Station(1, 5)
        stations = [station_1, station_2, station_3, station_4, station_5]

        # generate first arrivals
        generate_arrival(True)  # true or false makes no difference (it's the first arrival)

        while(clock < 1): #depending on stop criterium



            # look in the event_queue what the next  event will be
            event_queue = event_queue[event_queue["time"]>clock]
            current_time = event_queue["time"].min()

            #update clock
            clock = current_time

            #determine current job
            current_row = event_queue[event_queue["time"] == current_time]
            current_job = current_row.job
            index = current_job.index
            current_job = current_job[index[0]]
            current_type = current_row.type
            current_type = current_type[index[0]]

            #check event type
            if current_type == "arrival":

                #is there a not completed station?

                if current_job.stops_remaining() > 0:

                    #Current_job is not done yet!

                    #What is the next station?
                    current_station_id = current_job.next_stop() #je krijgt de id , mss stations in de dict steken?
                    for station in stations:
                        if(station.id == current_station_id):
                            current_station = station

                    #Is the next station free?

                    if(current_station.is_free()):
                        print("station is free")

                        #update location of job
                        current_job.update_location(current_station)

                        #Create departure event
                        create_departure_event(current_job)

                        ##TO DO: SERVERS updaten, momenteel heeft een job een location (station)
                        #maar als je kijkt in de station => server zijn die nog steeds leeg!

                        print("departure event done")
                    else:
                        print("Station is not free")
                        current_station.add_to_queue(current_job)


                else:
                    #job is finised
                    print("finished")

                    #euhhh wuk doenwe hier?

                #end criterium met?
                #if(end_criterium_met()):
                    #generate_arrival()
                    #update/sort_event_queue()



            else:
                print("tis een departure")
                #departure handling









