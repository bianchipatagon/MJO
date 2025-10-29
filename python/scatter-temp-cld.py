import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
# ~ import pymannkendall as mk
import seaborn as sns
from scipy import stats
import pickle

## temperatura
temparg = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/temp-arg.txt', header=None, delimiter=';', na_values='-99')
tempuru = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/temp-uru.txt', header=None, delimiter=';', na_values='-99')
tempchi = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/temp-chi.txt', header=None, delimiter=';', na_values='-99')

## nubosidad
with open('/home/emi/Dropbox/DTEC/MJO/merra/data/cldtot.pkl', 'rb') as file:
    data = pickle.load(file)

cld_uru = pd.DataFrame()
cld_arg = pd.DataFrame()
cld_chi = pd.DataFrame()

cld_uru = data[0]
cld_arg = data[1]
cld_chi = data[2]

cld_uru.index = pd.date_range(start="2000-01-01", end="2024-08-01",freq='D')
cld_arg.index = pd.date_range(start="2000-01-01", end="2024-08-01",freq='D')
cld_chi.index = pd.date_range(start="2000-01-01", end="2024-08-01",freq='D')

cld_uru = cld_uru.truncate(before=pd.Timestamp("2011-01-01"), after=pd.Timestamp("2022-12-31"))
cld_arg = cld_arg.truncate(before=pd.Timestamp("2007-01-01"), after=pd.Timestamp("2022-12-31"))
cld_chi = cld_chi.truncate(before=pd.Timestamp("2016-01-01"), after=pd.Timestamp("2022-12-31"))
# ~ print(temparg)
# ~ print(cld_arg.values)

###### Argentina
seriesA = pd.DataFrame()
seriesA[0] = temparg[1] # mes
seriesA[1] = temparg[3] # temp
seriesA[2] = cld_arg.values # nubosidad

# VERANO
verA = seriesA.loc[(seriesA[0] == 1) | (seriesA[0] == 2) | (seriesA[0] == 12)]
# hay que convertir a float
tverA = verA[1].values
cverA = verA[2].values

float_tverA = [float(string) for string in tverA]
float_cverA = [float(string) for string in cverA]

# OTOÑO
otoA = seriesA.loc[(seriesA[0] == 3) | (seriesA[0] == 4) | (seriesA[0] == 5)]
# hay que conototir a float
totoA= otoA[1].values
cotoA = otoA[2].values
float_totoA = [float(string) for string in totoA]
float_cotoA = [float(string) for string in cotoA]

# INVIERNO
invA = seriesA.loc[(seriesA[0] == 6) | (seriesA[0] == 7) | (seriesA[0] == 8)]
# hay que coninvtir a float
tinvA = invA[1].values
cinvA = invA[2].values
float_tinvA = [float(string) for string in tinvA]
float_cinvA = [float(string) for string in cinvA]

# primavera
priA = seriesA.loc[(seriesA[0] == 9) | (seriesA[0] == 10) | (seriesA[0] == 11)]

# ~ float_cpriA = [float(string) for string in cpriA]

###### Uruguay
seriesU = pd.DataFrame()
seriesU[0] = tempuru[1] # mes
seriesU[1] = tempuru[3] # temp
seriesU[2] = cld_uru.values # nubosidad

# VERANO
verU = seriesU.loc[(seriesU[0] == 1) | (seriesU[0] == 2) | (seriesU[0] == 12)]
# hay que convertir a float
tverU = verU[1].values
cverU = verU[2].values

float_tverU = [float(string) for string in tverU]
float_cverU = [float(string) for string in cverU]

# OTOÑO
otoU = seriesU.loc[(seriesU[0] == 3) | (seriesU[0] == 4) | (seriesU[0] == 5)]
# hay que conototir a float
totoU= otoU[1].values
cotoU = otoU[2].values
float_totoU = [float(string) for string in totoU]
float_cotoU = [float(string) for string in cotoU]

# INVIERNO
invU = seriesU.loc[(seriesU[0] == 6) | (seriesU[0] == 7) | (seriesU[0] == 8)]
# hay que coninvtir a float
tinvU = invU[1].values
cinvU = invU[2].values
float_tinvU = [float(string) for string in tinvU]
float_cinvU = [float(string) for string in cinvU]

# PRIMAVERA
priU = seriesU.loc[(seriesU[0] == 9) | (seriesU[0] == 10) | (seriesU[0] == 11)]
# hay que convertir a float
tpriU = priU[1].values
cpriU = priU[2].values
float_tpriU = [float(string) for string in tpriU]
float_cpriU = [float(string) for string in cpriU]

###### Chile
seriesC = pd.DataFrame()
seriesC[0] = tempchi[1] # mes
seriesC[1] = tempchi[3] # temp
seriesC[2] = cld_chi.values # nubosidad

# VERANO
verC = seriesC.loc[(seriesC[0] == 1) | (seriesC[0] == 2) | (seriesC[0] == 12)]
# hay que convertir a float
tverC = verC[1].values
cverC = verC[2].values

float_tverC = [float(string) for string in tverC]
float_cverC = [float(string) for string in cverC]

# OTOÑO
otoC = seriesC.loc[(seriesC[0] == 3) | (seriesC[0] == 4) | (seriesC[0] == 5)]
# hay que conototir a float
totoC= otoC[1].values
cotoC = otoC[2].values
float_totoC = [float(string) for string in totoC]
float_cotoC = [float(string) for string in cotoC]

# INVIERNO
invC = seriesC.loc[(seriesC[0] == 6) | (seriesC[0] == 7) | (seriesC[0] == 8)]
# hay que coninvtir a float
tinvC = invC[1].values
cinvC = invC[2].values
float_tinvC = [float(string) for string in tinvC]
float_cinvC = [float(string) for string in cinvC]

# PRIMAVERA
priC = seriesC.loc[(seriesC[0] == 9) | (seriesC[0] == 10) | (seriesC[0] == 11)]
# hay que convertir a float
tpriC = priC[1].values
cpriC = priC[2].values
float_tpriC = [float(string) for string in tpriC]
float_cpriC = [float(string) for string in cpriC]

# GRAFICO
fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4, 3,figsize=(10,10))
sns.set(font_scale = 2)

# PRIMER FILA; ARGENTINA
##### ver
kdeplot = sns.regplot(ax=ax1,x = float_tverA, y = float_cverA, scatter_kws = {"color": "black", "alpha": 0.3, 's': 8},line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
# ~ r = np.corrcoef(float_tverA, float_dverA)
ax1.tick_params(labelsize=14)
# ~ ax1.text(16.2, 520,'r=', fontsize=15)
# ~ ax1.text(18.2, 520, round(r[0, 1], 2), fontsize=15)
ax1.set_title('Argentina', fontsize = 14, weight='bold')
# ~ ax1.set_ylim(200, 570)

##### oto
kdeplot = sns.regplot(ax=ax4,x=float_totoA, y = float_cotoA, order=2, scatter_kws = {"color": "black", "alpha": 0.3, 's': 8}, line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
# ~ r = np.corrcoef(float_totoA, float_dotoA)
ax4.tick_params(labelsize=14)
# ~ ax2.text(-2.4, 185,'r=', fontsize=15)
# ~ ax2.text(-1.8, 185, round(r[0, 1], 2), fontsize=15)
# ~ ax4.set_ylim(200, 570)

##### inv
kdeplot = sns.regplot(ax=ax7,x=float_tinvA, y = float_cinvA, scatter_kws = {"color": "black", "alpha": 0.3, 's': 8}, line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
# ~ r = np.corrcoef(float_tinvA, float_dinvA)
ax7.tick_params(labelsize=14)
# ~ ax7.text(15.5, 520,'r=', fontsize=15)
# ~ ax7.text(18, 520, round(r[0, 1], 2), fontsize=15)
# ~ ax7.set_ylim(200, 570)

##### pri
kdeplot = sns.regplot(ax=ax10,x=priA[1], y = priA[2], order=2, scatter_kws = {"color": "black", "alpha": 0.3, 's': 8}, line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
# ~ r = np.corrcoef(float_tpriA,float_dpriA)
ax10.tick_params(labelsize=14)
# ~ ax4.text(-2.4, 350,'r=', fontsize=15)
# ~ ax4.text(-1.8, 350, round(r[0, 1], 2), fontsize=15)
# ~ ax10.set_ylim(200, 570)


plt.show()
