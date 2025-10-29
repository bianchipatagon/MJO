import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
import seaborn as sns
from scipy import stats
import pickle
import matplotlib as mpl
from statsmodels.tsa.seasonal import STL

## temperatura
temparg = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/temp-arg.txt', header=None, delimiter=';', na_values='-99')

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

## demanda
demarg = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/arg-dem.txt', header=None, delimiter=';', na_values='-99')

## indice mjo (para sacar dia de la semana)
mjoarg = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2007.txt', header=None, delimiter=',', na_values='-99')
mjouru = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2011.txt', header=None, delimiter=',', na_values='-99')
mjochi = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2014.txt', header=None, delimiter=',', na_values='-99')

##### armamos dataframe
seriesA = pd.DataFrame()
seriesA[0] = mjoarg[1] # mes
seriesA[1] = mjoarg[3] # dia de la semana
seriesA[2] = temparg[3]
seriesA[3] = cld_arg.values
seriesA[4] = demarg[3]
### removemos tendencia demanda
stl = STL(seriesA[4], seasonal=13, period = 365, robust=True) 
result = stl.fit()
original_mean = seriesA[4].mean()
seriesA[4] = seriesA[4] - result.trend + original_mean
print(seriesA)

# sacamos los fines de semana
seriesA = seriesA.loc[(seriesA[1] == 1) | (seriesA[1] == 2) | (seriesA[1] == 3) | (seriesA[1] == 1) | (seriesA[1] == 5)]

# VERANO
verA = seriesA.loc[(seriesA[0] == 1) | (seriesA[0] == 2) | (seriesA[0] == 12)]
threshold = verA[3].quantile(0.9)
threshold1 = verA[3].quantile(0.1)
verAN = verA[verA[3]>threshold]
verAD = verA[verA[3]<threshold1]
demV = pd.DataFrame()
demV[0] = verAN[4].values
demV[1] = verAD[4].values

# OTOÑO
otoA = seriesA.loc[(seriesA[0] == 3) | (seriesA[0] == 4) | (seriesA[0] == 5)]
threshold = otoA[3].quantile(0.9)
threshold1 = otoA[3].quantile(0.1)
otoAN = otoA[otoA[3]>threshold]
otoAD = otoA[otoA[3]<threshold1]
demO = pd.DataFrame()
demO[0] = otoAN[4].values
demO[1] = otoAD[4].values

# INVIERNO
invA = seriesA.loc[(seriesA[0] == 6) | (seriesA[0] == 7) | (seriesA[0] == 8)]
threshold = invA[3].quantile(0.9)
threshold1 = invA[3].quantile(0.1)
invAN = invA[invA[3]>threshold]
invAD = invA[invA[3]<threshold1]
demI = pd.DataFrame()
demI[0] = invAN[4].values
demI[1] = invAD[4].values

# PRIMAVERA
priA = seriesA.loc[(seriesA[0] == 9) | (seriesA[0] == 10) | (seriesA[0] == 11)]
threshold = priA[3].quantile(0.9)
threshold1 = priA[3].quantile(0.1)
priAN = priA[priA[3]>threshold]
priAD = priA[priA[3]<threshold1]
demP = pd.DataFrame()
demP[0] = priAN[4].values
demP[1] = priAD[4].values

fig, (ax1,ax2,ax3,ax4) = plt.subplots(1,4,figsize=(9.5,3),sharex=True)
demV.boxplot(ax=ax1, whis=(0, 100), showmeans=True, meanline = True)
demO.boxplot(ax=ax2, whis=(0, 100), showmeans=True, meanline = True)
demI.boxplot(ax=ax3, whis=(0, 100), showmeans=True, meanline = True)
demP.boxplot(ax=ax4, whis=(0, 100), showmeans=True, meanline = True)

plt.show()


