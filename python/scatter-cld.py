import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
# ~ import pymannkendall as mk
import seaborn as sns
from scipy import stats
import pickle


## demanda
demarg = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/arg-dem.txt', header=None, delimiter=';', na_values='-99')
demuru = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/uru-dem.txt', header=None, delimiter=';', na_values='-99')
demchi = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/chi-dem3.txt', header=None, delimiter=';', na_values='-99')

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


## indice mjo (para sacar dia de la semana)
mjoarg = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2007.txt', header=None, delimiter=',', na_values='-99')
mjouru = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2011.txt', header=None, delimiter=',', na_values='-99')
mjochi = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2014.txt', header=None, delimiter=',', na_values='-99')

## Argentina
seriesA = pd.DataFrame()

seriesA[0] = mjoarg[1] # mes
seriesA[1] = mjoarg[3] # dia de la semana
seriesA[2] = demarg[3] # demanda
seriesA[3] = cld_arg.values # temp

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
seriesU[3] = cld_uru.values # temp

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

## Chile
seriesC = pd.DataFrame()

seriesC[0] = mjochi[1] # mes
seriesC[1] = mjochi[3] # dia de la semana
seriesC[2] = demchi[3] # demanda
seriesC[2] = seriesC[2]/1000 # PASAMOS A GWh
seriesC[3] = cld_chi.values # temp

# sacamos los fines de semana
seriesC = seriesC.loc[(seriesC[1] == 1) | (seriesC[1] == 2) | (seriesC[1] == 3) | (seriesC[1] == 1) | (seriesC[1] == 5)]

# VERANO
verC = seriesC.loc[(seriesC[0] == 1) | (seriesC[0] == 2) | (seriesC[0] == 12)]
# hay que convertir a float
tverC = verC[3].values
dverC = verC[2].values

float_tverC = [float(string) for string in tverC]
float_dverC = [float(string) for string in dverC]

# OTOÑO
otoC = seriesC.loc[(seriesC[0] == 3) | (seriesC[0] == 4) | (seriesC[0] == 5)]
# hay que conototir a float
totoC = otoC[3].values
dotoC = otoC[2].values
float_totoC = [float(string) for string in totoC]
float_dotoC = [float(string) for string in dotoC]

# INVIERNO
invC = seriesC.loc[(seriesC[0] == 6) | (seriesC[0] == 7) | (seriesC[0] == 8)]
# hay que coninvtir a float
tinvC = invC[3].values
dinvC = invC[2].values
float_tinvC = [float(string) for string in tinvC]
float_dinvC = [float(string) for string in dinvC]

# primavera
priC = seriesC.loc[(seriesC[0] == 9) | (seriesC[0] == 10) | (seriesC[0] == 11)]
# hay que convertir a float
tpriC = priC[3].values
dpriC = priC[2].values
float_tpriC = [float(string) for string in tpriC]
float_dpriC = [float(string) for string in dpriC]

# GRAFICO
fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8),(ax9,ax10,ax11,ax12)) = plt.subplots(3, 4,figsize=(13,10))
sns.set(font_scale = 1.5)

# PRIMER FILA; ARGENTINA
##### ver
kdeplot = sns.regplot(ax=ax1,x = float_tverA, y = float_dverA, scatter_kws = {"color": "black", "alpha": 0.3},line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_tverA, float_dverA)
ax1.tick_params(labelsize=14)
# ~ ax1.text(16.2, 520,'r=', fontsize=15)
# ~ ax1.text(18.2, 520, round(r[0, 1], 2), fontsize=15)
ax1.set_title('DEF', fontsize = 14, weight='bold')
ax1.set_ylim(200, 570)

##### oto
kdeplot = sns.regplot(ax=ax2,x=float_totoA, y = float_dotoA, order=2, scatter_kws = {"color": "black", "alpha": 0.3}, line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_totoA, float_dotoA)
ax2.tick_params(labelsize=14)
# ~ ax2.text(-2.4, 185,'r=', fontsize=15)
# ~ ax2.text(-1.8, 185, round(r[0, 1], 2), fontsize=15)
ax2.set_title('MAM', fontsize = 14, weight='bold')
ax2.set_ylim(200, 570)
ax2.set_yticklabels([])

##### inv
kdeplot = sns.regplot(ax=ax3,x=float_tinvA, y = float_dinvA, scatter_kws = {"color": "black", "alpha": 0.3}, line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_tinvA, float_dinvA)
ax3.tick_params(labelsize=14)
# ~ ax3.text(16.5, 520,'r=', fontsize=15)
# ~ ax3.text(19, 520, round(r[0, 1], 2), fontsize=15)
ax3.set_title('JAS', fontsize = 15, weight='bold')
ax3.set_ylim(200, 570)
ax3.set_yticklabels([])

##### pri
kdeplot = sns.regplot(ax=ax4,x=float_tpriA, y = float_dpriA, order=2, scatter_kws = {"color": "black", "alpha": 0.3}, line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_tpriA,float_dpriA)
ax4.tick_params(labelsize=14)
# ~ ax4.text(-2.4, 350,'r=', fontsize=15)
# ~ ax4.text(-1.8, 350, round(r[0, 1], 2), fontsize=15)
ax4.set_title('OND', fontsize = 14, weight='bold')
ax4.set_ylim(200, 570)
ax4.set_yticklabels([])

# SEGUNDA FILA; URUGUAY
##### ver
kdeplot = sns.regplot(ax=ax5,x = float_tverU, y = float_dverU, scatter_kws = {"color": "black", "alpha": 0.3},line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_tverU, float_dverU)
ax5.tick_params(labelsize=14)
# ~ ax5.text(15, 40,'r=', fontsize=15)
# ~ ax5.text(17, 40, round(r[0, 1], 2), fontsize=15)
ax5.set_ylabel('power demand [MWh]', fontsize=15)
ax5.set_ylim(20, 45)

##### oto
kdeplot = sns.regplot(ax=ax6,x=float_totoU, y = float_dotoU, order=2, scatter_kws = {"color": "black", "alpha": 0.3}, line_kws = {"color": "black"}, ci= None, label=None)
# ~ r = np.corrcoef(float_totoU, float_dotoU)
r = stats.spearmanr(float_totoU, float_dotoU)
print(r)
ax6.tick_params(labelsize=14)
# ~ ax2.text(15, 40,'r=', fontsize=15)
# ~ ax2.text(17, 40, round(r[0, 1], 2), fontsize=15)
ax6.set_ylim(20, 45)
ax6.set_yticklabels([])

##### inv
kdeplot = sns.regplot(ax=ax7,x=float_tinvU, y = float_dinvU, scatter_kws = {"color": "black", "alpha": 0.3}, line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_tinvU, float_dinvU)
ax7.tick_params(labelsize=14)
# ~ ax7.text(12.5, 40,'r=', fontsize=15)
# ~ ax7.text(14, 40, round(r[0, 1], 2), fontsize=15)
ax7.set_ylim(20, 45)
ax7.set_yticklabels([])

##### pri
kdeplot = sns.regplot(ax=ax8,x=float_tpriU, y = float_dpriU, order=2, scatter_kws = {"color": "black", "alpha": 0.3}, line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_tpriU,float_dpriU)
ax8.tick_params(labelsize=14)
# ~ ax4.text(-2.4, 350,'r=', fontsize=15)
# ~ ax4.text(-1.8, 350, round(r[0, 1], 2), fontsize=15)
ax8.set_ylim(20, 45)
ax8.set_yticklabels([])

# SEGUNDA FILA; CHILE
##### ver
kdeplot = sns.regplot(ax=ax9,x = float_tverC, y = float_dverC, scatter_kws = {"color": "black", "alpha": 0.3},line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_tverC, float_dverC)
ax9.tick_params(labelsize=14)
# ~ ax9.text(16, 550,'r=', fontsize=15)
# ~ ax9.text(18, 550, round(r[0, 1], 2), fontsize=15)
ax9.set_ylim(155, 260)

##### oto
kdeplot = sns.regplot(ax=ax10,x=float_totoC, y = float_dotoC, order=2, scatter_kws = {"color": "black", "alpha": 0.3}, line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_totoC, float_dotoC)
ax10.tick_params(labelsize=14)
# ~ ax2.text(-2.4, 185,'r=', fontsize=15)
# ~ ax2.text(-1.8, 185, round(r[0, 1], 2), fontsize=15)
ax10.set_ylim(155, 260)
ax10.set_yticklabels([])

##### inv
kdeplot = sns.regplot(ax=ax11,x=float_tinvC, y = float_dinvC, scatter_kws = {"color": "black", "alpha": 0.3}, line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_tinvC, float_dinvC)
ax11.tick_params(labelsize=14)
# ~ ax11.text(5, 550,'r=', fontsize=15)
# ~ ax11.text(7, 550, round(r[0, 1], 2), fontsize=15)
ax11.set_ylim(155, 260)
ax11.set_yticklabels([])

##### pri
kdeplot = sns.regplot(ax=ax12,x=float_tpriC, y = float_dpriC, order=2, scatter_kws = {"color": "black", "alpha": 0.3}, line_kws = {"color": "black"}, ci= None, label=None)
r = np.corrcoef(float_tpriC,float_dpriC)
ax12.xaxis.set_tick_params(labelsize=14)
# ~ ax4.text(-2.4, 350,'r=', fontsize=15)
# ~ ax4.text(-1.8, 350, round(r[0, 1], 2), fontsize=15)
ax12.set_ylim(155, 260)
ax12.set_yticklabels([])

fig.subplots_adjust(hspace=0.15,wspace=0.05)
fig.text(0.45, 0.06, 'cloud fraction []', fontsize = 14)
fig.text(0.06, 0.72, 'Argentina', fontsize = 14, rotation='vertical' , weight='bold')
fig.text(0.06, 0.45, 'Uruguay', fontsize = 14, rotation='vertical', weight='bold')
fig.text(0.06, 0.20, 'Chile', fontsize = 14, rotation='vertical', weight='bold')

plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/scatter_cld.jpg', dpi=300, bbox_inches="tight")
plt.show()


