'''this file holds the structure for the simulation of a radiology department
authors: '''

from radiology_functions import simulate

simulate('testing', servers_of_2=2, servers_of_5=1, upgrade=0,handle_remaining_jobs=False, export_jobs=True,number_of_runs=10, number_of_jobs=1000)


