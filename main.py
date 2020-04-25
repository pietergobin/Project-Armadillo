'''this file holds the structure for the simulation of a radiology department
authors: '''

from radiology_functions import simulate

#zet u naam hier dan hebben we mooi overzicht
name = "(1,8) "
min =1
max =8
simulate(name+'screening_scenario---',servers_of_2=min, servers_of_5=min, upgrade=0,number_of_runs=32, number_of_jobs=1000)
simulate(name+'screening_scenario+--',servers_of_2=max, servers_of_5=min, upgrade=0,number_of_runs=32, number_of_jobs=1000)
simulate(name+'screening_scenario-+-',servers_of_2=min, servers_of_5=max, upgrade=0,number_of_runs=32, number_of_jobs=1000)
simulate(name+'screening_scenario++-',servers_of_2=max, servers_of_5=max, upgrade=0,number_of_runs=32, number_of_jobs=1000)
simulate(name+'screening_scenario--+',servers_of_2=min, servers_of_5=min, upgrade=2,number_of_runs=32, number_of_jobs=1000)
simulate(name+'screening_scenario+-+',servers_of_2=max, servers_of_5=min, upgrade=2,number_of_runs=32, number_of_jobs=1000)
simulate(name+'screening_scenario-++',servers_of_2=min, servers_of_5=max, upgrade=2,number_of_runs=32, number_of_jobs=1000)
simulate(name+'screening_scenario+++',servers_of_2=max, servers_of_5=max, upgrade=2,number_of_runs=32, number_of_jobs=1000)
