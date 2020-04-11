import pandas as pd
import numpy as np

#Create dataframes
Type_To_Path = pd.DataFrame({"Job_Type": [1,2,3,4],"Path": [[3,1,2,5],[4,1,3],[2,5,1,4,3],[2,4,5]]})
print(Type_To_Path.head())

Processing_Times_Prob = pd.DataFrame({""})