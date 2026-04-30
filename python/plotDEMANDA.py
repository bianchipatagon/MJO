import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from scipy.signal import detrend
import seaborn as sns
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, Normalize

demarg = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/demanda/hanna/arg-dem.txt', header=None, delimiter=';', na_values='-99')
demarg.index= pd.date_range(start='2007-01-01', end='2022-12-31', freq = 'D')

fig,ax = plt.subplots(1, 1,figsize=(14,6),sharex=True)

ax.plot(demarg[3], linewidth=1, color = 'mediumblue')
ax.set_ylabel('[GWh]', fontsize = 14)


plt.savefig('dem.jpg', dpi=300, bbox_inches="tight")
