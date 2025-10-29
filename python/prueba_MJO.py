import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

uru = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/series viento-sol/uru-sol-agrup.csv', header=None, delimiter=',', na_values='-99')
arg = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/series viento-sol/arg-sol-agrup.csv', header=None, delimiter=',', na_values='-99')
chi = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/series viento-sol/chi-sol-agrup.csv', header=None, delimiter=',', na_values='-99')

uru_cruda = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/series viento-sol/uru-sol.txt', header=None, delimiter=';', na_values='-99')
arg_cruda = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/series viento-sol/arg-sol.txt', header=None, delimiter=';', na_values='-99')
chi_cruda = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/series viento-sol/chi-sol.txt', header=None, delimiter=';', na_values='-99')

mad = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/mjo/WH.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, RMM1, RMM2, phase, amplitude

series = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series[0] = mad[1]
# cargamos fase
series[1] = mad[6]
# cargamos dia de la semana, para cuando trabajemos con demanda
series[2] = mad[3]
#  cargamos amplitud, para quedarnos con MJO activas
series[3] = mad[7]
# series uruguay argentina chile
series[4] = uru[1]
series[5] = arg[1]
series[6] = chi[1]

# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
print(series[0])
series = series.loc[series[3] > 1]

## calculamos los promedios estacionales de las series crudas. Esto sirve para sacar los porcentajes

uru_c_ver = uru_cruda.loc[(uru_cruda[1] == 1) | (uru_cruda[1] == 2) | (uru_cruda[1] == 12)]
uru_c_oto = uru_cruda.loc[(uru_cruda[1] == 3) | (uru_cruda[1] == 4) | (uru_cruda[1] == 5)]
uru_c_inv = uru_cruda.loc[(uru_cruda[1] == 6) | (uru_cruda[1] == 7) | (uru_cruda[1] == 8)]
uru_c_pri = uru_cruda.loc[(uru_cruda[1] == 9) | (uru_cruda[1] == 10) | (uru_cruda[1] == 11)]

uru_p_v = 100/uru_c_ver[3].mean()
uru_p_o = 100/uru_c_oto[3].mean()
uru_p_i = 100/uru_c_inv[3].mean()
uru_p_p = 100/uru_c_pri[3].mean()

chi_c_ver = chi_cruda.loc[(chi_cruda[1] == 1) | (chi_cruda[1] == 2) | (chi_cruda[1] == 12)]
chi_c_oto = chi_cruda.loc[(chi_cruda[1] == 3) | (chi_cruda[1] == 4) | (chi_cruda[1] == 5)]
chi_c_inv = chi_cruda.loc[(chi_cruda[1] == 6) | (chi_cruda[1] == 7) | (chi_cruda[1] == 8)]
chi_c_pri = chi_cruda.loc[(chi_cruda[1] == 9) | (chi_cruda[1] == 10) | (chi_cruda[1] == 11)]

chi_p_v = 100/chi_c_ver[3].mean()
chi_p_o = 100/chi_c_oto[3].mean()
chi_p_i = 100/chi_c_inv[3].mean()
chi_p_p = 100/chi_c_pri[3].mean()

arg_c_ver = arg_cruda.loc[(arg_cruda[1] == 1) | (arg_cruda[1] == 2) | (arg_cruda[1] == 12)]
arg_c_oto = arg_cruda.loc[(arg_cruda[1] == 3) | (arg_cruda[1] == 4) | (arg_cruda[1] == 5)]
arg_c_inv = arg_cruda.loc[(arg_cruda[1] == 6) | (arg_cruda[1] == 7) | (arg_cruda[1] == 8)]
arg_c_pri = arg_cruda.loc[(arg_cruda[1] == 9) | (arg_cruda[1] == 10) | (arg_cruda[1] == 11)]

arg_p_v = 100/arg_c_ver[3].mean()
arg_p_o = 100/arg_c_oto[3].mean()
arg_p_i = 100/arg_c_inv[3].mean()
arg_p_p = 100/arg_c_pri[3].mean()

# VERANO
verano = series.loc[(series[0] == 1) | (series[0] == 2) | (series[0] == 12)]
f1v = verano.loc[verano[1] == 1]
f2v = verano.loc[verano[1] == 2]
f3v = verano.loc[verano[1] == 3]
f4v = verano.loc[verano[1] == 4]
f5v = verano.loc[verano[1] == 5]
f6v = verano.loc[verano[1] == 6]
f7v = verano.loc[verano[1] == 7]
f8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series.loc[(series[0] == 3) | (series[0] == 4) | (series[0] == 5)]
f1o = otono.loc[otono[1] == 1]
f2o = otono.loc[otono[1] == 2]
f3o = otono.loc[otono[1] == 3]
f4o = otono.loc[otono[1] == 4]
f5o = otono.loc[otono[1] == 5]
f6o = otono.loc[otono[1] == 6]
f7o = otono.loc[otono[1] == 7]
f8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series.loc[(series[0] == 6) | (series[0] == 7) | (series[0] == 8)]
f1i = invierno.loc[invierno[1] == 1]
f2i = invierno.loc[invierno[1] == 2]
f3i = invierno.loc[invierno[1] == 3]
f4i = invierno.loc[invierno[1] == 4]
f5i = invierno.loc[invierno[1] == 5]
f6i = invierno.loc[invierno[1] == 6]
f7i = invierno.loc[invierno[1] == 7]
f8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series.loc[(series[0] == 9) | (series[0] == 10) | (series[0] == 11)]
f1p = primavera.loc[primavera[1] == 1]
f2p = primavera.loc[primavera[1] == 2]
f3p = primavera.loc[primavera[1] == 3]
f4p = primavera.loc[primavera[1] == 4]
f5p = primavera.loc[primavera[1] == 5]
f6p = primavera.loc[primavera[1] == 6]
f7p = primavera.loc[primavera[1] == 7]
f8p = primavera.loc[primavera[1] == 8]

uruver = [f1v[4].mean()*uru_p_v,f2v[4].mean()*uru_p_v,f3v[4].mean()*uru_p_v,f4v[4].mean()*uru_p_v,f5v[4].mean()*uru_p_v,f6v[4].mean()*uru_p_v,f7v[4].mean()*uru_p_v,f8v[4].mean()*uru_p_v ]
argver = [f1v[5].mean()*arg_p_v,f2v[5].mean()*arg_p_v,f3v[5].mean()*arg_p_v,f4v[5].mean()*arg_p_v,f5v[5].mean()*arg_p_v,f6v[5].mean()*arg_p_v,f7v[5].mean()*arg_p_v,f8v[5].mean()*arg_p_v ]
chiver = [f1v[6].mean()*chi_p_v,f2v[6].mean()*chi_p_v,f3v[6].mean()*chi_p_v,f4v[6].mean()*chi_p_v,f5v[6].mean()*chi_p_v,f6v[6].mean()*chi_p_v,f7v[6].mean()*chi_p_v,f8v[6].mean()*chi_p_v ]

uruoto = [f1o[4].mean()*uru_p_o,f2o[4].mean()*uru_p_o,f3o[4].mean()*uru_p_o,f4o[4].mean()*uru_p_o,f5o[4].mean()*uru_p_o,f6o[4].mean()*uru_p_o,f7o[4].mean()*uru_p_o,f8o[4].mean()*uru_p_o ]
argoto = [f1o[5].mean()*arg_p_o,f2o[5].mean()*arg_p_o,f3o[5].mean()*arg_p_o,f4o[5].mean()*arg_p_o,f5o[5].mean()*arg_p_o,f6o[5].mean()*arg_p_o,f7o[5].mean()*arg_p_o,f8o[5].mean()*arg_p_o ]
chioto = [f1o[6].mean()*chi_p_o,f2o[6].mean()*chi_p_o,f3o[6].mean()*chi_p_o,f4o[6].mean()*chi_p_o,f5o[6].mean()*chi_p_o,f6o[6].mean()*chi_p_o,f7o[6].mean()*chi_p_o,f8o[6].mean()*chi_p_o ]

uruinv = [f1i[4].mean()*uru_p_i,f2i[4].mean()*uru_p_i,f3i[4].mean()*uru_p_i,f4i[4].mean()*uru_p_i,f5i[4].mean()*uru_p_i,f6i[4].mean()*uru_p_i,f7i[4].mean()*uru_p_i,f8i[4].mean()*uru_p_i ]
arginv = [f1i[5].mean()*arg_p_i,f2i[5].mean()*arg_p_i,f3i[5].mean()*arg_p_i,f4i[5].mean()*arg_p_i,f5i[5].mean()*arg_p_i,f6i[5].mean()*arg_p_i,f7i[5].mean()*arg_p_i,f8i[5].mean()*arg_p_i ]
chiinv = [f1i[6].mean()*chi_p_i,f2i[6].mean()*chi_p_i,f3i[6].mean()*chi_p_i,f4i[6].mean()*chi_p_i,f5i[6].mean()*chi_p_i,f6i[6].mean()*chi_p_i,f7i[6].mean()*chi_p_i,f8i[6].mean()*chi_p_i ]

urupri = [f1p[4].mean()*uru_p_p,f2p[4].mean()*uru_p_p,f3p[4].mean()*uru_p_p,f4p[4].mean()*uru_p_p,f5p[4].mean()*uru_p_p,f6p[4].mean()*uru_p_p,f7p[4].mean()*uru_p_p,f8p[4].mean()*uru_p_p ]
argpri = [f1p[5].mean()*arg_p_p,f2p[5].mean()*arg_p_p,f3p[5].mean()*arg_p_p,f4p[5].mean()*arg_p_p,f5p[5].mean()*arg_p_p,f6p[5].mean()*arg_p_p,f7p[5].mean()*arg_p_p,f8p[5].mean()*arg_p_p ]
chipri = [f1p[6].mean()*chi_p_p,f2p[6].mean()*chi_p_p,f3p[6].mean()*chi_p_p,f4p[6].mean()*chi_p_p,f5p[6].mean()*chi_p_p,f6p[6].mean()*chi_p_p,f7p[6].mean()*chi_p_p,f8p[6].mean()*chi_p_p ]


X = [1,2,3,4,5,6,7,8]

fig, (ax1,ax2,ax3,ax4) = plt.subplots(1, 4,figsize=(9,2.5), sharey= True, sharex= True)

ax1.plot(X, uruver, linewidth = 2, alpha = 0.8, color = 'tomato')
ax1.plot(X, argver, linewidth = 2, alpha = 0.8, color = 'darkblue')
ax1.plot(X, chiver, linewidth = 2, alpha = 0.8, color = 'orange')
ax1.set_ylabel('irradiance \n [%]', fontsize=14)
ax1.tick_params(labelsize=14)
ax1.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
# ~ ax1.set_yticks([-0.4,-0.2,0,0.2], ['-0.4','-0.2','0','0.2'])
ax1.set_title('DJF', fontsize=13, weight='bold')
ax1.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)

ax2.plot(X, uruoto, linewidth = 2, alpha = 0.8, color = 'tomato')
ax2.plot(X, argoto, linewidth = 2, alpha = 0.8, color = 'darkblue')
ax2.plot(X, chioto, linewidth = 2, alpha = 0.8, color = 'orange')
ax2.tick_params(labelsize=14)
ax2.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax2.set_title('MAM', fontsize=13, weight='bold')
ax2.yaxis.set_tick_params(length=0)
ax2.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)

ax3.plot(X, uruinv, linewidth = 2, alpha = 0.8, color = 'tomato')
ax3.plot(X, arginv, linewidth = 2, alpha = 0.8, color = 'darkblue')
ax3.plot(X, chiinv, linewidth = 2, alpha = 0.8, color = 'orange')
ax3.tick_params(labelsize=14)
ax3.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax3.set_title('JJA', fontsize=13, weight='bold')
ax3.yaxis.set_tick_params(length=0)
ax3.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)

ax4.plot(X, urupri, label = 'Uruguay', linewidth = 2, alpha = 0.8, color = 'tomato')
ax4.plot(X, argpri, label = 'Argentina', linewidth = 2, alpha = 0.8, color = 'darkblue')
ax4.plot(X, chipri, label = 'Chile', linewidth = 2, alpha = 0.8, color = 'orange')
ax4.tick_params(labelsize=14)
ax4.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax4.set_title('SON', fontsize=13, weight='bold')
ax4.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=14).get_frame().set_edgecolor("white")
ax4.yaxis.set_tick_params(length=0)
ax4.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)

fig.text(0.45, -0.1, 'MJO phase', fontsize=14)
fig.subplots_adjust(wspace=0.08)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/sol.png',bbox_inches="tight", dpi=600)
plt.show()

