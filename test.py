import pandas as pd
import numpy as np

#Create dataframes

Processing_Times_Prob = pd.DataFrame({"Job_Type":[1,2,3,4],"Distribution_WS1":[[12,2],[15,2],[15,3],[0,0]]
                                         ,"Distribution_WS2":[[20,4],[0,0],[21,3],[18,3]]
                                         ,"Distribution_WS3":[[16,4],[14,2],[10,1],[0,0]]
                                         ,"Distribtuion_WS4":[[0,0],[20,3],[24,4],[13,2]]
                                         ,"Distribution_WS5":[[25,5],[0,0],[20,3],[25,5]]})

print(Processing_Times_Prob)