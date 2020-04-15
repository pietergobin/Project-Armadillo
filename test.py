import pandas as pd
import numpy as np
import matplotlib as plt

df = pd.read_csv("")



plt.figure(fig_size=(4,3))
plt.plot(df["run"],df["objective function"],label = "Objective_Function")
plt.title("Running Averages per day")
plt.legend(loc = "upper right")
plt.show()
