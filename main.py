'''this file holds the structure for the simulation of a radiology department
authors: '''

import radiology_functions as f

f.clock = 0
station_1 = f.Station(3,1)
f.generate_arrival(True)
queue = f.event_queue
print(queue)