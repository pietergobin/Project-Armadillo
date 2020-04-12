'''this file holds the structure for the simulation of a radiology department
authors: '''
import radiology_functions as f


#initialise objects
f.clock = 0

Station_1 = f.Station(3,1)
f.generate_arrival(True)
event_queue = f.event_queue
print(event_queue)

