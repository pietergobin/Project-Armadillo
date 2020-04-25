'''this file holds the structure for the simulation of a radiology department
authors: '''

from radiology_functions import simulate

simulate('100runs',handle_remaining_jobs=False, export_jobs=False,number_of_runs=100, number_of_jobs=1000)


