
from radiology_functions import simulate

for i in range(1,5):
    for j in range(1,5):
        for k in range(0,2):
            simulate('experimental design', servers_of_2=i, servers_of_5=j, upgrade=k)
            #De output wordt nu overschreven, als we de output aanpassen kunnen we dit 1 keer runnen voor alle
            #mogelijke combinaties voor de comparison design.

