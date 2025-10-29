import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from scipy.signal import detrend


#################################
#######DEMANDA####################
#################################

# ~ DN_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda-brasil/carga_N.txt', header=None, delimiter=',', na_values='-99')
# ~ DNE_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda-brasil/carga_NE.txt', header=None, delimiter=',', na_values='-99')
# ~ DS_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda-brasil/carga_S.txt', header=None, delimiter=',', na_values='-99')
Duru_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/demanda-brasil/carga_SE2.txt', header=None, delimiter=',', na_values='-99')

# ~ DN = pd.read_csv('/home/emi/Documents/MJO/datos/demanda-brasil/carga_N_agrup.csv', header=None, delimiter=',')
# ~ DNE = pd.read_csv('/home/emi/Documents/MJO/datos/demanda-brasil/carga_NE_agrup.csv', header=None, delimiter=',')
# ~ DS = pd.read_csv('/home/emi/Documents/MJO/datos/demanda-brasil/carga_S_agrup.csv', header=None, delimiter=',')
DSE = pd.read_csv('/home/emi/Documents/MJO/datos/demanda-brasil/carga_SE2_agrup.csv', header=None, delimiter=',')

mad = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH2007.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, RMM1, RMM2, phase, amplitude

## calculamos los promedios estacionales de las series crudas. Esto sirve para sacar los porcentajes
Duru_c_ver = Duru_cruda.loc[(Duru_cruda[1] == 1) | (Duru_cruda[1] == 2) | (Duru_cruda[1] == 12)]
Duru_c_oto = Duru_cruda.loc[(Duru_cruda[1] == 3) | (Duru_cruda[1] == 4) | (Duru_cruda[1] == 5)]
Duru_c_inv = Duru_cruda.loc[(Duru_cruda[1] == 6) | (Duru_cruda[1] == 7) | (Duru_cruda[1] == 8)]
Duru_c_pri = Duru_cruda.loc[(Duru_cruda[1] == 9) | (Duru_cruda[1] == 10) | (Duru_cruda[1] == 11)]

Duru_p_v = 100/Duru_c_ver[3].mean()
Duru_p_o = 100/Duru_c_oto[3].mean()
Duru_p_i = 100/Duru_c_inv[3].mean()
Duru_p_p = 100/Duru_c_pri[3].mean()
# ~ print(DSE_p_v)
# ~ print(DSE_p_o)
# ~ print(DSE_p_i)
# ~ print(DSE_p_p)

#### SE
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
series[4] = DSE[1]
# ~ print(series)
# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series = series.loc[series[3] > 1]
# sacamos los fines de semana
series = series.loc[(series[2] == 1) | (series[2] == 2) | (series[2] == 3) | (series[4] == 1) | (series[2] == 5)]

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


X = [1,2,3,4,5,6,7,8]

fig, (ax1,ax2,ax3,ax4) = plt.subplots(1, 4,figsize=(9,2.5), sharex= True)

ax1.bar(X, Duruver, color = 'black', zorder=99, alpha = 0.7)
ax1.tick_params(labelsize=14)
ax1.set_title('DJF', fontsize=13, weight='bold')
ax1.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)
ax1.set_yticks([-2,2], ['-2','2'])
# ~ ax1.set_ylim(-3.8,3.8)
ax1.xaxis.set_tick_params(length=0)

ax2.bar(X, Duruoto, color = 'black', zorder=99, alpha = 0.7)
ax2.tick_params(labelsize=14)
ax2.set_title('DJF', fontsize=13, weight='bold')
ax2.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)
ax2.set_yticks([-2,2], ['-2','2'])
# ~ ax2.set_ylim(-3.8,3.8)
ax2.xaxis.set_tick_params(length=0)

ax3.bar(X, Duruinv, color = 'black', zorder=99, alpha = 0.7)
ax3.tick_params(labelsize=14)
ax3.set_title('DJF', fontsize=13, weight='bold')
ax3.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)
ax3.set_yticks([-2,2], ['-2','2'])
# ~ ax3.set_ylim(-3.8,3.8)
ax3.xaxis.set_tick_params(length=0)

ax4.bar(X, Durupri, color = 'black', zorder=99, alpha = 0.7)
ax4.tick_params(labelsize=14)
ax4.set_title('DJF', fontsize=13, weight='bold')
ax4.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)
ax4.set_yticks([-2,2], ['-2','2'])
# ~ ax4.set_ylim(-3.8,3.8)
ax4.xaxis.set_tick_params(length=0)

plt.show()
