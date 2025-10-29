import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from scipy.signal import detrend

uru = pd.read_csv('arg -dem-agrup.csv', header=None, delimiter=',', na_values='-99')

fig, ax = plt.subplots(figsize=(7,2), sharex= True)
 
ax.plot(uru[1])
plt.show()
