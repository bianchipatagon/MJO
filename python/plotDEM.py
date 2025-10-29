import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
# ~ import pymannkendall as mk
import seaborn as sns
from scipy import stats
from datetime import datetime

## demanda
demarg = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/arg-dem.txt', header=None, delimiter=';', na_values='-99')
demuru = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/uru-dem.txt', header=None, delimiter=';', na_values='-99')
demchi = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/chi-dem3.txt', header=None, delimiter=';', na_values='-99')


demarg.index= pd.date_range(start='2007-01-01', end='2022-12-31', freq = 'D')
demuru.index= pd.date_range(start='2011-01-01', end='2022-12-31', freq = 'D')
demchi.index= pd.date_range(start='2016-01-01', end='2022-12-31', freq = 'D')
print(demarg)

fig,(ax1,ax2,ax3) = plt.subplots(3, 1,figsize=(14,6),sharex=True)

ax1.plot(demarg[3]*1000, linewidth=1, color = 'mediumblue')
ax1.tick_params(labelsize=14)
ax1.xaxis.set_tick_params(length=0)

ax2.plot(demuru[3], linewidth=1, color = 'lightblue')
ax2.tick_params(labelsize=14)
ax2.set_ylabel('Power [MWh]', fontsize = 14)
ax2.xaxis.set_tick_params(length=0)

ax3.plot(demchi[3], linewidth=1, color = 'crimson')
ax3.tick_params(labelsize=14)
ax3.set_xlim([datetime(2007, 1, 1), datetime(2022, 12, 31)])

fig.text(0.15, 0.82, 'Argentina', fontsize = 15, color = 'mediumblue',fontweight='bold')
fig.text(0.15, 0.57, 'Uruguay', fontsize = 15, color = 'lightblue',fontweight='bold')
fig.text(0.15, 0.3, 'Chile', fontsize = 15, color = 'crimson',fontweight='bold')
fig.subplots_adjust(hspace=0.1)
plt.savefig('/home/emi/Documents/MJO/imagenes/DEMplot.jpg', dpi=300, bbox_inches="tight")

# ~ plt.show()
