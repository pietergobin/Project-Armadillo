'''this file contains the methods and event functions in order to simulate a radiology department
authors:
'''

import math
import os
from pathlib import Path

import numpy
import numpy as np
import pandas as pd
from tqdm import trange

# DEFINE GLOBAL VARIABLES

event_queue = pd.DataFrame({"job": [], "time": [], "type": []})
job_output = pd.DataFrame({"id": [], "source patient": [], "type": [],
                           "arrival time": [], "departure time": [],
                           "process time": []})
job_output = job_output.astype({"id": int, "source patient": int, "type": int, "arrival time": float,
                                "departure time": float, "process time": float})
station_output = pd.DataFrame()
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
        self.departure_time = 0
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

    def update_location(self, station):
        self.location = station

    def to_output(self):
        global job_output
        to_append = pd.DataFrame({"id": [self.id], "source patient": [self.patient], "type": [self.type],
                                  "arrival time": [self.arrival_time], "departure time": [self.departure_time],
                                  "process time": [self.process_time]})
        job_output = job_output.append(to_append)


class Server:
    """
    this class has attributes
        busy_time       :total busy time of the server (float)
        current_job     :the job currently being processed
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
        self.queue = []  # contains the jobs who are in queue

    def get_free_server(self):
        # this method returns a Server object if a server is free, otherwise it returns None

        if len(self.queue) > 0:
            return None
        else:
            for server in self.serverlist:
                if server.current_job == None:
                    return server
            return None

    def add_to_queue(self, job):
        self.queue.append(job)

    def to_output(self):
        global station_output
        count = 0
        for server in self.serverlist:
            count += 1
            station_output = station_output.append(
                {"server": 'station' + str(self.id) + 'server' + str(count), "busy time": server.busy_time},
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
        t_a1 = clock + exponential_distribution(1/(0.25 * 60))  # interarrival rate = 0.25; arrival rate = 1/0.25 = 4
        t_a2 = clock + exponential_distribution(1/60)  # interarrival rate = 1; arrival rate = 1/1 = 1
        newjob1 = Job(True, t_a1)
        newjob2 = Job(False, t_a2)
        add = pd.DataFrame({"job": [newjob1, newjob2], "time": [newjob1.arrival_time, newjob2.arrival_time],
                            "type": ['arrival', 'arrival']})
        event_queue = event_queue.append(add, ignore_index=True)
        return
    elif patient:  # generate new patient arrival
        t_a = clock + exponential_distribution(1/(0.25 * 60))
        newjob = Job(True, t_a)
    else:  # generate other arrival
        t_a = clock + exponential_distribution(1/60)
        newjob = Job(False, t_a)
    event_queue = event_queue.append(
        {"job": newjob, "time": newjob.arrival_time,
         "type": 'arrival'}, ignore_index=True)


def create_departure_event(job, upgrade):
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
    if station.id == 5 and upgrade != 0:
        if upgrade == 1:
            distr = Efficiency_Improvement['Upgrade'].iloc[job_type - 1]
        else:
            distr = Efficiency_Improvement['New_System'].iloc[job_type - 1]
    else:
        distr = Processing_Times_Prob[current_station].iloc[job_type - 1]
    mu = distr[0]
    sigma = math.sqrt(distr[1])
    process_time = normal_distributions(mu, sigma)
    job.process_time += process_time
    job.depart()
    for server in station.serverlist:
        if job == server.current_job:
            server.busy_time += process_time
    departure_time = process_time + clock
    event_queue = event_queue.append({"job": job, "time": departure_time, "type": 'departure'},
                                     ignore_index=True)


def get_next_event():
    global event_queue
    return event_queue[0]


def update_clock():
    global event_queue, clock
    event_queue = event_queue.sort_values(by=["time"], ignore_index=True)
    clock = event_queue.loc[0, "time"]


def reset_output():
    global job_output
    job_output = job_output.drop(job_output.index, inplace=True)
    job_output = pd.DataFrame({"id": [], "source patient": [], "type": [],
                               "arrival time": [], "departure time": [],
                               "process time": []})
    job_output = job_output.astype({"id": int, "source patient": int, "type": int, "arrival time": float,
                                    "departure time": float, "process time": float})


def departure(job, stations, upgrade):
    global event_queue, clock

    station = job.location
    for server in station.serverlist:
        if server.current_job == job:
            if len(station.queue) > 0:
                next_job = station.queue[0]
                station.queue = station.queue[1:]
                next_job.location = station
                server.current_job = next_job
                create_departure_event(next_job, upgrade)
            else:
                server.current_job = None

    if job.stops_remaining() > 0:
        # generate future arrival event to relevant station
        current_station_id = job.next_stop()
        for station in stations:
            if station.id == current_station_id:
                # Is the next station free?
                current_server = station.get_free_server()
                if current_server is not None:

                    # update location of job
                    job.update_location(station)
                    # assign to server
                    current_server.current_job = job
                    # Create departure event
                    create_departure_event(job, upgrade)

                else:
                    station.add_to_queue(job)
            else:
                continue
            break
    else:
        job.departure_time = clock
        job.to_output()


def simulate(dir_name, number_of_runs=10, servers_of_2=2, servers_of_5=1, upgrade=0, handle_remaining_jobs = True):
    """
    this function implements all the functions above in order to correctly simulate the workings of a radiology
    department
    variables:
        servers_of_2    : amount of servers for station 2
        servers_of_5    : amount of servers for station 5
        upgrade         : whether to use the upgraded system (1) or the new system (2) for station 5, default is current
                          system (0)
    """
    global event_queue, job_output
    global clock
    global counter
    CT_jobs = []
    stop = (11 * 60)
    output_path = Path("output/" + dir_name)
    output_path_runs = output_path /'runs'
    #create directories
    try:
        os.makedirs(output_path_runs, exist_ok=True)
    except OSError as error:
        print(error)


    for run in trange(number_of_runs):
        # set parameters = 0
        clock = 0
        counter = 0

        event_queue = event_queue.iloc[0:0]

        reset_output()

        # Create stations
        station_1 = Station(3, 1)
        station_2 = Station(servers_of_2, 2)
        station_3 = Station(4, 3)
        station_4 = Station(3, 4)
        station_5 = Station(servers_of_5, 5)
        stations = [station_1, station_2, station_3, station_4, station_5]

        # generate first arrivals
        generate_arrival(True)  # true or false makes no difference (it's the first arrival)

        while clock < stop:  # depending on stop criterium

            # sort event queue to determine next event
            event_queue = event_queue.sort_values("time")

            # select event job and type
            current_row = event_queue.iloc[0]
            current_job = current_row.job
            current_type = current_row.type
            # delete selected event from the queue and update the clock
            update_clock()
            event_queue = event_queue.iloc[1:]

            # check event type
            if current_type == "arrival":

                # is there a not completed station?

                if current_job.stops_remaining() > 0:

                    # Current_job is not done yet!

                    # What is the next station?
                    current_station_id = current_job.next_stop()
                    for station in stations:
                        if station.id == current_station_id:
                            # Is the next station free?
                            current_server = station.get_free_server()
                            if current_server is not None:

                                # update location of job
                                current_job.update_location(station)
                                # assign to server
                                current_server.current_job = current_job
                                # Create departure event
                                create_departure_event(current_job, upgrade)

                            else:
                                station.add_to_queue(current_job)
                        else:
                            continue
                        break
                    generate_arrival(current_job.patient)


                else:
                    # job is finished
                    current_job.departure_time = clock
                    current_job.to_output()
                    print("finished")

            else:
                # departure handling
                departure(current_job, stations, upgrade)

        if handle_remaining_jobs:
            #handle customers left in system
            event_queue = event_queue.loc[event_queue["type"] == 'departure']
            while len(event_queue)> 0:
                event_queue = event_queue.sort_values(by=["time"])
                # select event job and type
                current_row = event_queue.iloc[0]
                current_job = current_row.job
                current_type = current_row.type
                # delete selected event from the queue and update the clock
                update_clock()
                event_queue = event_queue.iloc[1:]
                departure(current_job, stations, upgrade)
        # store cycle time of day in array
        job_output["cycle time"] = job_output["departure time"] - job_output["arrival time"]
        job_output = job_output.drop(["departure time", "arrival time"], axis = 1)

        #store average cycle time of jobs
        CT_jobs.append((job_output["cycle time"].mean()))

        # write to csv after each run
        output_job_name = output_path_runs / ('job' + str(run) + '.csv')
        job_output.reset_index()
        job_output.to_csv(output_job_name)
        # store server information in station_output
        for station in stations:
            station.to_output()

    # write server information to output
    output_station_name = output_path / 'station.csv'
    station_output.reset_index()
    station_output.to_csv(output_station_name)

    # determine mean cycle time and utilisation
    performance_file_name = output_path / 'performance.txt'
    CT = numpy.mean(CT_jobs)
    rho = station_output["busy time"].mean()/stop
    obj_function = CT - 10*rho
    with open(performance_file_name, 'w')as file:
        file.write('Mean CT; Rho; Objective function value \n '+str(CT)+"; "+str(rho)+"; "+str(obj_function))
