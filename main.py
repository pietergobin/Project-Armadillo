'''this file holds the structure for the simulation of a radiology department
authors: '''

from radiology_functions import simulate

name = "(3,3) "
min, max = 3,3
simulate(name+' comparative upgrade',servers_of_2=min, servers_of_5=min, upgrade=1,number_of_runs=32, number_of_jobs=1000)
simulate(name+'comparative new',servers_of_2=max, servers_of_5=min, upgrade=2,number_of_runs=32, number_of_jobs=1000)

