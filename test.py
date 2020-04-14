import pandas as pd
import numpy as np
import radiology_functions as f


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

            current_job = current_row["job"]
            print(current_job)
            print(type(current_job))
            current_job = current_job["job"] # DEZE CODE WERKT SOMS NIET OMDAT HET SOMS OP 0 STAAT (nog te fixen)
            current_type = current_row["type"]
            current_type = current_type["job"] #werkt soms niet

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









