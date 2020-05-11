'''this file holds the structure for the simulation of a radiology department
authors: '''

from radiology_functions import simulate

name = "(2,3)"
min = 2
max = 3
simulate(name+'upgrade 32',servers_of_2=min, servers_of_5=max, upgrade=1,number_of_runs=32, number_of_jobs=1000)

