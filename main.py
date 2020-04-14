'''this file holds the structure for the simulation of a radiology department
authors: '''

from radiology_functions import simulate
from datetime import datetime

first = datetime.now()
simulate()
second = datetime.now()
run_time = second - first
print("Run Time in microseconds =", run_time.microseconds)

