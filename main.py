'''this file holds the structure for the simulation of a radiology department
authors: '''

import radiology_functions as f
import pandas as pd
import numpy as np
from datetime import datetime

first = datetime.now()
f.simulate()
second = datetime.now()
run_time = second - first
print("Run Time in microseconds =", run_time.microseconds)

