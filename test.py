import pandas as pd


event_queue = pd.DataFrame({"job ID": [1,2], "time": [5,7], "type": ["a","d"]})

time = event_queue["time"].min()
current_job = event_queue[event_queue["time"]==time]
current_job = (current_job["job ID"])
print(current_job[0])
