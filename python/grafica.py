import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from scipy.signal import detrend
import seaborn as sns
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.stats import mannwhitneyu

#################################
#######VIENTO####################
#################################

Vuru = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/uru-dem_agrup.csv', index_col=0, parse_dates=True,na_values='-99')
Varg = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/arg-dem_agrup.csv', header=None, delimiter=',', na_values='-99')
print(Varg[1])
fig, ax = plt.subplots(1,1,figsize=(6.5,3))

ax.plot(Varg.index, Varg[1], color='#A1140B')
plt.show()
