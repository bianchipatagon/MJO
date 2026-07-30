import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
# ~ import pymannkendall as mk
import seaborn as sns
from scipy import stats
from statsmodels.tsa.seasonal import STL
import pickle
from matplotlib import cm


## demanda
demarg = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/arg-dem.txt', header=None, delimiter=';', na_values='-99')
demuru = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/uru-dem.txt', header=None, delimiter=';', na_values='-99')

## temperatura
temparg = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/temp-arg.txt', header=None, delimiter=';', na_values='-99')
tempuru = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/temp-uruERA5.txt', header=None, delimiter=';', na_values='-99')

tempuru.index = pd.date_range(start="2000-01-01", end="2022-12-31",freq='D')
temparg.index = pd.date_range(start="2000-01-01", end="2022-12-31",freq='D')

tempuru = tempuru.truncate(before=pd.Timestamp("2011-01-01"), after=pd.Timestamp("2022-12-31"))
temparg = temparg.truncate(before=pd.Timestamp("2007-01-01"), after=pd.Timestamp("2022-12-31"))

# ~ '''
## indice mjo (para sacar dia de la semana)
mjoarg = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2007.txt', header=None, delimiter=',', na_values='-99')
mjouru = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2011.txt', header=None, delimiter=',', na_values='-99')

## Argentina
seriesA = pd.DataFrame()

seriesA[0] = mjoarg[1] # mes
seriesA[1] = mjoarg[3] # dia de la semana
seriesA[2] = demarg[3] # demanda

### removemos tendencia demanda
stl = STL(seriesA[2], seasonal=13, period = 365, robust=True) 
result = stl.fit()
original_mean = seriesA[2].mean()
seriesA[2] = seriesA[2] - result.trend + original_mean

seriesA[3] = temparg[3].values # temp

# sacamos los fines de semana
seriesA = seriesA.loc[(seriesA[1] == 1) | (seriesA[1] == 2) | (seriesA[1] == 3) | (seriesA[1] == 1) | (seriesA[1] == 5)]

# VERANO
verA = seriesA.loc[(seriesA[0] == 1) | (seriesA[0] == 2) | (seriesA[0] == 12)]
# hay que convertir a float
tverA = verA[3].values
dverA = verA[2].values

float_tverA = [float(string) for string in tverA]
float_dverA = [float(string) for string in dverA]

# OTOÑO
otoA = seriesA.loc[(seriesA[0] == 3) | (seriesA[0] == 4) | (seriesA[0] == 5)]
# hay que conototir a float
totoA= otoA[3].values
dotoA = otoA[2].values
float_totoA = [float(string) for string in totoA]
float_dotoA = [float(string) for string in dotoA]

# INVIERNO
invA = seriesA.loc[(seriesA[0] == 6) | (seriesA[0] == 7) | (seriesA[0] == 8)]
# hay que coninvtir a float
tinvA = invA[3].values
dinvA = invA[2].values
float_tinvA = [float(string) for string in tinvA]
float_dinvA = [float(string) for string in dinvA]

# primavera
priA = seriesA.loc[(seriesA[0] == 9) | (seriesA[0] == 10) | (seriesA[0] == 11)]
# hay que convertir a float
tpriA = priA[3].values
dpriA = priA[2].values
float_tpriA = [float(string) for string in tpriA]
float_dpriA = [float(string) for string in dpriA]

## Uruguay
seriesU = pd.DataFrame()

seriesU[0] = mjouru[1] # mes
seriesU[1] = mjouru[3] # dia de la semana
seriesU[2] = demuru[3] # demanda
seriesU[2] = seriesU[2]/1000 # PASAMOS A GWh

### removemos tendencia demanda
stl = STL(seriesU[2], seasonal=13, period = 365, robust=True) 
result = stl.fit()
original_mean = seriesU[2].mean()
seriesU[2] = seriesU[2] - result.trend + original_mean

seriesU[3] = tempuru[3].values # temp

# sacamos los fines de semana
seriesU = seriesU.loc[(seriesU[1] == 1) | (seriesU[1] == 2) | (seriesU[1] == 3) | (seriesU[1] == 1) | (seriesU[1] == 5)]

# VERANO
verU = seriesU.loc[(seriesU[0] == 1) | (seriesU[0] == 2) | (seriesU[0] == 12)]
# hay que convertir a float
tverU = verU[3].values
dverU = verU[2].values

float_tverU = [float(string) for string in tverU]
float_dverU = [float(string) for string in dverU]

# OTOÑO
otoU = seriesU.loc[(seriesU[0] == 3) | (seriesU[0] == 4) | (seriesU[0] == 5)]
# hay que conototir a float
totoU= otoU[3].values
dotoU = otoU[2].values
float_totoU = [float(string) for string in totoU]
float_dotoU = [float(string) for string in dotoU]

# INVIERNO
invU = seriesU.loc[(seriesU[0] == 6) | (seriesU[0] == 7) | (seriesU[0] == 8)]
# hay que coninvtir a float
tinvU = invU[3].values
dinvU = invU[2].values
float_tinvU = [float(string) for string in tinvU]
float_dinvU = [float(string) for string in dinvU]

# primavera
priU = seriesU.loc[(seriesU[0] == 9) | (seriesU[0] == 10) | (seriesU[0] == 11)]
# hay que convertir a float
tpriU = priU[3].values
dpriU = priU[2].values
float_tpriU = [float(string) for string in tpriU]
float_dpriU = [float(string) for string in dpriU]



# GRAFICO
fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8)) = plt.subplots(2, 4,figsize=(9,3.6), sharey="row")
sns.set(font_scale = 2)

# PRIMER FILA; ARGENTINA

# Normalize the third variable for colormap
# ~ norm = plt.Normalize(vmin=cverA.min(), vmax=cverA.max())
# ~ colors = cm.viridis(norm(cverA))
##### ver
kdeplot = sns.regplot(ax=ax1,x = float_tverA, y = float_dverA, scatter_kws = {"color": "black", "alpha": 0.2, 's': 12},line_kws = {"color": "black",'lw': 1}, ci= None, label=None)

r = np.corrcoef(float_tverA, float_dverA)
ax1.tick_params(labelsize=14)
# ~ ax1.text(16.2, 520,'r=', fontsize=15)
# ~ ax1.text(18.2, 520, round(r[0, 1], 2), fontsize=15)
ax1.set_title('DJF', fontsize = 14)
ax1.set_ylim(200, 570)
ax1.xaxis.set_tick_params(labelsize=0, color='white')

##### oto
kdeplot = sns.regplot(ax=ax2,x=float_totoA, y = float_dotoA, order=2, scatter_kws = {"color": "black", "alpha": 0.2, 's': 12}, line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
r = np.corrcoef(float_totoA, float_dotoA)
ax2.tick_params(labelsize=14)
# ~ ax2.text(-2.4, 185,'r=', fontsize=15)
# ~ ax2.text(-1.8, 185, round(r[0, 1], 2), fontsize=15)
ax2.set_ylim(200, 570)
ax2.set_title('MAM', fontsize = 14)
ax2.xaxis.set_tick_params(labelsize=0, color='white')
ax2.yaxis.set_tick_params(labelsize=0, color='white')

##### inv
kdeplot = sns.regplot(ax=ax3,x=float_tinvA, y = float_dinvA, scatter_kws = {"color": "black", "alpha": 0.2, 's': 12}, line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
r = np.corrcoef(float_tinvA, float_dinvA)
ax3.tick_params(labelsize=14)
# ~ ax3.text(15.5, 520,'r=', fontsize=15)
# ~ ax3.text(18, 520, round(r[0, 1], 2), fontsize=15)
ax3.set_ylim(200, 570)
ax3.set_title('JJA', fontsize = 14)
ax3.xaxis.set_tick_params(labelsize=0, color='white')
ax3.yaxis.set_tick_params(labelsize=0, color='white')

##### pri
kdeplot = sns.regplot(ax=ax4,x=float_tpriA, y = float_dpriA, order=2, scatter_kws = {"color": "black", "alpha": 0.2, 's': 12}, line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
r = np.corrcoef(float_tpriA,float_dpriA)
ax4.tick_params(labelsize=14)
# ~ ax4.text(-2.4, 350,'r=', fontsize=15)
# ~ ax4.text(-1.8, 350, round(r[0, 1], 2), fontsize=15)
ax4.set_ylim(200, 570)
ax4.set_title('SON', fontsize = 14)
ax4.xaxis.set_tick_params(labelsize=0, color='white')
ax4.yaxis.set_tick_params(labelsize=0, color='white')

# SEGUNDA FILA; URUGUAY
##### ver
kdeplot = sns.regplot(ax=ax5,x = float_tverU, y = float_dverU, scatter_kws = {"color": "black", "alpha": 0.2, 's': 12},line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
r = np.corrcoef(float_tverU, float_dverU)
ax5.tick_params(labelsize=14)
# ~ ax5.text(15, 40,'r=', fontsize=15)
# ~ ax5.text(17, 40, round(r[0, 1], 2), fontsize=15)
ax5.set_ylim(20, 45)

##### oto
kdeplot = sns.regplot(ax=ax6,x=float_totoU, y = float_dotoU, order=2, scatter_kws = {"color": "black", "alpha": 0.2, 's': 12}, line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
# ~ r = np.corrcoef(float_totoU, float_dotoU)
r = stats.spearmanr(float_totoU, float_dotoU)
print(r)
ax6.tick_params(labelsize=14)
# ~ ax2.text(15, 40,'r=', fontsize=15)
# ~ ax2.text(17, 40, round(r[0, 1], 2), fontsize=15)
ax6.set_ylim(20, 45)
ax6.yaxis.set_tick_params(labelsize=0, color='white')

##### inv
kdeplot = sns.regplot(ax=ax7,x=float_tinvU, y = float_dinvU, scatter_kws = {"color": "black", "alpha": 0.2, 's': 12}, line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
r = np.corrcoef(float_tinvU, float_dinvU)
ax7.tick_params(labelsize=14)
# ~ ax7.text(12.5, 40,'r=', fontsize=15)
# ~ ax7.text(14, 40, round(r[0, 1], 2), fontsize=15)
ax7.set_ylim(20, 45)
ax7.yaxis.set_tick_params(labelsize=0, color='white')

##### pri
kdeplot = sns.regplot(ax=ax8,x=float_tpriU, y = float_dpriU, order=2, scatter_kws = {"color": "black", "alpha": 0.2, 's': 12}, line_kws = {"color": "black",'lw': 1}, ci= None, label=None)
r = np.corrcoef(float_tpriU,float_dpriU)
ax8.tick_params(labelsize=14)
# ~ ax4.text(-2.4, 350,'r=', fontsize=15)
# ~ ax4.text(-1.8, 350, round(r[0, 1], 2), fontsize=15)
ax8.set_ylim(20, 45)
ax8.yaxis.set_tick_params(labelsize=0, color='white')


fig.subplots_adjust(hspace=0.1,wspace=0.05)
fig.text(0.45, 0.02, 'temperature [°c]', fontsize = 15)
fig.text(0.91, 0.6, 'Argentina', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.22, 'Uruguay', fontsize = 14, rotation='vertical')
fig.text(0.05, 0.25, 'power demand [MWh]', fontsize=15, rotation='vertical')

fig.subplots_adjust(bottom=0.13)
# ~ fig.subplots_adjust(left=0.15)

plt.savefig('/home/emi/Documents/MJO/imagenes/scatter_temp.svg', dpi=300, bbox_inches="tight")
# ~ plt.show()
