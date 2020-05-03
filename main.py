'''this file holds the structure for the simulation of a radiology department
authors: '''

from radiology_functions import simulate

name = "(5,2)"
min = 5
max = 2
simulate(name+'Comparative upgrade',servers_of_2=min, servers_of_5=max, upgrade=1,number_of_runs=32, number_of_jobs=1000)
simulate(name+'Comparative new',servers_of_2=min, servers_of_5=max, upgrade=2,number_of_runs=32, number_of_jobs=1000)

