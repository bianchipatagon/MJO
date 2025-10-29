import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
# ~ import pymannkendall as mk
import seaborn as sns
from scipy import stats
from datetime import datetime

## demanda
metod = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/metod.txt', header=None, delimiter=',', na_values='-99')
# ~ demuru = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/uru-dem.txt', header=None, delimiter=';', na_values='-99')
# ~ demchi = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/chi-dem3.txt', header=None, delimiter=';', na_values='-99')


metod.index= pd.date_range(start='2016-01-01', end='2022-12-31', freq = 'D')
print(metod)
fig,ax = plt.subplots(1, 1,figsize=(10,2),sharex=True)

ax.plot(metod[1]*1000, linewidth=1.5, color = 'mediumblue')
ax.tick_params(labelsize=14)
# ~ ax.xaxis.set_tick_params(length=0)
ax.set_ylabel('Power [MWh]', fontsize = 14)
ax.set_xlim([datetime(2020, 1, 1), datetime(2022, 12, 31)])
ax.tick_params(axis='x', labelrotation = 90)

# ~ ax2.plot(metod[1]*1000, linewidth=1.5, color = 'lightblue')
# ~ ax2.tick_params(labelsize=14)
# ~ ax2.set_ylabel('Power [MWh]', fontsize = 14)
# ~ ax2.xaxis.set_tick_params(length=0)
# ~ ax2.set_xlim([datetime(2020, 1, 1), datetime(2022, 12, 31)])

# ~ ax3.plot(demchi[3], linewidth=1, color = 'crimson')
# ~ ax3.tick_params(labelsize=14)
# ~ ax3.set_xlim([datetime(2007, 1, 1), datetime(2022, 12, 31)])

# ~ fig.text(0.15, 0.82, 'Argentina', fontsize = 15, color = 'mediumblue',fontweight='bold')
# ~ fig.text(0.15, 0.57, 'Uruguay', fontsize = 15, color = 'lightblue',fontweight='bold')
# ~ fig.text(0.15, 0.3, 'Chile', fontsize = 15, color = 'crimson',fontweight='bold')
fig.subplots_adjust(hspace=0.1)
plt.savefig('/home/emi/Documents/MJO/imagenes/filtro.jpg', dpi=300, bbox_inches="tight")

# ~ plt.show()
