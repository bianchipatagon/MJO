import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from scipy.signal import detrend

#################################
#######VIENTO####################
#################################

Vuru = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-vie-agrup.csv', header=None, delimiter=',', na_values='-99')
Varg = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-vie-agrup.csv', header=None, delimiter=',', na_values='-99')
Vchi = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-vie-agrup.csv', header=None, delimiter=',', na_values='-99')

Vuru_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-vie.txt', header=None, delimiter=';', na_values='-99')
Varg_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-vie.txt', header=None, delimiter=';', na_values='-99')
Vchi_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-vie.txt', header=None, delimiter=';', na_values='-99')

Vmad = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, RMM1, RMM2, phase, amplitude
fmo = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/filtered.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, RMM1, RMM2, phase, amplitude

series = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series[0] = Vmad[1]
# cargamos fase
series[1] = Vmad[6]
# cargamos dia de la semana, para cuando trabajemos con demanda
series[2] = Vmad[3]
#  cargamos amplitud, para quedarnos con MJO activas
series[3] = Vmad[7]
# series uruguay argentina chile
series[4] = Vuru[1]
series[5] = Varg[1]
series[6] = Vchi[1]
series[7] = fmo[7]


# nos quedamos con MJO activos, esto es cuando la amplitud WH es >= 1
seriesWH = series.loc[series[3] > 1]

# VERANO
veranoWH = seriesWH.loc[(seriesWH[0] == 1) | (seriesWH[0] == 2) | (seriesWH[0] == 12)]
Vf1v = veranoWH.loc[veranoWH[1] == 1]
Vf2v = veranoWH.loc[veranoWH[1] == 2]
Vf3v = veranoWH.loc[veranoWH[1] == 3]
Vf4v = veranoWH.loc[veranoWH[1] == 4]
Vf5v = veranoWH.loc[veranoWH[1] == 5]
Vf6v = veranoWH.loc[veranoWH[1] == 6]
Vf7v = veranoWH.loc[veranoWH[1] == 7]
Vf8v = veranoWH.loc[veranoWH[1] == 8]

# OTOÑO
otonoWH = seriesWH.loc[(seriesWH[0] == 3) | (seriesWH[0] == 4) | (seriesWH[0] == 5)]
Vf1o = otonoWH.loc[otonoWH[1] == 1]
Vf2o = otonoWH.loc[otonoWH[1] == 2]
Vf3o = otonoWH.loc[otonoWH[1] == 3]
Vf4o = otonoWH.loc[otonoWH[1] == 4]
Vf5o = otonoWH.loc[otonoWH[1] == 5]
Vf6o = otonoWH.loc[otonoWH[1] == 6]
Vf7o = otonoWH.loc[otonoWH[1] == 7]
Vf8o = otonoWH.loc[otonoWH[1] == 8]

# INVIERNO
inviernoWH = seriesWH.loc[(seriesWH[0] == 6) | (seriesWH[0] == 7) | (seriesWH[0] == 8)]
Vf1i = inviernoWH.loc[inviernoWH[1] == 1]
Vf2i = inviernoWH.loc[inviernoWH[1] == 2]
Vf3i = inviernoWH.loc[inviernoWH[1] == 3]
Vf4i = inviernoWH.loc[inviernoWH[1] == 4]
Vf5i = inviernoWH.loc[inviernoWH[1] == 5]
Vf6i = inviernoWH.loc[inviernoWH[1] == 6]
Vf7i = inviernoWH.loc[inviernoWH[1] == 7]
Vf8i = inviernoWH.loc[inviernoWH[1] == 8]

# primavera
primaveraWH = seriesWH.loc[(seriesWH[0] == 9) | (seriesWH[0] == 10) | (seriesWH[0] == 11)]
Vf1p = primaveraWH.loc[primaveraWH[1] == 1]
Vf2p = primaveraWH.loc[primaveraWH[1] == 2]
Vf3p = primaveraWH.loc[primaveraWH[1] == 3]
Vf4p = primaveraWH.loc[primaveraWH[1] == 4]
Vf5p = primaveraWH.loc[primaveraWH[1] == 5]
Vf6p = primaveraWH.loc[primaveraWH[1] == 6]
Vf7p = primaveraWH.loc[primaveraWH[1] == 7]
Vf8p = primaveraWH.loc[primaveraWH[1] == 8]

verwh = [len(Vf1v),len(Vf2v),len(Vf3v),len(Vf4v),len(Vf5v),len(Vf6v),len(Vf7v),len(Vf8v)]
otowh = [len(Vf1o),len(Vf2o),len(Vf3o),len(Vf4o),len(Vf5o),len(Vf6o),len(Vf7o),len(Vf8o)]
invwh = [len(Vf1i),len(Vf2i),len(Vf3i),len(Vf4i),len(Vf5i),len(Vf6i),len(Vf7i),len(Vf8i)]
priwh = [len(Vf1p),len(Vf2p),len(Vf3p),len(Vf4p),len(Vf5p),len(Vf6p),len(Vf7p),len(Vf8p)]

# nos quedamos con MJO activos, esto es cuando la amplitud fmo es >= 1
seriesFMO = series.loc[series[7] > 1]

# VERANO
veranoFMO = seriesFMO.loc[(seriesFMO[0] == 1) | (seriesFMO[0] == 2) | (seriesFMO[0] == 12)]
V1v = veranoFMO.loc[veranoFMO[1] == 1]
V2v = veranoFMO.loc[veranoFMO[1] == 2]
V3v = veranoFMO.loc[veranoFMO[1] == 3]
V4v = veranoFMO.loc[veranoFMO[1] == 4]
V5v = veranoFMO.loc[veranoFMO[1] == 5]
V6v = veranoFMO.loc[veranoFMO[1] == 6]
V7v = veranoFMO.loc[veranoFMO[1] == 7]
V8v = veranoFMO.loc[veranoFMO[1] == 8]

# OTOÑO
otonoFMO = seriesFMO.loc[(seriesFMO[0] == 3) | (seriesFMO[0] == 4) | (seriesFMO[0] == 5)]
V1o = otonoFMO.loc[otonoFMO[1] == 1]
V2o = otonoFMO.loc[otonoFMO[1] == 2]
V3o = otonoFMO.loc[otonoFMO[1] == 3]
V4o = otonoFMO.loc[otonoFMO[1] == 4]
V5o = otonoFMO.loc[otonoFMO[1] == 5]
V6o = otonoFMO.loc[otonoFMO[1] == 6]
V7o = otonoFMO.loc[otonoFMO[1] == 7]
V8o = otonoFMO.loc[otonoFMO[1] == 8]

# INVIERNO
inviernoFMO = seriesFMO.loc[(seriesFMO[0] == 6) | (seriesFMO[0] == 7) | (seriesFMO[0] == 8)]
V1i = inviernoFMO.loc[inviernoFMO[1] == 1]
V2i = inviernoFMO.loc[inviernoFMO[1] == 2]
V3i = inviernoFMO.loc[inviernoFMO[1] == 3]
V4i = inviernoFMO.loc[inviernoFMO[1] == 4]
V5i = inviernoFMO.loc[inviernoFMO[1] == 5]
V6i = inviernoFMO.loc[inviernoFMO[1] == 6]
V7i = inviernoFMO.loc[inviernoFMO[1] == 7]
V8i = inviernoFMO.loc[inviernoFMO[1] == 8]

# primavera
primaveraFMO = seriesFMO.loc[(seriesFMO[0] == 9) | (seriesFMO[0] == 10) | (seriesFMO[0] == 11)]
V1p = primaveraFMO.loc[primaveraFMO[1] == 1]
V2p = primaveraFMO.loc[primaveraFMO[1] == 2]
V3p = primaveraFMO.loc[primaveraFMO[1] == 3]
V4p = primaveraFMO.loc[primaveraFMO[1] == 4]
V5p = primaveraFMO.loc[primaveraFMO[1] == 5]
V6p = primaveraFMO.loc[primaveraFMO[1] == 6]
V7p = primaveraFMO.loc[primaveraFMO[1] == 7]
V8p = primaveraFMO.loc[primaveraFMO[1] == 8]

verfmo = [len(V1v),len(V2v),len(V3v),len(V4v),len(V5v),len(V6v),len(V7v),len(V8v)]
otofmo = [len(V1o),len(V2o),len(V3o),len(V4o),len(V5o),len(V6o),len(V7o),len(V8o)]
invfmo = [len(V1i),len(V2i),len(V3i),len(V4i),len(V5i),len(V6i),len(V7i),len(V8i)]
prifmo = [len(V1p),len(V2p),len(V3p),len(V4p),len(V5p),len(V6p),len(V7p),len(V8p)]

X = [1,2,3,4,5,6,7,8]

fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8)) = plt.subplots(2, 4,figsize=(6.75,3), sharey= True, sharex=True)

ax1.set_title('DJF  ', fontsize=13, weight='bold')
ax1.bar(X, verwh, alpha = 1)
ax1.tick_params(labelsize=14)
ax1.set_yticks([100,200,300], ['100','200','300'])
ax1.xaxis.set_tick_params(length=0)

ax2.set_title('MAM  ', fontsize=13, weight='bold')
ax2.bar(X, otowh, alpha = 1)
ax2.tick_params(labelsize=14)
ax2.xaxis.set_tick_params(length=0)
ax2.yaxis.set_tick_params(length=0)

ax3.set_title('JJA  ', fontsize=13, weight='bold')
ax3.bar(X, invwh, alpha = 1)
ax3.tick_params(labelsize=14)
ax3.xaxis.set_tick_params(length=0)
ax3.yaxis.set_tick_params(length=0)

ax4.set_title('SON  ', fontsize=13, weight='bold')
ax4.bar(X, priwh, alpha = 1)
ax4.tick_params(labelsize=14)
ax4.xaxis.set_tick_params(length=0)
ax4.yaxis.set_tick_params(length=0)

ax5.bar(X, verfmo, alpha = 1)
ax5.tick_params(labelsize=14)
ax5.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax5.set_yticks([100,200,300], ['100','200','300'])

ax6.bar(X, otofmo, alpha = 1)
ax6.tick_params(labelsize=14)
ax6.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax6.yaxis.set_tick_params(length=0)

ax7.bar(X, invfmo, alpha = 1)
ax7.tick_params(labelsize=14)
ax7.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax7.yaxis.set_tick_params(length=0)

ax8.bar(X, prifmo, alpha = 1)
ax8.tick_params(labelsize=14)
ax8.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax8.yaxis.set_tick_params(length=0)

fig.text(0.01, 0.42, '# cases', fontsize=14, rotation='vertical')
fig.text(0.91, 0.62, 'W&H', fontsize=14, rotation='vertical')
fig.text(0.91, 0.24, 'FMO', fontsize=14, rotation='vertical')
fig.text(0.45, -0.05, 'MJO phase', fontsize=14)
fig.subplots_adjust(wspace=0.08,hspace=0.08)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/casos.png',bbox_inches="tight", dpi=600)
