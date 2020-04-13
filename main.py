'''this file holds the structure for the simulation of a radiology department
authors: '''

import radiology_functions as f
import pandas as pd
import numpy as np

number_of_runs = 1
for run in number_of_runs:

    #set parameters = 0
    f.clock = 0 #werkt dit met OOP, of moeten we een functie schrijven die de clock update?
    f.counter = 0 #idem als hierboven
    f.event_queue = f.event_queue.iloc[0:0] #idem als hierboven (dit cleared de event_queue)
    #Create stations
    station_1 = f.Station(3,1)
    station_2 = f.Station(2, 2)
    station_3 = f.Station(4,3)
    station_4 = f.Station(3,4)
    station_5 = f.Station(1,5)

    #generate first arrivals
    f.generate_arrival()

    #look in the event_queue what the first arrival event will be
    current_job = f.event_queue["job"].loc[f.event_queue["time"]==f.event_queue.min()]
    time = f.event_queue["time"].min()
    f.clock = time
    current_job = f.event_queue[f.event_queue["time"] == time]
    current_job = (current_job["job"])
    current_job = current_job[0]





    f.generate_arrival()


    print('successss')