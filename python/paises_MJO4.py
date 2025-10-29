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

# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series = series.loc[series[3] > 1]

## calculamos los promedios estacionales de las series crudas. Esto sirve para sacar los porcentajes

Vuru_c_ver = Vuru_cruda.loc[(Vuru_cruda[1] == 1) | (Vuru_cruda[1] == 2) | (Vuru_cruda[1] == 12)]
Vuru_c_oto = Vuru_cruda.loc[(Vuru_cruda[1] == 3) | (Vuru_cruda[1] == 4) | (Vuru_cruda[1] == 5)]
Vuru_c_inv = Vuru_cruda.loc[(Vuru_cruda[1] == 6) | (Vuru_cruda[1] == 7) | (Vuru_cruda[1] == 8)]
Vuru_c_pri = Vuru_cruda.loc[(Vuru_cruda[1] == 9) | (Vuru_cruda[1] == 10) |(Vuru_cruda[1] == 11)]

Vuru_p_v = 100/Vuru_c_ver[3].mean()
Vuru_p_o = 100/Vuru_c_oto[3].mean()
Vuru_p_i = 100/Vuru_c_inv[3].mean()
Vuru_p_p = 100/Vuru_c_pri[3].mean()

Vchi_c_ver = Vchi_cruda.loc[(Vchi_cruda[1] == 1) | (Vchi_cruda[1] == 2) | (Vchi_cruda[1] == 12)]
Vchi_c_oto = Vchi_cruda.loc[(Vchi_cruda[1] == 3) | (Vchi_cruda[1] == 4) | (Vchi_cruda[1] == 5)]
Vchi_c_inv = Vchi_cruda.loc[(Vchi_cruda[1] == 6) | (Vchi_cruda[1] == 7) | (Vchi_cruda[1] == 8)]
Vchi_c_pri = Vchi_cruda.loc[(Vchi_cruda[1] == 9) | (Vchi_cruda[1] == 10) | (Vchi_cruda[1] == 11)]

Vchi_p_v = 100/Vchi_c_ver[3].mean()
Vchi_p_o = 100/Vchi_c_oto[3].mean()
Vchi_p_i = 100/Vchi_c_inv[3].mean()
Vchi_p_p = 100/Vchi_c_pri[3].mean()

Varg_c_ver = Varg_cruda.loc[(Varg_cruda[1] == 1) | (Varg_cruda[1] == 2) | (Varg_cruda[1] == 12)]
Varg_c_oto = Varg_cruda.loc[(Varg_cruda[1] == 3) | (Varg_cruda[1] == 4) | (Varg_cruda[1] == 5)]
Varg_c_inv = Varg_cruda.loc[(Varg_cruda[1] == 6) | (Varg_cruda[1] == 7) | (Varg_cruda[1] == 8)]
Varg_c_pri = Varg_cruda.loc[(Varg_cruda[1] == 9) | (Varg_cruda[1] == 10) | (Varg_cruda[1] == 11)]

Varg_p_v = 100/Varg_c_ver[3].mean()
Varg_p_o = 100/Varg_c_oto[3].mean()
Varg_p_i = 100/Varg_c_inv[3].mean()
Varg_p_p = 100/Varg_c_pri[3].mean()

# VERANO
verano = series.loc[(series[0] == 1) | (series[0] == 2) | (series[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series.loc[(series[0] == 3) | (series[0] == 4) | (series[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series.loc[(series[0] == 6) | (series[0] == 7) | (series[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series.loc[(series[0] == 9) | (series[0] == 10) | (series[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

X = [1,2,3,4,5,6,7,8]

fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4, 3,figsize=(6.75,4.75), sharex= True)

########## argentina

ax1.set_title('Argentina  ', fontsize=13, weight='bold')
ax1.bar(X, Vargver, color = 'mediumblue', alpha = 1)
ax1.tick_params(labelsize=14)
ax1.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax1.set_yticks([-3,3], ['-3','3'])
ax1.set_ylim(-6,6)
ax1.xaxis.set_tick_params(length=0)

ax4.bar(X, Vargoto, color = 'mediumblue', alpha = 1)
ax4.tick_params(labelsize=14)
ax4.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax4.set_yticks([-3,3], ['-3','3'])
ax4.set_ylim(-6,6)
ax4.xaxis.set_tick_params(length=0)

ax7.bar(X, Varginv, color = 'mediumblue', alpha = 1)
ax7.tick_params(labelsize=14)
ax7.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax7.set_yticks([-3,3], ['-3','3'])
ax7.set_ylim(-6,6)
ax7.xaxis.set_tick_params(length=0)

ax10.bar(X, Vargpri, color = 'mediumblue', alpha = 1, label= 'power demand')
ax10.tick_params(labelsize=14)
ax10.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax10.set_yticks([-3,3], ['-3','3'])
ax10.set_ylim(-6,6)
ax10.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])

# ~ ax4.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=14).get_frame().set_edgecolor("white")

########## uruguay
ax2.set_title('Uruguay  ', fontsize=13, weight='bold')
ax2.bar(X, Vuruver, color = 'mediumblue', alpha = 1)
ax2.tick_params(labelsize=14)
ax2.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax2.set_yticks([-5,5], ['-5','5'])
ax2.set_ylim(-8,8)
ax2.xaxis.set_tick_params(length=0)

ax5.bar(X, Vuruoto, color = 'mediumblue', alpha = 1)
ax5.tick_params(labelsize=14)
ax5.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax5.set_yticks([-5,5], ['-5','5'])
ax5.set_ylim(-8,8)
ax5.xaxis.set_tick_params(length=0)

ax8.bar(X, Vuruinv, color = 'mediumblue', alpha = 1)
ax8.tick_params(labelsize=14)
ax8.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax8.set_yticks([-5,5], ['-5','5'])
ax8.set_ylim(-8,8)
ax8.xaxis.set_tick_params(length=0)

ax11.bar(X, Vurupri, color = 'mediumblue', alpha = 1)
ax11.tick_params(labelsize=14)
ax11.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax11.set_yticks([-5,5], ['-5','5'])
ax11.set_ylim(-8,8)
ax11.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])

########## chile
ax3.set_title('Chile  ', fontsize=13, weight='bold')
ax3.bar(X, Vchiver, color = 'mediumblue', alpha = 1)
ax3.tick_params(labelsize=14)
ax3.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax3.set_yticks([-2,2], ['-2','2'])
ax3.set_ylim(-3.8,3.8)
ax3.xaxis.set_tick_params(length=0)

ax6.bar(X, Vchioto, color = 'mediumblue', alpha = 1)
ax6.tick_params(labelsize=14)
ax6.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax6.set_yticks([-2,2], ['-2','2'])
ax6.set_ylim(-3.8,3.8)
ax6.xaxis.set_tick_params(length=0)

ax9.bar(X, Vchiinv, color = 'mediumblue', alpha = 1)
ax9.tick_params(labelsize=14)
ax9.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax9.set_yticks([-2,2], ['-2','2'])
ax9.set_ylim(-3.8,3.8)
ax9.xaxis.set_tick_params(length=0)

ax12.bar(X, Vchipri, color = 'mediumblue', alpha = 1)
ax12.tick_params(labelsize=14)
ax12.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax12.set_yticks([-2,2], ['-2','2'])
ax12.set_ylim(-3.8,3.8)
ax12.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])

fig.text(0.91, 0.77, 'DJF', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.57, 'MAM', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.39, 'JJA', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.19, 'SON', fontsize = 14, rotation='vertical')
fig.text(0.05, 0.42, 'variation [%]', fontsize=14, rotation='vertical')
fig.text(0.45, 0.05, 'MJO phase', fontsize=14)
fig.subplots_adjust(wspace=0.2, hspace=0.08)
fig.subplots_adjust(bottom=0.15)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/paisesV.png',bbox_inches="tight", dpi=600)

#################################
#######SOL####################
#################################

Suru = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-sol-agrup.csv', header=None, delimiter=',', na_values='-99')
Sarg = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-sol-agrup.csv', header=None, delimiter=',', na_values='-99')
Schi = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-sol-agrup.csv', header=None, delimiter=',', na_values='-99')

Suru_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-sol.txt', header=None, delimiter=';', na_values='-99')
Sarg_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-sol.txt', header=None, delimiter=';', na_values='-99')
Schi_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-sol.txt', header=None, delimiter=';', na_values='-99')

mad = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day oSf week, RMM1, RMM2, phase, amplitude

series = pd.DataFrame()
# cSargamos mes, para despues Sfiltrar por estacion
series[0] = mad[1]
# cSargamos Sfase
series[1] = mad[6]
# cSargamos dia de la semana, para cuando trabajemos con demanda
series[2] = mad[3]
#  cSargamos amplitud, para quedarnos con MJO activas
series[3] = mad[7]
# series Suruguay Sargentina Schile
series[4] = Suru[1]
series[5] = Sarg[1]
series[6] = Schi[1]

# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series = series.loc[series[3] > 1]

## calculamos los promedios estacionales de las series crudas. Esto sirve para sacar los porcentajes

Suru_c_ver = Suru_cruda.loc[(Suru_cruda[1] == 1) | (Suru_cruda[1] == 2) | (Suru_cruda[1] == 12)]
Suru_c_oto = Suru_cruda.loc[(Suru_cruda[1] == 3) | (Suru_cruda[1] == 4) | (Suru_cruda[1] == 5)]
Suru_c_inv = Suru_cruda.loc[(Suru_cruda[1] == 6) | (Suru_cruda[1] == 7) | (Suru_cruda[1] == 8)]
Suru_c_pri = Suru_cruda.loc[(Suru_cruda[1] == 9) | (Suru_cruda[1] == 10) | (Suru_cruda[1] == 11)]

Suru_p_v = 100/Suru_c_ver[3].mean()
Suru_p_o = 100/Suru_c_oto[3].mean()
Suru_p_i = 100/Suru_c_inv[3].mean()
Suru_p_p = 100/Suru_c_pri[3].mean()

Schi_c_ver = Schi_cruda.loc[(Schi_cruda[1] == 1) | (Schi_cruda[1] == 2) | (Schi_cruda[1] == 12)]
Schi_c_oto = Schi_cruda.loc[(Schi_cruda[1] == 3) | (Schi_cruda[1] == 4) | (Schi_cruda[1] == 5)]
Schi_c_inv = Schi_cruda.loc[(Schi_cruda[1] == 6) | (Schi_cruda[1] == 7) | (Schi_cruda[1] == 8)]
Schi_c_pri = Schi_cruda.loc[(Schi_cruda[1] == 9) | (Schi_cruda[1] == 10) | (Schi_cruda[1] == 11)]

Schi_p_v = 100/Schi_c_ver[3].mean()
Schi_p_o = 100/Schi_c_oto[3].mean()
Schi_p_i = 100/Schi_c_inv[3].mean()
Schi_p_p = 100/Schi_c_pri[3].mean()

Sarg_c_ver = Sarg_cruda.loc[(Sarg_cruda[1] == 1) | (Sarg_cruda[1] == 2) | (Sarg_cruda[1] == 12)]
Sarg_c_oto = Sarg_cruda.loc[(Sarg_cruda[1] == 3) | (Sarg_cruda[1] == 4) | (Sarg_cruda[1] == 5)]
Sarg_c_inv = Sarg_cruda.loc[(Sarg_cruda[1] == 6) | (Sarg_cruda[1] == 7) | (Sarg_cruda[1] == 8)]
Sarg_c_pri = Sarg_cruda.loc[(Sarg_cruda[1] == 9) | (Sarg_cruda[1] == 10) | (Sarg_cruda[1] == 11)]

Sarg_p_v = 100/Sarg_c_ver[3].mean()
Sarg_p_o = 100/Sarg_c_oto[3].mean()
Sarg_p_i = 100/Sarg_c_inv[3].mean()
Sarg_p_p = 100/Sarg_c_pri[3].mean()

# VERANO
verano = series.loc[(series[0] == 1) | (series[0] == 2) | (series[0] == 12)]
Sf1v = verano.loc[verano[1] == 1]
Sf2v = verano.loc[verano[1] == 2]
Sf3v = verano.loc[verano[1] == 3]
Sf4v = verano.loc[verano[1] == 4]
Sf5v = verano.loc[verano[1] == 5]
Sf6v = verano.loc[verano[1] == 6]
Sf7v = verano.loc[verano[1] == 7]
Sf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series.loc[(series[0] == 3) | (series[0] == 4) | (series[0] == 5)]
Sf1o = otono.loc[otono[1] == 1]
Sf2o = otono.loc[otono[1] == 2]
Sf3o = otono.loc[otono[1] == 3]
Sf4o = otono.loc[otono[1] == 4]
Sf5o = otono.loc[otono[1] == 5]
Sf6o = otono.loc[otono[1] == 6]
Sf7o = otono.loc[otono[1] == 7]
Sf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series.loc[(series[0] == 6) | (series[0] == 7) | (series[0] == 8)]
Sf1i = invierno.loc[invierno[1] == 1]
Sf2i = invierno.loc[invierno[1] == 2]
Sf3i = invierno.loc[invierno[1] == 3]
Sf4i = invierno.loc[invierno[1] == 4]
Sf5i = invierno.loc[invierno[1] == 5]
Sf6i = invierno.loc[invierno[1] == 6]
Sf7i = invierno.loc[invierno[1] == 7]
Sf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series.loc[(series[0] == 9) | (series[0] == 10) | (series[0] == 11)]
Sf1p = primavera.loc[primavera[1] == 1]
Sf2p = primavera.loc[primavera[1] == 2]
Sf3p = primavera.loc[primavera[1] == 3]
Sf4p = primavera.loc[primavera[1] == 4]
Sf5p = primavera.loc[primavera[1] == 5]
Sf6p = primavera.loc[primavera[1] == 6]
Sf7p = primavera.loc[primavera[1] == 7]
Sf8p = primavera.loc[primavera[1] == 8]

Suruver = [Sf1v[4].mean()*Suru_p_v,Sf2v[4].mean()*Suru_p_v,Sf3v[4].mean()*Suru_p_v,Sf4v[4].mean()*Suru_p_v,Sf5v[4].mean()*Suru_p_v,Sf6v[4].mean()*Suru_p_v,Sf7v[4].mean()*Suru_p_v,Sf8v[4].mean()*Suru_p_v ]
Sargver = [Sf1v[5].mean()*Sarg_p_v,Sf2v[5].mean()*Sarg_p_v,Sf3v[5].mean()*Sarg_p_v,Sf4v[5].mean()*Sarg_p_v,Sf5v[5].mean()*Sarg_p_v,Sf6v[5].mean()*Sarg_p_v,Sf7v[5].mean()*Sarg_p_v,Sf8v[5].mean()*Sarg_p_v ]
Schiver = [Sf1v[6].mean()*Schi_p_v,Sf2v[6].mean()*Schi_p_v,Sf3v[6].mean()*Schi_p_v,Sf4v[6].mean()*Schi_p_v,Sf5v[6].mean()*Schi_p_v,Sf6v[6].mean()*Schi_p_v,Sf7v[6].mean()*Schi_p_v,Sf8v[6].mean()*Schi_p_v ]

Suruoto = [Sf1o[4].mean()*Suru_p_o,Sf2o[4].mean()*Suru_p_o,Sf3o[4].mean()*Suru_p_o,Sf4o[4].mean()*Suru_p_o,Sf5o[4].mean()*Suru_p_o,Sf6o[4].mean()*Suru_p_o,Sf7o[4].mean()*Suru_p_o,Sf8o[4].mean()*Suru_p_o ]
Sargoto = [Sf1o[5].mean()*Sarg_p_o,Sf2o[5].mean()*Sarg_p_o,Sf3o[5].mean()*Sarg_p_o,Sf4o[5].mean()*Sarg_p_o,Sf5o[5].mean()*Sarg_p_o,Sf6o[5].mean()*Sarg_p_o,Sf7o[5].mean()*Sarg_p_o,Sf8o[5].mean()*Sarg_p_o ]
Schioto = [Sf1o[6].mean()*Schi_p_o,Sf2o[6].mean()*Schi_p_o,Sf3o[6].mean()*Schi_p_o,Sf4o[6].mean()*Schi_p_o,Sf5o[6].mean()*Schi_p_o,Sf6o[6].mean()*Schi_p_o,Sf7o[6].mean()*Schi_p_o,Sf8o[6].mean()*Schi_p_o ]

Suruinv = [Sf1i[4].mean()*Suru_p_i,Sf2i[4].mean()*Suru_p_i,Sf3i[4].mean()*Suru_p_i,Sf4i[4].mean()*Suru_p_i,Sf5i[4].mean()*Suru_p_i,Sf6i[4].mean()*Suru_p_i,Sf7i[4].mean()*Suru_p_i,Sf8i[4].mean()*Suru_p_i ]
Sarginv = [Sf1i[5].mean()*Sarg_p_i,Sf2i[5].mean()*Sarg_p_i,Sf3i[5].mean()*Sarg_p_i,Sf4i[5].mean()*Sarg_p_i,Sf5i[5].mean()*Sarg_p_i,Sf6i[5].mean()*Sarg_p_i,Sf7i[5].mean()*Sarg_p_i,Sf8i[5].mean()*Sarg_p_i ]
Schiinv = [Sf1i[6].mean()*Schi_p_i,Sf2i[6].mean()*Schi_p_i,Sf3i[6].mean()*Schi_p_i,Sf4i[6].mean()*Schi_p_i,Sf5i[6].mean()*Schi_p_i,Sf6i[6].mean()*Schi_p_i,Sf7i[6].mean()*Schi_p_i,Sf8i[6].mean()*Schi_p_i ]

Surupri = [Sf1p[4].mean()*Suru_p_p,Sf2p[4].mean()*Suru_p_p,Sf3p[4].mean()*Suru_p_p,Sf4p[4].mean()*Suru_p_p,Sf5p[4].mean()*Suru_p_p,Sf6p[4].mean()*Suru_p_p,Sf7p[4].mean()*Suru_p_p,Sf8p[4].mean()*Suru_p_p ]
Sargpri = [Sf1p[5].mean()*Sarg_p_p,Sf2p[5].mean()*Sarg_p_p,Sf3p[5].mean()*Sarg_p_p,Sf4p[5].mean()*Sarg_p_p,Sf5p[5].mean()*Sarg_p_p,Sf6p[5].mean()*Sarg_p_p,Sf7p[5].mean()*Sarg_p_p,Sf8p[5].mean()*Sarg_p_p ]
Schipri = [Sf1p[6].mean()*Schi_p_p,Sf2p[6].mean()*Schi_p_p,Sf3p[6].mean()*Schi_p_p,Sf4p[6].mean()*Schi_p_p,Sf5p[6].mean()*Schi_p_p,Sf6p[6].mean()*Schi_p_p,Sf7p[6].mean()*Schi_p_p,Sf8p[6].mean()*Schi_p_p ]

fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4, 3,figsize=(6.75,4.75), sharex= True)

########## argentina

ax1.set_title('Argentina  ', fontsize=13, weight='bold')
ax1.bar(X, Sargver, color = 'orangered', alpha = 1)
ax1.tick_params(labelsize=14)
ax1.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax1.set_yticks([-2,2], ['-2','2'])
ax1.set_ylim(-4.5,4.5)
ax1.xaxis.set_tick_params(length=0)

ax4.bar(X, Sargoto, color = 'orangered', alpha = 1)
ax4.tick_params(labelsize=14)
ax4.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax4.set_yticks([-2,2], ['-2','2'])
ax4.set_ylim(-4.5,4.5)
ax4.xaxis.set_tick_params(length=0)

ax7.bar(X, Sarginv, color = 'orangered', alpha = 1)
ax7.tick_params(labelsize=14)
ax7.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax7.set_yticks([-2,2], ['-2','2'])
ax7.set_ylim(-4.5,4.5)
ax7.xaxis.set_tick_params(length=0)

ax10.bar(X, Sargpri, color = 'orangered', alpha = 1, label= 'power demand')
ax10.tick_params(labelsize=14)
ax10.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax10.set_yticks([-2,2], ['-2','2'])
ax10.set_ylim(-4.5,4.5)
ax10.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])

# ~ ax4.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=14).get_frame().set_edgecolor("white")

########## uruguay
ax2.set_title('Uruguay  ', fontsize=13, weight='bold')
ax2.bar(X, Suruver, color = 'orangered', alpha = 1)
ax2.tick_params(labelsize=14)
ax2.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax2.set_yticks([-5,5], ['-5','5'])
ax2.set_ylim(-10,10)
ax2.xaxis.set_tick_params(length=0)

ax5.bar(X, Suruoto, color = 'orangered', alpha = 1)
ax5.tick_params(labelsize=14)
ax5.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax5.set_yticks([-5,5], ['-5','5'])
ax5.set_ylim(-10,10)
ax5.xaxis.set_tick_params(length=0)

ax8.bar(X, Suruinv, color = 'orangered', alpha = 1)
ax8.tick_params(labelsize=14)
ax8.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax8.set_yticks([-5,5], ['-5','5'])
ax8.set_ylim(-10,10)
ax8.xaxis.set_tick_params(length=0)

ax11.bar(X, Surupri, color = 'orangered', alpha = 1)
ax11.tick_params(labelsize=14)
ax11.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax11.set_yticks([-5,5], ['-5','5'])
ax11.set_ylim(-10,10)
ax11.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])

########## chile
ax3.set_title('Chile  ', fontsize=13, weight='bold')
ax3.bar(X, Schiver, color = 'orangered', alpha = 1)
ax3.tick_params(labelsize=14)
ax3.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax3.set_yticks([-2,2], ['-2','2'])
ax3.set_ylim(-3.8,3.8)
ax3.xaxis.set_tick_params(length=0)

ax6.bar(X, Schioto, color = 'orangered', alpha = 1)
ax6.tick_params(labelsize=14)
ax6.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax6.set_yticks([-2,2], ['-2','2'])
ax6.set_ylim(-3.8,3.8)
ax6.xaxis.set_tick_params(length=0)

ax9.bar(X, Schiinv, color = 'orangered', alpha = 1)
ax9.tick_params(labelsize=14)
ax9.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax9.set_yticks([-2,2], ['-2','2'])
ax9.set_ylim(-3.8,3.8)
ax9.xaxis.set_tick_params(length=0)

ax12.bar(X, Schipri, color = 'orangered', alpha = 1)
ax12.tick_params(labelsize=14)
ax12.axhline(y=0, color="orangered", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax12.set_yticks([-2,2], ['-2','2'])
ax12.set_ylim(-3.8,3.8)
ax12.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])

fig.text(0.91, 0.77, 'DJF', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.57, 'MAM', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.39, 'JJA', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.19, 'SON', fontsize = 14, rotation='vertical')
fig.text(0.05, 0.42, 'variation [%]', fontsize=14, rotation='vertical')
fig.text(0.45, 0.05, 'MJO phase', fontsize=14)
fig.subplots_adjust(wspace=0.2, hspace=0.08)
fig.subplots_adjust(bottom=0.15)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/paisesS.png',bbox_inches="tight", dpi=600)


#################################
#######DEMANDA####################
#################################

Duru = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/uru-dem-agrup.csv', header=None, delimiter=',', na_values='-99')
Darg = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/arg-dem-agrup.csv', header=None, delimiter=',', na_values='-99')
Dchi = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/chi-dem-agrup2.csv', header=None, delimiter=',', na_values='-99')


Duru_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/uru-dem.txt', header=None, delimiter=';')
Darg_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/arg-dem.txt', header=None, delimiter=';')
Dchi_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/chi-dem2.txt', header=None, delimiter=';')

mad = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2011.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day oDf week, RMM1, RMM2, phase, amplitude
mad2 = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2014.txt', header=None, delimiter=',', na_values='-99')
mad3 = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2007.txt', header=None, delimiter=',', na_values='-99')

## aca hay que armar dataDframes diDferentes por que las series de demanda tienen longitudes diDferentes
#### DuruGUAY
series = pd.DataFrame()
# cDargamos mes, para despues Dfiltrar por estacion
series[0] = mad[1]
# cDargamos Dfase
series[1] = mad[6]
# cDargamos dia de la semana, para cuando trabajemos con demanda
series[2] = mad[3]
#  cDargamos amplitud, para quedarnos con MJO activas
series[3] = mad[7]
# series Duruguay Dargentina Dchile
# ~ series[4] = Duru[1]*10
series[4] = Duru[1]
## calculamos los promedios estacionales de las series crudas. Esto sirve para sacar los porcentajes

Duru_c_ver = Duru_cruda.loc[(Duru_cruda[1] == 1) | (Duru_cruda[1] == 2) | (Duru_cruda[1] == 12)]
Duru_c_oto = Duru_cruda.loc[(Duru_cruda[1] == 3) | (Duru_cruda[1] == 4) | (Duru_cruda[1] == 5)]
Duru_c_inv = Duru_cruda.loc[(Duru_cruda[1] == 6) | (Duru_cruda[1] == 7) | (Duru_cruda[1] == 8)]
Duru_c_pri = Duru_cruda.loc[(Duru_cruda[1] == 9) | (Duru_cruda[1] == 10) | (Duru_cruda[1] == 11)]

Duru_p_v = 100/Duru_c_ver[3].mean()
Duru_p_o = 100/Duru_c_oto[3].mean()
Duru_p_i = 100/Duru_c_inv[3].mean()
Duru_p_p = 100/Duru_c_pri[3].mean()

Dchi_c_ver = Dchi_cruda.loc[(Dchi_cruda[1] == 1) | (Dchi_cruda[1] == 2) | (Dchi_cruda[1] == 12)]
Dchi_c_oto = Dchi_cruda.loc[(Dchi_cruda[1] == 3) | (Dchi_cruda[1] == 4) | (Dchi_cruda[1] == 5)]
Dchi_c_inv = Dchi_cruda.loc[(Dchi_cruda[1] == 6) | (Dchi_cruda[1] == 7) | (Dchi_cruda[1] == 8)]
Dchi_c_pri = Dchi_cruda.loc[(Dchi_cruda[1] == 9) | (Dchi_cruda[1] == 10) | (Dchi_cruda[1] == 11)]

Dchi_p_v = 100/Dchi_c_ver[3].mean()
Dchi_p_o = 100/Dchi_c_oto[3].mean()
Dchi_p_i = 100/Dchi_c_inv[3].mean()
Dchi_p_p = 100/Dchi_c_pri[3].mean()

Darg_c_ver = Darg_cruda.loc[(Darg_cruda[1] == 1) | (Darg_cruda[1] == 2) | (Darg_cruda[1] == 12)]
Darg_c_oto = Darg_cruda.loc[(Darg_cruda[1] == 3) | (Darg_cruda[1] == 4) | (Darg_cruda[1] == 5)]
Darg_c_inv = Darg_cruda.loc[(Darg_cruda[1] == 6) | (Darg_cruda[1] == 7) | (Darg_cruda[1] == 8)]
Darg_c_pri = Darg_cruda.loc[(Darg_cruda[1] == 9) | (Darg_cruda[1] == 10) | (Darg_cruda[1] == 11)]

#Dargentina multiplico x 1000 x que esta en gigas
Darg_p_v = 100/(1000*Darg_c_ver[3].mean())
Darg_p_o = 100/(1000*Darg_c_oto[3].mean())
Darg_p_i = 100/(1000*Darg_c_inv[3].mean())
Darg_p_p = 100/(1000*Darg_c_pri[3].mean())

# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series = series.loc[series[3] > 1]
# sacamos los Dfines de semana
series = series.loc[(series[2] == 1) | (series[2] == 2) | (series[2] == 3) | (series[2] == 1) | (series[2] == 5)]

# VERANO
verano_U = series.loc[(series[0] == 1) | (series[0] == 2) | (series[0] == 12)]
Df1Uv = verano_U.loc[verano_U[1] == 1]
Df2Uv = verano_U.loc[verano_U[1] == 2]
Df3Uv = verano_U.loc[verano_U[1] == 3]
Df4Uv = verano_U.loc[verano_U[1] == 4]
Df5Uv = verano_U.loc[verano_U[1] == 5]
Df6Uv = verano_U.loc[verano_U[1] == 6]
Df7Uv = verano_U.loc[verano_U[1] == 7]
Df8Uv = verano_U.loc[verano_U[1] == 8]

# OTOÑO
otono_U = series.loc[(series[0] == 3) | (series[0] == 4) | (series[0] == 5)]
Df1Uo = otono_U.loc[otono_U[1] == 1]
Df2Uo = otono_U.loc[otono_U[1] == 2]
Df3Uo = otono_U.loc[otono_U[1] == 3]
Df4Uo = otono_U.loc[otono_U[1] == 4]
Df5Uo = otono_U.loc[otono_U[1] == 5]
Df6Uo = otono_U.loc[otono_U[1] == 6]
Df7Uo = otono_U.loc[otono_U[1] == 7]
Df8Uo = otono_U.loc[otono_U[1] == 8]

# INVIERNO
invierno_U = series.loc[(series[0] == 6) | (series[0] == 7) | (series[0] == 8)]
Df1Ui = invierno_U.loc[invierno_U[1] == 1]
Df2Ui = invierno_U.loc[invierno_U[1] == 2]
Df3Ui = invierno_U.loc[invierno_U[1] == 3]
Df4Ui = invierno_U.loc[invierno_U[1] == 4]
Df5Ui = invierno_U.loc[invierno_U[1] == 5]
Df6Ui = invierno_U.loc[invierno_U[1] == 6]
Df7Ui = invierno_U.loc[invierno_U[1] == 7]
Df8Ui = invierno_U.loc[invierno_U[1] == 8]

# primavera
primavera_U = series.loc[(series[0] == 9) | (series[0] == 10) | (series[0] == 11)]
Df1Up = primavera_U.loc[primavera_U[1] == 1]
Df2Up = primavera_U.loc[primavera_U[1] == 2]
Df3Up = primavera_U.loc[primavera_U[1] == 3]
Df4Up = primavera_U.loc[primavera_U[1] == 4]
Df5Up = primavera_U.loc[primavera_U[1] == 5]
Df6Up = primavera_U.loc[primavera_U[1] == 6]
Df7Up = primavera_U.loc[primavera_U[1] == 7]
Df8Up = primavera_U.loc[primavera_U[1] == 8]

Duruver = [Df1Uv[4].mean()*Duru_p_v,Df2Uv[4].mean()*Duru_p_v,Df3Uv[4].mean()*Duru_p_v,Df4Uv[4].mean()*Duru_p_v,Df5Uv[4].mean()*Duru_p_v,Df6Uv[4].mean()*Duru_p_v,Df7Uv[4].mean()*Duru_p_v,Df8Uv[4].mean()*Duru_p_v]
Duruver10 = [Df1Uv[4].quantile(.3)*Duru_p_v,Df2Uv[4].quantile(.3)*Duru_p_v,Df3Uv[4].quantile(.3)*Duru_p_v,Df4Uv[4].quantile(.3)*Duru_p_v,Df5Uv[4].quantile(.3)*Duru_p_v,Df6Uv[4].quantile(.3)*Duru_p_v,Df7Uv[4].quantile(.3)*Duru_p_v,Df8Uv[4].quantile(.3)*Duru_p_v]
Duruver90 = [Df1Uv[4].quantile(.7)*Duru_p_v,Df2Uv[4].quantile(.7)*Duru_p_v,Df3Uv[4].quantile(.7)*Duru_p_v,Df4Uv[4].quantile(.7)*Duru_p_v,Df5Uv[4].quantile(.7)*Duru_p_v,Df6Uv[4].quantile(.7)*Duru_p_v,Df7Uv[4].quantile(.7)*Duru_p_v,Df8Uv[4].quantile(.7)*Duru_p_v]
Duruoto = [Df1Uo[4].mean()*Duru_p_o,Df2Uo[4].mean()*Duru_p_o,Df3Uo[4].mean()*Duru_p_o,Df4Uo[4].mean()*Duru_p_o,Df5Uo[4].mean()*Duru_p_o,Df6Uo[4].mean()*Duru_p_o,Df7Uo[4].mean()*Duru_p_o,Df8Uo[4].mean()*Duru_p_o ]
Duruinv = [Df1Ui[4].mean()*Duru_p_i,Df2Ui[4].mean()*Duru_p_i,Df3Ui[4].mean()*Duru_p_i,Df4Ui[4].mean()*Duru_p_i,Df5Ui[4].mean()*Duru_p_i,Df6Ui[4].mean()*Duru_p_i,Df7Ui[4].mean()*Duru_p_i,Df8Ui[4].mean()*Duru_p_i ]
Durupri = [Df1Up[4].mean()*Duru_p_p,Df2Up[4].mean()*Duru_p_p,Df3Up[4].mean()*Duru_p_p,Df4Up[4].mean()*Duru_p_p,Df5Up[4].mean()*Duru_p_p,Df6Up[4].mean()*Duru_p_p,Df7Up[4].mean()*Duru_p_p,Df8Up[4].mean()*Duru_p_p ]

#### DchiLE
series2 = pd.DataFrame()
# cDargamos mes, para despues Dfiltrar por estacion
series2[0] = mad2[1]
# cDargamos Dfase
series2[1] = mad2[6]
# cDargamos dia de la semana, para cuando trabajemos con demanda
series2[2] = mad2[3]
#  cDargamos amplitud, para quedarnos con MJO activas
series2[3] = mad2[7]
# series Duruguay Dargentina Dchile
series2[4] = Dchi[1]
# ~ print(series2)
# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series2 = series2.loc[series2[3] > 1]
# ~ print(series2)
# sacamos los Dfines de semana
series2 = series2.loc[(series2[2] == 1) | (series2[2] == 2) | (series2[2] == 3) | (series2[2] == 1) | (series2[2] == 5)]

# VERANO
verano_C = series2.loc[(series2[0] == 1) | (series2[0] == 2) | (series2[0] == 12)]
print(verano_C)
Df1Cv = verano_C.loc[verano_C[1] == 1]
Df2Cv = verano_C.loc[verano_C[1] == 2]
Df3Cv = verano_C.loc[verano_C[1] == 3]
Df4Cv = verano_C.loc[verano_C[1] == 4]
Df5Cv = verano_C.loc[verano_C[1] == 5]
Df6Cv = verano_C.loc[verano_C[1] == 6]
Df7Cv = verano_C.loc[verano_C[1] == 7]
Df8Cv = verano_C.loc[verano_C[1] == 8]

# OTOÑO
otono_C = series2.loc[(series2[0] == 3) | (series2[0] == 4) | (series2[0] == 5)]
Df1Co = otono_C.loc[otono_C[1] == 1]
Df2Co = otono_C.loc[otono_C[1] == 2]
Df3Co = otono_C.loc[otono_C[1] == 3]
Df4Co = otono_C.loc[otono_C[1] == 4]
Df5Co = otono_C.loc[otono_C[1] == 5]
Df6Co = otono_C.loc[otono_C[1] == 6]
Df7Co = otono_C.loc[otono_C[1] == 7]
Df8Co = otono_C.loc[otono_C[1] == 8]

# INVIERNO
invierno_C = series2.loc[(series2[0] == 6) | (series2[0] == 7) | (series2[0] == 8)]
Df1Ci = invierno_C.loc[invierno_C[1] == 1]
Df2Ci = invierno_C.loc[invierno_C[1] == 2]
Df3Ci = invierno_C.loc[invierno_C[1] == 3]
Df4Ci = invierno_C.loc[invierno_C[1] == 4]
Df5Ci = invierno_C.loc[invierno_C[1] == 5]
Df6Ci = invierno_C.loc[invierno_C[1] == 6]
Df7Ci = invierno_C.loc[invierno_C[1] == 7]
Df8Ci = invierno_C.loc[invierno_C[1] == 8]

# primavera
primavera_C = series2.loc[(series2[0] == 9) | (series2[0] == 10) | (series2[0] == 11)]
Df1Cp = primavera_C.loc[primavera_C[1] == 1]
Df2Cp = primavera_C.loc[primavera_C[1] == 2]
Df3Cp = primavera_C.loc[primavera_C[1] == 3]
Df4Cp = primavera_C.loc[primavera_C[1] == 4]
Df5Cp = primavera_C.loc[primavera_C[1] == 5]
Df6Cp = primavera_C.loc[primavera_C[1] == 6]
Df7Cp = primavera_C.loc[primavera_C[1] == 7]
Df8Cp = primavera_C.loc[primavera_C[1] == 8]

Dchiver = [Df1Cv[4].mean()*Dchi_p_v,Df2Cv[4].mean()*Dchi_p_v,Df3Cv[4].mean()*Dchi_p_v,Df4Cv[4].mean()*Dchi_p_v,Df5Cv[4].mean()*Dchi_p_v,Df6Cv[4].mean()*Dchi_p_v,Df7Cv[4].mean()*Dchi_p_v,Df8Cv[4].mean()*Dchi_p_v]
Dchiver10 = [Df1Cv[4].quantile(.3)*Dchi_p_v,Df2Cv[4].quantile(.3)*Dchi_p_v,Df3Cv[4].quantile(.3)*Dchi_p_v,Df4Cv[4].quantile(.3)*Dchi_p_v,Df5Cv[4].quantile(.3)*Dchi_p_v,Df6Cv[4].quantile(.3)*Dchi_p_v,Df7Cv[4].quantile(.3)*Dchi_p_v,Df8Cv[4].quantile(.3)*Dchi_p_v]
Dchiver90 = [Df1Cv[4].quantile(.7)*Dchi_p_v,Df2Cv[4].quantile(.7)*Dchi_p_v,Df3Cv[4].quantile(.7)*Dchi_p_v,Df4Cv[4].quantile(.7)*Dchi_p_v,Df5Cv[4].quantile(.7)*Dchi_p_v,Df6Cv[4].quantile(.7)*Dchi_p_v,Df7Cv[4].quantile(.7)*Dchi_p_v,Df8Cv[4].quantile(.7)*Dchi_p_v]
Dchioto = [Df1Co[4].mean()*Dchi_p_o,Df2Co[4].mean()*Dchi_p_o,Df3Co[4].mean()*Dchi_p_o,Df4Co[4].mean()*Dchi_p_o,Df5Co[4].mean()*Dchi_p_o,Df6Co[4].mean()*Dchi_p_o,Df7Co[4].mean()*Dchi_p_o,Df8Co[4].mean()*Dchi_p_o ]
Dchiinv = [Df1Ci[4].mean()*Dchi_p_i,Df2Ci[4].mean()*Dchi_p_i,Df3Ci[4].mean()*Dchi_p_i,Df4Ci[4].mean()*Dchi_p_i,Df5Ci[4].mean()*Dchi_p_i,Df6Ci[4].mean()*Dchi_p_i,Df7Ci[4].mean()*Dchi_p_i,Df8Ci[4].mean()*Dchi_p_i ]
Dchipri = [Df1Cp[4].mean()*Dchi_p_p,Df2Cp[4].mean()*Dchi_p_p,Df3Cp[4].mean()*Dchi_p_p,Df4Cp[4].mean()*Dchi_p_p,Df5Cp[4].mean()*Dchi_p_p,Df6Cp[4].mean()*Dchi_p_p,Df7Cp[4].mean()*Dchi_p_p,Df8Cp[4].mean()*Dchi_p_p ]

#### DargENTINA
series3 = pd.DataFrame()
# cDargamos mes, para despues Dfiltrar por estacion
series3[0] = mad3[1]
# cDargamos Dfase
series3[1] = mad3[6]
# cDargamos dia de la semana, para cuando trabajemos con demanda
series3[2] = mad3[3]
#  cDargamos amplitud, para quedarnos con MJO activas
series3[3] = mad3[7]
# series Duruguay Dargentina Dchile
series3[4] = Darg[1]*1000

# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series3 = series3.loc[series3[3] > 1]
# sacamos los Dfines de semana
series3 = series3.loc[(series3[2] == 1) | (series3[2] == 2) | (series3[2] == 3) | (series3[2] == 1) | (series3[2] == 5)]

# VERANO
verano_A = series3.loc[(series3[0] == 1) | (series3[0] == 2) | (series3[0] == 12)]
Df1Av = verano_A.loc[verano_A[1] == 1]
Df2Av = verano_A.loc[verano_A[1] == 2]
Df3Av = verano_A.loc[verano_A[1] == 3]
Df4Av = verano_A.loc[verano_A[1] == 4]
Df5Av = verano_A.loc[verano_A[1] == 5]
Df6Av = verano_A.loc[verano_A[1] == 6]
Df7Av = verano_A.loc[verano_A[1] == 7]
Df8Av = verano_A.loc[verano_A[1] == 8]

# OTOÑO
otono_A = series3.loc[(series3[0] == 3) | (series3[0] == 4) | (series3[0] == 5)]
Df1Ao = otono_A.loc[otono_A[1] == 1]
Df2Ao = otono_A.loc[otono_A[1] == 2]
Df3Ao = otono_A.loc[otono_A[1] == 3]
Df4Ao = otono_A.loc[otono_A[1] == 4]
Df5Ao = otono_A.loc[otono_A[1] == 5]
Df6Ao = otono_A.loc[otono_A[1] == 6]
Df7Ao = otono_A.loc[otono_A[1] == 7]
Df8Ao = otono_A.loc[otono_A[1] == 8]

# INVIERNO
invierno_A = series3.loc[(series3[0] == 6) | (series3[0] == 7) | (series3[0] == 8)]
Df1Ai = invierno_A.loc[invierno_A[1] == 1]
Df2Ai = invierno_A.loc[invierno_A[1] == 2]
Df3Ai = invierno_A.loc[invierno_A[1] == 3]
Df4Ai = invierno_A.loc[invierno_A[1] == 4]
Df5Ai = invierno_A.loc[invierno_A[1] == 5]
Df6Ai = invierno_A.loc[invierno_A[1] == 6]
Df7Ai = invierno_A.loc[invierno_A[1] == 7]
Df8Ai = invierno_A.loc[invierno_A[1] == 8]

# primavera
primavera_A = series3.loc[(series3[0] == 9) | (series3[0] == 10) | (series3[0] == 11)]
Df1Ap = primavera_A.loc[primavera_A[1] == 1]
Df2Ap = primavera_A.loc[primavera_A[1] == 2]
Df3Ap = primavera_A.loc[primavera_A[1] == 3]
Df4Ap = primavera_A.loc[primavera_A[1] == 4]
Df5Ap = primavera_A.loc[primavera_A[1] == 5]
Df6Ap = primavera_A.loc[primavera_A[1] == 6]
Df7Ap = primavera_A.loc[primavera_A[1] == 7]
Df8Ap = primavera_A.loc[primavera_A[1] == 8]

porc = 100/(1000*Darg_cruda[3].mean())

Dargver = [Df1Av[4].mean()*Darg_p_v,Df2Av[4].mean()*Darg_p_v,Df3Av[4].mean()*Darg_p_v,Df4Av[4].mean()*Darg_p_v,Df5Av[4].mean()*Darg_p_v,Df6Av[4].mean()*Darg_p_v,Df7Av[4].mean()*Darg_p_v,Df8Av[4].mean()*Darg_p_v]
Dargver10 = [Df1Av[4].quantile(.3)*Darg_p_v,Df2Av[4].quantile(.3)*Darg_p_v,Df3Av[4].quantile(.3)*Darg_p_v,Df4Av[4].quantile(.3)*Darg_p_v,Df5Av[4].quantile(.3)*Darg_p_v,Df6Av[4].quantile(.3)*Darg_p_v,Df7Av[4].quantile(.3)*Darg_p_v,Df8Av[4].quantile(.3)*Darg_p_v]
Dargver90 = [Df1Av[4].quantile(.7)*Darg_p_v,Df2Av[4].quantile(.7)*Darg_p_v,Df3Av[4].quantile(.7)*Darg_p_v,Df4Av[4].quantile(.7)*Darg_p_v,Df5Av[4].quantile(.7)*Darg_p_v,Df6Av[4].quantile(.7)*Darg_p_v,Df7Av[4].quantile(.7)*Darg_p_v,Df8Av[4].quantile(.7)*Darg_p_v]
Dargoto = [Df1Ao[4].mean()*Darg_p_o,Df2Ao[4].mean()*Darg_p_o,Df3Ao[4].mean()*Darg_p_o,Df4Ao[4].mean()*Darg_p_o,Df5Ao[4].mean()*Darg_p_o,Df6Ao[4].mean()*Darg_p_o,Df7Ao[4].mean()*Darg_p_o,Df8Ao[4].mean()*Darg_p_o ]
Darginv = [Df1Ai[4].mean()*Darg_p_i,Df2Ai[4].mean()*Darg_p_i,Df3Ai[4].mean()*Darg_p_i,Df4Ai[4].mean()*Darg_p_i,Df5Ai[4].mean()*Darg_p_i,Df6Ai[4].mean()*Darg_p_i,Df7Ai[4].mean()*Darg_p_i,Df8Ai[4].mean()*Darg_p_i ]
Dargpri = [Df1Ap[4].mean()*Darg_p_p,Df2Ap[4].mean()*Darg_p_p,Df3Ap[4].mean()*Darg_p_p,Df4Ap[4].mean()*Darg_p_p,Df5Ap[4].mean()*Darg_p_p,Df6Ap[4].mean()*Darg_p_p,Df7Ap[4].mean()*Darg_p_p,Df8Ap[4].mean()*Darg_p_p ]

fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4, 3,figsize=(6.75,4.75), sharex= True)

########## argentina

ax1.set_title('Argentina  ', fontsize=13, weight='bold')
ax1.bar(X, Dargver, color = 'black', alpha = 1)
ax1.tick_params(labelsize=14)
ax1.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax1.set_yticks([-2,2], ['-2','2'])
ax1.set_ylim(-4.5,4.5)
ax1.xaxis.set_tick_params(length=0)

ax4.bar(X, Dargoto, color = 'black', alpha = 1)
ax4.tick_params(labelsize=14)
ax4.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax4.set_yticks([-2,2], ['-2','2'])
ax4.set_ylim(-4.5,4.5)
ax4.xaxis.set_tick_params(length=0)

ax7.bar(X, Darginv, color = 'black', alpha = 1)
ax7.tick_params(labelsize=14)
ax7.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax7.set_yticks([-2,2], ['-2','2'])
ax7.set_ylim(-4.5,4.5)
ax7.xaxis.set_tick_params(length=0)

ax10.bar(X, Dargpri, color = 'black', alpha = 1, label= 'power demand')
ax10.tick_params(labelsize=14)
ax10.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax10.set_yticks([-2,2], ['-2','2'])
ax10.set_ylim(-4.5,4.5)
ax10.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])

# ~ ax4.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=14).get_frame().set_edgecolor("white")

########## uruguay
ax2.set_title('Uruguay  ', fontsize=13, weight='bold')
ax2.bar(X, Duruver, color = 'black', alpha = 1)
ax2.tick_params(labelsize=14)
ax2.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax2.set_yticks([-2,2], ['-2','2'])
ax2.set_ylim(-4,4)
ax2.xaxis.set_tick_params(length=0)

ax5.bar(X, Duruoto, color = 'black', alpha = 1)
ax5.tick_params(labelsize=14)
ax5.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax5.set_yticks([-2,2], ['-2','2'])
ax5.set_ylim(-4,4)
ax5.xaxis.set_tick_params(length=0)

ax8.bar(X, Duruinv, color = 'black', alpha = 1)
ax8.tick_params(labelsize=14)
ax8.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax8.set_yticks([-2,2], ['-2','2'])
ax8.set_ylim(-4,4)
ax8.xaxis.set_tick_params(length=0)

ax11.bar(X, Durupri, color = 'black', alpha = 1)
ax11.tick_params(labelsize=14)
ax11.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax11.set_yticks([-2,2], ['-2','2'])
ax11.set_ylim(-4,4)
ax11.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])

########## chile
ax3.set_title('Chile  ', fontsize=13, weight='bold')
ax3.bar(X, Dchiver, color = 'black', alpha = 1)
ax3.tick_params(labelsize=14)
ax3.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax3.set_yticks([-2,2], ['-2','2'])
ax3.set_ylim(-4,4)
ax3.xaxis.set_tick_params(length=0)

ax6.bar(X, Dchioto, color = 'black', alpha = 1)
ax6.tick_params(labelsize=14)
ax6.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax6.set_yticks([-2,2], ['-2','2'])
ax6.set_ylim(-4,4)
ax6.xaxis.set_tick_params(length=0)

ax9.bar(X, Dchiinv, color = 'black', alpha = 1)
ax9.tick_params(labelsize=14)
ax9.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax9.set_yticks([-2,2], ['-2','2'])
ax9.set_ylim(-4,4)
ax9.xaxis.set_tick_params(length=0)

ax12.bar(X, Dchipri, color = 'black', alpha = 1)
ax12.tick_params(labelsize=14)
ax12.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax12.set_yticks([-2,2], ['-2','2'])
ax12.set_ylim(-4,4)
ax12.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])

fig.text(0.91, 0.77, 'DJF', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.57, 'MAM', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.39, 'JJA', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.19, 'SON', fontsize = 14, rotation='vertical')
fig.text(0.05, 0.42, 'variation [%]', fontsize=14, rotation='vertical')
fig.text(0.45, 0.05, 'MJO phase', fontsize=14)
fig.subplots_adjust(wspace=0.2, hspace=0.08)
fig.subplots_adjust(bottom=0.15)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/paisesD.png',bbox_inches="tight", dpi=600)

# ~ fig, (ax1,ax2,ax3,ax4) = plt.subplots(1, 4,figsize=(9,2.5), sharey=True, sharex= True)


