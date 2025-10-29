import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from scipy.signal import detrend
import math

#################################
#######VIENTO####################
#################################

Vuru = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-vie-agrup.csv', header=None, delimiter=',', na_values='-99')
Varg = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-vie-agrup.csv', header=None, delimiter=',', na_values='-99')
Vchi = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-vie-agrup.csv', header=None, delimiter=',', na_values='-99')

Vuru_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-vie.txt', header=None, delimiter=';', na_values='-99')
Varg_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-vie.txt', header=None, delimiter=';', na_values='-99')
Vchi_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-vie.txt', header=None, delimiter=';', na_values='-99')

Vsam = pd.read_csv('/home/emi/Documents/MJO/datos/AAO/SAM.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, SAM

series = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series[0] = Vsam[1]
# cargamos dia de la semana, para cuando trabajemos con demanda
series[2] = Vsam[3]
#  cargamos amplitud, para quedarnos con MJO activas
series[3] = Vsam[4]
# series uruguay argentina chile
series[4] = Vuru[1]
series[5] = Varg[1]
series[6] = Vchi[1]

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
Vnegv = verano.loc[verano[3] <= -1]
Vneuv = verano.loc[(verano[3] >= -1) & (verano[3] <= 1)]
Vposv = verano.loc[verano[3] >= 1]

# OTOÑO
otono = series.loc[(series[0] == 3) | (series[0] == 4) | (series[0] == 5)]
Vnego = otono.loc[otono[3] <= -1]
Vneuo = otono.loc[(otono[3] >= -1) & (otono[3] <= 1)]
Vposo = otono.loc[otono[3] >= 1]

# INVIERNO
invierno = series.loc[(series[0] == 6) | (series[0] == 7) | (series[0] == 8)]
Vnegi = invierno.loc[invierno[3] <= -1]
Vneui = invierno.loc[(invierno[3] >= -1) & (invierno[3] <= 1)]
Vposi = invierno.loc[invierno[3] >= 1]

# primavera
primavera = series.loc[(series[0] == 9) | (series[0] == 10) | (series[0] == 11)]
Vnegp = primavera.loc[primavera[3] <= -1]
Vneup = primavera.loc[(primavera[3] >= -1) & (primavera[3] <= 1)]
Vposp = primavera.loc[primavera[3] >= 1]

Vuruver = [Vnegv[4].mean()*Vuru_p_v,Vneuv[4].mean()*Vuru_p_v,Vposv[4].mean()*Vuru_p_v]
Vargver = [Vnegv[5].mean()*Varg_p_v,Vneuv[5].mean()*Varg_p_v,Vposv[5].mean()*Varg_p_v]
Vchiver = [Vnegv[6].mean()*Vchi_p_v,Vneuv[6].mean()*Vchi_p_v,Vposv[6].mean()*Vchi_p_v]

Vuruoto = [Vnego[4].mean()*Vuru_p_o,Vneuo[4].mean()*Vuru_p_o,Vposo[4].mean()*Vuru_p_o]
Vargoto = [Vnego[5].mean()*Varg_p_o,Vneuo[5].mean()*Varg_p_o,Vposo[5].mean()*Varg_p_o]
Vchioto = [Vnego[6].mean()*Vchi_p_o,Vneuo[6].mean()*Vchi_p_o,Vposo[6].mean()*Vchi_p_o]

Vuruinv = [Vnegi[4].mean()*Vuru_p_i,Vneui[4].mean()*Vuru_p_i,Vposi[4].mean()*Vuru_p_i]
Varginv = [Vnegi[5].mean()*Varg_p_i,Vneui[5].mean()*Varg_p_i,Vposi[5].mean()*Varg_p_i]
Vchiinv = [Vnegi[6].mean()*Vchi_p_i,Vneui[6].mean()*Vchi_p_i,Vposi[6].mean()*Vchi_p_i]

Vurupri = [Vnegp[4].mean()*Vuru_p_p,Vneup[4].mean()*Vuru_p_p,Vposp[4].mean()*Vuru_p_p]
Vargpri = [Vnegp[5].mean()*Varg_p_p,Vneup[5].mean()*Varg_p_p,Vposp[5].mean()*Varg_p_p]
Vchipri = [Vnegp[6].mean()*Vchi_p_p,Vneup[6].mean()*Vchi_p_p,Vposp[6].mean()*Vchi_p_p]

X = [1,2,3]

fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4, 3,figsize=(6.5,5), sharex= True)

########## argentina

ax1.set_title('Argentina', fontsize=13, weight='bold')
ax1.bar(X, Vargver, color = 'mediumblue', alpha = 1)
ax1.tick_params(labelsize=14)
ax1.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax1.set_yticks([-3,3], ['-3','3'])
ax1.set_ylim(-5.2,5.2)
ax1.xaxis.set_tick_params(length=0)

ax4.bar(X, Vargoto, color = 'mediumblue', alpha = 1)
ax4.tick_params(labelsize=14)
ax4.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax4.set_yticks([-3,3], ['-3','3'])
ax4.set_ylim(-5.2,5.2)
ax4.xaxis.set_tick_params(length=0)

ax7.bar(X, Varginv, color = 'mediumblue', alpha = 1)
ax7.tick_params(labelsize=14)
ax7.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax7.set_yticks([-3,3], ['-3','3'])
ax7.set_ylim(-5.2,5.2)
ax7.xaxis.set_tick_params(length=0)

ax10.bar(X, Vargpri, color = 'mediumblue', alpha = 1, label= 'radiation')
ax10.tick_params(labelsize=14)
ax10.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax10.set_yticks([-3,3], ['-3','3'])
ax10.set_ylim(-5.2,5.2)
ax10.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax10.tick_params(axis='x', labelrotation=90)

# ~ ax4.legend(bbox_to_anchor=(2.2, 1), borderaxespad=0., fontsize=14).get_frame().set_edgecolor("white")

########## uruguay

ax2.set_title('Uruguay  ', fontsize=13, weight='bold')
ax2.bar(X, Vuruver, color = 'mediumblue', alpha = 1)
ax2.tick_params(labelsize=14)
ax2.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax2.set_yticks([-3,3], ['-3','3'])
ax2.set_ylim(-5,5)
ax2.xaxis.set_tick_params(length=0)

ax5.bar(X, Vuruoto, color = 'mediumblue', alpha = 1)
ax5.set_yticks([-3,3], ['-3','3'])
ax5.set_ylim(-5,5)
ax5.tick_params(labelsize=14)
ax5.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax5.xaxis.set_tick_params(length=0)

ax8.bar(X, Vuruinv, color = 'mediumblue', alpha = 1)
ax8.set_yticks([-3,3], ['-3','3'])
ax8.set_ylim(-5,5)
ax8.tick_params(labelsize=14)
ax8.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax8.xaxis.set_tick_params(length=0)

ax11.bar(X, Vurupri, color = 'mediumblue', alpha = 1)
ax11.set_yticks([-3,3], ['-3','3'])
ax11.set_ylim(-5,5)
ax11.tick_params(labelsize=14)
ax11.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax11.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax11.tick_params(axis='x', labelrotation=90)

########## chile

ax3.set_title('Chile  ', fontsize=13, weight='bold')
ax3.bar(X, Vchiver, color = 'mediumblue', alpha = 1)
ax3.tick_params(labelsize=14)
ax3.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax3.set_yticks([-2,2], ['-2','2'])
ax3.set_ylim(-3.8,3.8)
ax3.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax3.xaxis.set_tick_params(length=0)

ax6.bar(X, Vchioto, color = 'mediumblue', alpha = 1)
ax6.tick_params(labelsize=14)
ax6.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax6.set_yticks([-2,2], ['-2','2'])
ax6.set_ylim(-3.8,3.8)
ax6.xaxis.set_tick_params(length=0)
ax6.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])

ax9.bar(X, Vchiinv, color = 'mediumblue', alpha = 1)
ax9.tick_params(labelsize=14)
ax9.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax9.set_yticks([-2,2], ['-2','2'])
ax9.set_ylim(-3.8,3.8)
ax9.xaxis.set_tick_params(length=0)
ax9.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])

ax12.bar(X, Vchipri, color = 'mediumblue', alpha = 1)
ax12.tick_params(labelsize=14)
ax12.axhline(y=0, color="mediumblue", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax12.set_yticks([-2,2], ['-2','2'])
ax12.set_ylim(-3.8,3.8)
ax12.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax12.tick_params(axis='x', labelrotation=90)

fig.text(0.91, 0.77, 'DJF', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.59, 'MAM', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.44, 'JJA', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.25, 'SON', fontsize = 14, rotation='vertical')
fig.text(0.05, 0.42, 'variation [%]', fontsize=14, rotation='vertical')
fig.text(0.45, 0.02, 'SAM index', fontsize=14)
fig.subplots_adjust(wspace=0.25, hspace=0.08)
fig.subplots_adjust(bottom=0.2)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/paisesAAO_V.png',bbox_inches="tight", dpi=600)
'''
fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8),(ax9,ax10,ax11,ax12)) = plt.subplots(3, 4,figsize=(7,4), sharex= True, sharey='row')

########## argentina

ax1.set_title('DJF', fontsize=13, weight='bold')
ax1.bar(X, Vargver, color = 'mediumblue', alpha = 1)
ax1.tick_params(labelsize=14)
ax1.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax1.set_yticks([-3,3], ['-3','3'])
ax1.set_ylim(-5.2,5.2)
ax1.xaxis.set_tick_params(length=0)
# ~ ax1.grid(alpha=0.5, linestyle='--')

ax2.set_title('MAM', fontsize=13, weight='bold')
ax2.bar(X, Vargoto, color = 'mediumblue', alpha = 1)
ax2.tick_params(labelsize=14)
ax2.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax2.set_ylim(-5.2,5.2)
ax2.xaxis.set_tick_params(length=0)
ax2.yaxis.set_tick_params(length=0)
# ~ ax2.grid(alpha=0.5, linestyle='--')

ax3.set_title('JJA', fontsize=13, weight='bold')
ax3.bar(X, Varginv, color = 'mediumblue', alpha = 1)
ax3.tick_params(labelsize=14)
ax3.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax3.set_ylim(-5.2,5.2)
ax3.xaxis.set_tick_params(length=0)
ax3.yaxis.set_tick_params(length=0)
# ~ ax3.grid(alpha=0.5, linestyle='--')

ax4.set_title('SON', fontsize=13, weight='bold')
ax4.bar(X, Vargpri, color = 'mediumblue', alpha = 1, label= 'wind speed')
ax4.tick_params(labelsize=14)
ax4.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax4.set_ylim(-5.2,5.2)
ax4.xaxis.set_tick_params(length=0)
ax4.yaxis.set_tick_params(length=0)
# ~ ax4.grid(alpha=0.5, linestyle='--')

# ~ ax4.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=14).get_frame().set_edgecolor("white")

########## uruguay

ax5.bar(X, Vuruver, color = 'mediumblue', alpha = 1)
ax5.tick_params(labelsize=14)
ax5.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax5.set_yticks([-3,3], ['-3','3'])
ax5.set_ylim(-5,5)
ax5.xaxis.set_tick_params(length=0)
ax5.set_ylabel('variation [%]', fontsize=15)
# ~ ax5.grid(alpha=0.5, linestyle='--')

ax6.bar(X, Vuruoto, color = 'mediumblue', alpha = 1)
ax6.tick_params(labelsize=14)
ax6.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax6.set_ylim(-5,5)
ax6.xaxis.set_tick_params(length=0)
ax6.yaxis.set_tick_params(length=0)
# ~ ax6.grid(alpha=0.5, linestyle='--')

ax7.bar(X, Vuruinv, color = 'mediumblue', alpha = 1)
ax7.tick_params(labelsize=14)
ax7.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax7.set_ylim(-5,5)
ax7.xaxis.set_tick_params(length=0)
ax7.yaxis.set_tick_params(length=0)
# ~ ax7.grid(alpha=0.5, linestyle='--')

ax8.bar(X, Vurupri, color = 'mediumblue', alpha = 1)
ax8.tick_params(labelsize=14)
ax8.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax8.set_ylim(-5,5)
ax8.xaxis.set_tick_params(length=0)
ax8.yaxis.set_tick_params(length=0)
# ~ ax8.grid(alpha=0.5, linestyle='--')

########## chile

ax9.bar(X, Vchiver, color = 'mediumblue', alpha = 1)
ax9.tick_params(labelsize=14)
ax9.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax9.set_yticks([-2,2], ['-2','2'])
ax9.set_ylim(-3.8,3.8)
ax9.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax9.tick_params(axis='x', labelrotation=90)

ax10.bar(X, Vchioto, color = 'mediumblue', alpha = 1)
ax10.tick_params(labelsize=14)
ax10.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax10.set_yticks([-2,2], ['-2','2'])
ax10.set_ylim(-3.8,3.8)
ax10.yaxis.set_tick_params(length=0)
ax10.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax10.tick_params(axis='x', labelrotation=90)

ax11.bar(X, Vchiinv, color = 'mediumblue', alpha = 1)
ax11.tick_params(labelsize=14)
ax11.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax11.set_yticks([-2,2], ['-2','2'])
ax11.set_ylim(-3.8,3.8)
ax11.yaxis.set_tick_params(length=0)
ax11.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax11.tick_params(axis='x', labelrotation=90)

ax12.bar(X, Vchipri, color = 'mediumblue', alpha = 1)
ax12.tick_params(labelsize=14)
ax12.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax12.set_yticks([-2,2], ['-2','2'])
ax12.set_ylim(-3.8,3.8)
ax12.yaxis.set_tick_params(length=0)
ax12.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax12.tick_params(axis='x', labelrotation=90)

fig.text(0.91, 0.72, 'Arg.', fontsize = 14, rotation='vertical' , weight='bold')
fig.text(0.91, 0.47, 'Urug.', fontsize = 14, rotation='vertical', weight='bold')
fig.text(0.91, 0.26, 'Chi.', fontsize = 14, rotation='vertical', weight='bold')
fig.text(0.45, 0.002, 'SAM index', fontsize=14)
fig.subplots_adjust(wspace=0.04, hspace=0.08)
fig.subplots_adjust(bottom=0.2)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/paisesAAO_V.png',bbox_inches="tight", dpi=600)
# ~ plt.show()
'''
#################################
#######SOL####################
#################################

Suru = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-sol-agrup.csv', header=None, delimiter=',', na_values='-99')
Sarg = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-sol-agrup.csv', header=None, delimiter=',', na_values='-99')
Schi = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-sol-agrup.csv', header=None, delimiter=',', na_values='-99')

Suru_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-sol.txt', header=None, delimiter=';', na_values='-99')
Sarg_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-sol.txt', header=None, delimiter=';', na_values='-99')
Schi_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-sol.txt', header=None, delimiter=';', na_values='-99')

Ssam = pd.read_csv('/home/emi/Documents/MJO/datos/AAO/SAM.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, SAM

series = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series[0] = Ssam[1]
# cargamos dia de la semana, para cuando trabajemos con demanda
series[2] = Ssam[3]
#  cargamos amplitud, para quedarnos con MJO activas
series[3] = Ssam[4]
# series uruguay argentina chile
series[4] = Suru[1]
series[5] = Sarg[1]
series[6] = Schi[1]

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
Snegv = verano.loc[verano[3] <= -1]
Sneuv = verano.loc[(verano[3] >= -1) & (verano[3] <= 1)]
Sposv = verano.loc[verano[3] >= 1]

# OTOÑO
otono = series.loc[(series[0] == 3) | (series[0] == 4) | (series[0] == 5)]
Snego = otono.loc[otono[3] <= -1]
Sneuo = otono.loc[(otono[3] >= -1) & (otono[3] <= 1)]
Sposo = otono.loc[otono[3] >= 1]

# INVIERNO
invierno = series.loc[(series[0] == 6) | (series[0] == 7) | (series[0] == 8)]
Snegi = invierno.loc[invierno[3] <= -1]
Sneui = invierno.loc[(invierno[3] >= -1) & (invierno[3] <= 1)]
Sposi = invierno.loc[invierno[3] >= 1]

# primavera
primavera = series.loc[(series[0] == 9) | (series[0] == 10) | (series[0] == 11)]
Snegp = primavera.loc[primavera[3] <= -1]
Sneup = primavera.loc[(primavera[3] >= -1) & (primavera[3] <= 1)]
Sposp = primavera.loc[primavera[3] >= 1]

Suruver = [Snegv[4].mean()*Suru_p_v,Sneuv[4].mean()*Suru_p_v,Sposv[4].mean()*Suru_p_v]
Sargver = [Snegv[5].mean()*Sarg_p_v,Sneuv[5].mean()*Sarg_p_v,Sposv[5].mean()*Sarg_p_v]
Schiver = [Snegv[6].mean()*Schi_p_v,Sneuv[6].mean()*Schi_p_v,Sposv[6].mean()*Schi_p_v]

Suruoto = [Snego[4].mean()*Suru_p_o,Sneuo[4].mean()*Suru_p_o,Sposo[4].mean()*Suru_p_o]
Sargoto = [Snego[5].mean()*Sarg_p_o,Sneuo[5].mean()*Sarg_p_o,Sposo[5].mean()*Sarg_p_o]
Schioto = [Snego[6].mean()*Schi_p_o,Sneuo[6].mean()*Schi_p_o,Sposo[6].mean()*Schi_p_o]

Suruinv = [Snegi[4].mean()*Suru_p_i,Sneui[4].mean()*Suru_p_i,Sposi[4].mean()*Suru_p_i]
Sarginv = [Snegi[5].mean()*Sarg_p_i,Sneui[5].mean()*Sarg_p_i,Sposi[5].mean()*Sarg_p_i]
Schiinv = [Snegi[6].mean()*Schi_p_i,Sneui[6].mean()*Schi_p_i,Sposi[6].mean()*Schi_p_i]

Surupri = [Snegp[4].mean()*Suru_p_p,Sneup[4].mean()*Suru_p_p,Sposp[4].mean()*Suru_p_p]
Sargpri = [Snegp[5].mean()*Sarg_p_p,Sneup[5].mean()*Sarg_p_p,Sposp[5].mean()*Sarg_p_p]
Schipri = [Snegp[6].mean()*Schi_p_p,Sneup[6].mean()*Schi_p_p,Sposp[6].mean()*Schi_p_p]

fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4, 3,figsize=(6.5,5), sharex= True)

########## argentina

ax1.set_title('Argentina', fontsize=13, weight='bold')
ax1.bar(X, Sargver, color = 'orangered', alpha = 1)
ax1.tick_params(labelsize=14)
ax1.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax1.set_yticks([-2,2], ['-2','2'])
ax1.set_ylim(-3.8,3.8)
ax1.xaxis.set_tick_params(length=0)

ax4.bar(X, Sargoto, color = 'orangered', alpha = 1)
ax4.tick_params(labelsize=14)
ax4.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax4.set_yticks([-2,2], ['-2','2'])
ax4.set_ylim(-3.8,3.8)
ax4.xaxis.set_tick_params(length=0)

ax7.bar(X, Sarginv, color = 'orangered', alpha = 1)
ax7.tick_params(labelsize=14)
ax7.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax7.set_yticks([-2,2], ['-2','2'])
ax7.set_ylim(-3.8,3.8)
ax7.xaxis.set_tick_params(length=0)

ax10.bar(X, Sargpri, color = 'orangered', alpha = 1, label= 'radiation')
ax10.tick_params(labelsize=14)
ax10.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax10.set_yticks([-2,2], ['-2','2'])
ax10.set_ylim(-3.8,3.8)
ax10.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax10.tick_params(axis='x', labelrotation=90)

# ~ ax4.legend(bbox_to_anchor=(2.2, 1), borderaxespad=0., fontsize=14).get_frame().set_edgecolor("white")

########## uruguay

ax2.set_title('Uruguay  ', fontsize=13, weight='bold')
ax2.bar(X, Suruver, color = 'orangered', alpha = 1)
ax2.tick_params(labelsize=14)
ax2.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax2.set_yticks([-2,2], ['-2','2'])
ax2.set_ylim(-3.8,3.8)
ax2.xaxis.set_tick_params(length=0)

ax5.bar(X, Suruoto, color = 'orangered', alpha = 1)
ax5.set_yticks([-2,2], ['-2','2'])
ax5.set_ylim(-3.8,3.8)
ax5.tick_params(labelsize=14)
ax5.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax5.xaxis.set_tick_params(length=0)

ax8.bar(X, Suruinv, color = 'orangered', alpha = 1)
ax8.set_yticks([-2,2], ['-2','2'])
ax8.set_ylim(-3.8,3.8)
ax8.tick_params(labelsize=14)
ax8.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax8.xaxis.set_tick_params(length=0)

ax11.bar(X, Surupri, color = 'orangered', alpha = 1)
ax11.set_yticks([-2,2], ['-2','2'])
ax11.set_ylim(-3.8,3.8)
ax11.tick_params(labelsize=14)
ax11.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax11.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax11.tick_params(axis='x', labelrotation=90)

########## chile

ax3.set_title('Chile  ', fontsize=13, weight='bold')
ax3.bar(X, Schiver, color = 'orangered', alpha = 1)
ax3.tick_params(labelsize=14)
ax3.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax3.set_yticks([-2,2], ['-2','2'])
ax3.set_ylim(-3.8,3.8)
ax3.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax3.xaxis.set_tick_params(length=0)

ax6.bar(X, Schioto, color = 'orangered', alpha = 1)
ax6.tick_params(labelsize=14)
ax6.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax6.set_yticks([-2,2], ['-2','2'])
ax6.set_ylim(-3.8,3.8)
ax6.xaxis.set_tick_params(length=0)
ax6.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])

ax9.bar(X, Schiinv, color = 'orangered', alpha = 1)
ax9.tick_params(labelsize=14)
ax9.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax9.set_yticks([-2,2], ['-2','2'])
ax9.set_ylim(-3.8,3.8)
ax9.xaxis.set_tick_params(length=0)
ax9.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])

ax12.bar(X, Schipri, color = 'orangered', alpha = 1)
ax12.tick_params(labelsize=14)
ax12.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax12.set_yticks([-2,2], ['-2','2'])
ax12.set_ylim(-3.8,3.8)
ax12.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax12.tick_params(axis='x', labelrotation=90)

fig.text(0.91, 0.77, 'DJF', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.59, 'MAM', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.44, 'JJA', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.25, 'SON', fontsize = 14, rotation='vertical')
fig.text(0.05, 0.42, 'variation [%]', fontsize=14, rotation='vertical')
fig.text(0.45, 0.02, 'SAM index', fontsize=14)
fig.subplots_adjust(wspace=0.25, hspace=0.08)
fig.subplots_adjust(bottom=0.2)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/paisesAAO_S.png',bbox_inches="tight", dpi=600)

#################################
#######DEMANDA####################
#################################

Duru = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/uru-dem-agrup.txt', header=None, delimiter=',', na_values='-9999')
Darg = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/arg-dem-agrup.txt', header=None, delimiter=',', na_values='-9999')
Dchi = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/chi-dem-agrup2.txt', header=None, delimiter=',', na_values='-9999')


Duru_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/uru-dem.txt', header=None, delimiter=';')
Darg_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/arg-dem.txt', header=None, delimiter=';')
Dchi_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda/chi-dem2.txt', header=None, delimiter=';')

sam1 = pd.read_csv('/home/emi/Documents/MJO/datos/AAO/SAM2011.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, SAM
sam2 = pd.read_csv('/home/emi/Documents/MJO/datos/AAO/SAM2014.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, SAM
sam3 = pd.read_csv('/home/emi/Documents/MJO/datos/AAO/SAM2007.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, SAM


## aca hay que armar dataDframes diDferentes por que las series de demanda tienen longitudes diDferentes
#### DuruGUAY
series1 = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series1[0] = sam1[1]
# cargamos dia de la semana, para cuando trabajemos con demanda
series1[1] = sam1[3]
#  cargamos indice
series1[2] = sam1[4]
# series uruguay argentina chile
series1[3] = Duru[1]

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
print(Dchi_p_v)
print(Darg_p_v)
print(Darg_p_o)
print(Darg_p_i)
print(Darg_p_p)

# sacamos los Dfines de semana
# ~ series1 = series1.loc[(series1[1] == 1) | (series1[1] == 2) | (series1[1] == 3) | (series1[1] == 4) | (series1[1] == 5)]

# VERANO
verano_U = series1.loc[(series1[0] == 1) | (series1[0] == 2) | (series1[0] == 12)]

DnegUv = verano_U.loc[verano_U[2] <= -1]
DneuUv = verano_U.loc[(verano_U[2] >= -1) & (verano_U[2] <= 1)]
DposUv = verano_U.loc[verano_U[2] >= 1]

# OTOÑO
otono_U = series1.loc[(series1[0] == 3) | (series1[0] == 4) | (series1[0] == 5)]
DnegUo = otono_U.loc[otono_U[2] <= -1]
DneuUo = otono_U.loc[(otono_U[2] >= -1) & (otono_U[2] <= 1)]
DposUo = otono_U.loc[otono_U[2] >= 1]

# INVIERNO
invierno_U = series1.loc[(series1[0] == 6) | (series1[0] == 7) | (series1[0] == 8)]
DnegUi = invierno_U.loc[invierno_U[2] <= -1]
DneuUi = invierno_U.loc[(invierno_U[2] >= -1) & (invierno_U[2] <= 1)]
DposUi = invierno_U.loc[invierno_U[2] >= 1]

# primavera
primavera_U = series1.loc[(series1[0] == 9) | (series1[0] == 10) | (series1[0] == 11)]
DnegUp = primavera_U.loc[primavera_U[2] <= -1]
DneuUp = primavera_U.loc[(primavera_U[2] >= -1) & (primavera_U[2] <= 1)]
DposUp = primavera_U.loc[primavera_U[2] >= 1]

Duruver = [DnegUv[3].mean()*Duru_p_v,DneuUv[3].mean()*Duru_p_v,DposUv[3].mean()*Duru_p_v]
Duruoto = [DnegUo[3].mean()*Duru_p_o,DneuUo[3].mean()*Duru_p_o,DposUo[3].mean()*Duru_p_o]
Duruinv = [DnegUi[3].mean()*Duru_p_i,DneuUi[3].mean()*Duru_p_i,DposUi[3].mean()*Duru_p_i]
Durupri = [DnegUp[3].mean()*Duru_p_p,DneuUp[3].mean()*Duru_p_p,DposUp[3].mean()*Duru_p_p]

#### DchiLE

series2 = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series2[0] = sam2[1]
# cargamos dia de la semana, para cuando trabajemos con demanda
series2[1] = sam2[3]
#  cargamos amplitud, para quedarnos con MJO activas
series2[2] = sam2[4]
# series uruguay argentina chile
series2[3] = Dchi[1]

# sacamos los Dfines de semana
# ~ series2 = series2.loc[(series2[1] == 1) | (series2[1] == 2) | (series2[1] == 3) | (series2[1] == 4) | (series2[1] == 5)]

# VERANO
verano_C = series2.loc[(series2[0] == 1) | (series2[0] == 2) | (series2[0] == 12)]
DnegCv = verano_C.loc[verano_C[2] <= -1]
DneuCv = verano_C.loc[(verano_C[2] >= -1) & (verano_C[2] <= 1)]
DposCv = verano_C.loc[verano_C[2] >= 1]

# OTOÑO
otono_C = series2.loc[(series2[0] == 3) | (series2[0] == 4) | (series2[0] == 5)]
DnegCo = otono_C.loc[otono_C[2] <= -1]
DneuCo = otono_C.loc[(otono_C[2] >= -1) & (otono_C[2] <= 1)]
DposCo = otono_C.loc[otono_C[2] >= 1]

# INVIERNO
invierno_C = series2.loc[(series2[0] == 6) | (series2[0] == 7) | (series2[0] == 8)]
DnegCi = invierno_C.loc[invierno_C[2] <= -1]
DneuCi = invierno_C.loc[(invierno_C[2] >= -1) & (invierno_C[2] <= 1)]
DposCi = invierno_C.loc[invierno_C[2] >= 1]

# primavera
primavera_C = series2.loc[(series2[0] == 9) | (series2[0] == 10) | (series2[0] == 11)]
DnegCp = primavera_C.loc[primavera_C[2] <= -1]
DneuCp = primavera_C.loc[(primavera_C[2] >= -1) & (primavera_C[2] <= 1)]
DposCp = primavera_C.loc[primavera_C[2] >= 1]

Dchiver = [DnegCv[3].mean()*Dchi_p_v,DneuCv[3].mean()*Dchi_p_v,DposCv[3].mean()*Dchi_p_v]
Dchioto = [DnegCo[3].mean()*Dchi_p_o,DneuCo[3].mean()*Dchi_p_o,DposCo[3].mean()*Dchi_p_o]
Dchiinv = [DnegCi[3].mean()*Dchi_p_i,DneuCi[3].mean()*Dchi_p_i,DposCi[3].mean()*Dchi_p_i]
Dchipri = [DnegCp[3].mean()*Dchi_p_p,DneuCp[3].mean()*Dchi_p_p,DposCp[3].mean()*Dchi_p_p]

#### DargENTINA
series3 = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series3[0] = sam3[1]
# cargamos dia de la semana, para cuando trabajemos con demanda
series3[1] = sam3[3]
#  cargamos amplitud, para quedarnos con MJO activas
series3[2] = sam3[4]
# series uruguay argentina chile
series3[3] = Darg[1]*1000

# sacamos los Dfines de semana
# ~ series3 = series3.loc[(series3[1] == 1) | (series3[1] == 2) | (series3[1] == 3) | (series3[1] == 1) | (series3[1] == 5)]

# VERANO
verano_A = series3.loc[(series3[0] == 1) | (series3[0] == 2) | (series3[0] == 12)]
DnegAv = verano_A.loc[verano_A[2] <= -1]
DneuAv = verano_A.loc[(verano_A[2] >= -1) & (verano_A[2] <= 1)]
DposAv = verano_A.loc[verano_A[2] >= 1]
print(DnegAv)
print(DneuAv)
print(DposAv)
print(DnegAv[3].mean())
print(DneuAv[3].mean())
print(DposAv[3].mean())

# OTOÑO
otono_A = series3.loc[(series3[0] == 3) | (series3[0] == 4) | (series3[0] == 5)]
DnegAo = otono_A.loc[otono_A[2] <= -1]
DneuAo = otono_A.loc[(otono_A[2] >= -1) & (otono_A[2] <= 1)]
DposAo = otono_A.loc[otono_A[2] >= 1]

# INVIERNO
invierno_A = series3.loc[(series3[0] == 6) | (series3[0] == 7) | (series3[0] == 8)]
DnegAi = invierno_A.loc[invierno_A[2] <= -1]
DneuAi = invierno_A.loc[(invierno_A[2] >= -1) & (invierno_A[2] <= 1)]
DposAi = invierno_A.loc[invierno_A[2] >= 1]

# primavera
primavera_A = series3.loc[(series3[0] == 9) | (series3[0] == 10) | (series3[0] == 11)]
DnegAp = primavera_A.loc[primavera_A[2] <= -1]
DneuAp = primavera_A.loc[(primavera_A[2] >= -1) & (primavera_A[2] <= 1)]
DposAp = primavera_A.loc[primavera_A[2] >= 1]

porc = 100/(1000*Darg_cruda[3].mean())

Dargver = [DnegAv[3].mean()*Darg_p_v,DneuAv[3].mean()*Darg_p_v,DposAv[3].mean()*Darg_p_v]
Dargoto = [DnegAo[3].mean()*Darg_p_o,DneuAo[3].mean()*Darg_p_o,DposAo[3].mean()*Darg_p_o]
Darginv = [DnegAi[3].mean()*Darg_p_i,DneuAi[3].mean()*Darg_p_i,DposAi[3].mean()*Darg_p_i]
Dargpri = [DnegAp[3].mean()*Darg_p_p,DneuAp[3].mean()*Darg_p_p,DposAp[3].mean()*Darg_p_p]

fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4, 3,figsize=(6.5,5), sharex= True)

########## argentina

ax1.set_title('Argentina', fontsize=13, weight='bold')
ax1.bar(X, Dargver, color = 'black', alpha = 1)
ax1.tick_params(labelsize=14)
ax1.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax1.set_yticks([-2,2], ['-2','2'])
ax1.set_ylim(-3,3)
ax1.xaxis.set_tick_params(length=0)

ax4.bar(X, Dargoto, color = 'black', alpha = 1)
ax4.tick_params(labelsize=14)
ax4.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax4.set_yticks([-2,2], ['-2','2'])
ax4.set_ylim(-3,3)
ax4.xaxis.set_tick_params(length=0)

ax7.bar(X, Darginv, color = 'black', alpha = 1)
ax7.tick_params(labelsize=14)
ax7.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax7.set_yticks([-2,2], ['-2','2'])
ax7.set_ylim(-3,3)
ax7.xaxis.set_tick_params(length=0)

ax10.bar(X, Dargpri, color = 'black', alpha = 1, label= 'radiation')
ax10.tick_params(labelsize=14)
ax10.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax10.set_yticks([-2,2], ['-2','2'])
ax10.set_ylim(-3,3)
ax10.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax10.tick_params(axis='x', labelrotation=90)

# ~ ax4.legend(bbox_to_anchor=(2.2, 1), borderaxespad=0., fontsize=14).get_frame().set_edgecolor("white")

########## uruguay

ax2.set_title('Uruguay  ', fontsize=13, weight='bold')
ax2.bar(X, Duruver, color = 'black', alpha = 1)
ax2.tick_params(labelsize=14)
ax2.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax2.set_yticks([-2,2], ['-2','2'])
ax2.set_ylim(-3,3)
ax2.xaxis.set_tick_params(length=0)

ax5.bar(X, Duruoto, color = 'black', alpha = 1)
ax5.set_yticks([-2,2], ['-2','2'])
ax5.set_ylim(-3,3)
ax5.tick_params(labelsize=14)
ax5.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax5.xaxis.set_tick_params(length=0)

ax8.bar(X, Duruinv, color = 'black', alpha = 1)
ax8.set_yticks([-2,2], ['-2','2'])
ax8.set_ylim(-3,3)
ax8.tick_params(labelsize=14)
ax8.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax8.xaxis.set_tick_params(length=0)

ax11.bar(X, Durupri, color = 'black', alpha = 1)
ax11.set_yticks([-2,2], ['-2','2'])
ax11.set_ylim(-3,3)
ax11.tick_params(labelsize=14)
ax11.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax11.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax11.tick_params(axis='x', labelrotation=90)

########## chile

ax3.set_title('Chile  ', fontsize=13, weight='bold')
ax3.bar(X, Dchiver, color = 'black', alpha = 1)
ax3.tick_params(labelsize=14)
ax3.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax3.set_yticks([-1,1], ['-1','1'])
ax3.set_ylim(-1.5,1.5)
ax3.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax3.xaxis.set_tick_params(length=0)

ax6.bar(X, Dchioto, color = 'black', alpha = 1)
ax6.tick_params(labelsize=14)
ax6.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax6.set_yticks([-1,1], ['-1','1'])
ax6.set_ylim(-1.5,1.5)
ax6.xaxis.set_tick_params(length=0)
ax6.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])

ax9.bar(X, Dchiinv, color = 'black', alpha = 1)
ax9.tick_params(labelsize=14)
ax9.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax9.set_yticks([-1,1], ['-1','1'])
ax9.set_ylim(-1.5,1.5)
ax9.xaxis.set_tick_params(length=0)
ax9.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])

ax12.bar(X, Dchipri, color = 'black', alpha = 1)
ax12.tick_params(labelsize=14)
ax12.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 1, zorder = 0)
ax12.set_yticks([-1,1], ['-1','1'])
ax12.set_ylim(-1.5,1.5)
ax12.set_xticks([1,2,3], ['<-1','[-1,1]','>+1'])
ax12.tick_params(axis='x', labelrotation=90)

fig.text(0.91, 0.77, 'DJF', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.59, 'MAM', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.44, 'JJA', fontsize = 14, rotation='vertical')
fig.text(0.91, 0.25, 'SON', fontsize = 14, rotation='vertical')
fig.text(0.05, 0.42, 'variation [%]', fontsize=14, rotation='vertical')
fig.text(0.45, 0.02, 'SAM index', fontsize=14)
fig.subplots_adjust(wspace=0.25, hspace=0.08)
fig.subplots_adjust(bottom=0.2)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/paisesAAO_D.png',bbox_inches="tight", dpi=600)

