import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from scipy.signal import detrend

uru = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/demanda/uru-dem-agrup.csv', header=None, delimiter=',', na_values='-99')
arg = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/demanda/arg-dem-agrup.csv', header=None, delimiter=',', na_values='-99')
chi = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/demanda/chi-dem-agrup2.csv', header=None, delimiter=',', na_values='-99')

uru_cruda = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/demanda/uru-dem.txt', header=None, delimiter=';')
arg_cruda = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/demanda/arg-dem.txt', header=None, delimiter=';')
chi_cruda = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/demanda/chi-dem2.txt', header=None, delimiter=';')

mad = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/mjo/WH2011.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, RMM1, RMM2, phase, amplitude
mad2 = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/mjo/WH2014.txt', header=None, delimiter=',', na_values='-99')
mad3 = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/mjo/WH2007.txt', header=None, delimiter=',', na_values='-99')

## aca hay que armar dataframes diferentes por que las series de demanda tienen longitudes diferentes
#### URUGUAY
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
# ~ series[4] = uru[1]*10
series[4] = uru[1]

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

#argentina multiplico x 1000 x que esta en gigas
arg_p_v = 100/(1000*arg_c_ver[3].mean())
arg_p_o = 100/(1000*arg_c_oto[3].mean())
arg_p_i = 100/(1000*arg_c_inv[3].mean())
arg_p_p = 100/(1000*arg_c_pri[3].mean())

# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series = series.loc[series[3] > 1]
# sacamos los fines de semana
series = series.loc[(series[2] == 1) | (series[2] == 2) | (series[2] == 3) | (series[4] == 1) | (series[2] == 5)]

# VERANO
verano_U = series.loc[(series[0] == 1) | (series[0] == 2) | (series[0] == 12)]
f1Uv = verano_U.loc[verano_U[1] == 1]
f2Uv = verano_U.loc[verano_U[1] == 2]
f3Uv = verano_U.loc[verano_U[1] == 3]
f4Uv = verano_U.loc[verano_U[1] == 4]
f5Uv = verano_U.loc[verano_U[1] == 5]
f6Uv = verano_U.loc[verano_U[1] == 6]
f7Uv = verano_U.loc[verano_U[1] == 7]
f8Uv = verano_U.loc[verano_U[1] == 8]

# OTOÑO
otono_U = series.loc[(series[0] == 3) | (series[0] == 4) | (series[0] == 5)]
f1Uo = otono_U.loc[otono_U[1] == 1]
f2Uo = otono_U.loc[otono_U[1] == 2]
f3Uo = otono_U.loc[otono_U[1] == 3]
f4Uo = otono_U.loc[otono_U[1] == 4]
f5Uo = otono_U.loc[otono_U[1] == 5]
f6Uo = otono_U.loc[otono_U[1] == 6]
f7Uo = otono_U.loc[otono_U[1] == 7]
f8Uo = otono_U.loc[otono_U[1] == 8]

# INVIERNO
invierno_U = series.loc[(series[0] == 6) | (series[0] == 7) | (series[0] == 8)]
f1Ui = invierno_U.loc[invierno_U[1] == 1]
f2Ui = invierno_U.loc[invierno_U[1] == 2]
f3Ui = invierno_U.loc[invierno_U[1] == 3]
f4Ui = invierno_U.loc[invierno_U[1] == 4]
f5Ui = invierno_U.loc[invierno_U[1] == 5]
f6Ui = invierno_U.loc[invierno_U[1] == 6]
f7Ui = invierno_U.loc[invierno_U[1] == 7]
f8Ui = invierno_U.loc[invierno_U[1] == 8]

# primavera
primavera_U = series.loc[(series[0] == 9) | (series[0] == 10) | (series[0] == 11)]
f1Up = primavera_U.loc[primavera_U[1] == 1]
f2Up = primavera_U.loc[primavera_U[1] == 2]
f3Up = primavera_U.loc[primavera_U[1] == 3]
f4Up = primavera_U.loc[primavera_U[1] == 4]
f5Up = primavera_U.loc[primavera_U[1] == 5]
f6Up = primavera_U.loc[primavera_U[1] == 6]
f7Up = primavera_U.loc[primavera_U[1] == 7]
f8Up = primavera_U.loc[primavera_U[1] == 8]

uruver = [f1Uv[4].mean()*uru_p_v,f2Uv[4].mean()*uru_p_v,f3Uv[4].mean()*uru_p_v,f4Uv[4].mean()*uru_p_v,f5Uv[4].mean()*uru_p_v,f6Uv[4].mean()*uru_p_v,f7Uv[4].mean()*uru_p_v,f8Uv[4].mean()*uru_p_v]
uruver10 = [f1Uv[4].quantile(.3)*uru_p_v,f2Uv[4].quantile(.3)*uru_p_v,f3Uv[4].quantile(.3)*uru_p_v,f4Uv[4].quantile(.3)*uru_p_v,f5Uv[4].quantile(.3)*uru_p_v,f6Uv[4].quantile(.3)*uru_p_v,f7Uv[4].quantile(.3)*uru_p_v,f8Uv[4].quantile(.3)*uru_p_v]
uruver90 = [f1Uv[4].quantile(.7)*uru_p_v,f2Uv[4].quantile(.7)*uru_p_v,f3Uv[4].quantile(.7)*uru_p_v,f4Uv[4].quantile(.7)*uru_p_v,f5Uv[4].quantile(.7)*uru_p_v,f6Uv[4].quantile(.7)*uru_p_v,f7Uv[4].quantile(.7)*uru_p_v,f8Uv[4].quantile(.7)*uru_p_v]
uruoto = [f1Uo[4].mean()*uru_p_o,f2Uo[4].mean()*uru_p_o,f3Uo[4].mean()*uru_p_o,f4Uo[4].mean()*uru_p_o,f5Uo[4].mean()*uru_p_o,f6Uo[4].mean()*uru_p_o,f7Uo[4].mean()*uru_p_o,f8Uo[4].mean()*uru_p_o ]
uruinv = [f1Ui[4].mean()*uru_p_i,f2Ui[4].mean()*uru_p_i,f3Ui[4].mean()*uru_p_i,f4Ui[4].mean()*uru_p_i,f5Ui[4].mean()*uru_p_i,f6Ui[4].mean()*uru_p_i,f7Ui[4].mean()*uru_p_i,f8Ui[4].mean()*uru_p_i ]
urupri = [f1Up[4].mean()*uru_p_p,f2Up[4].mean()*uru_p_p,f3Up[4].mean()*uru_p_p,f4Up[4].mean()*uru_p_p,f5Up[4].mean()*uru_p_p,f6Up[4].mean()*uru_p_p,f7Up[4].mean()*uru_p_p,f8Up[4].mean()*uru_p_p ]

#### CHILE
series2 = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series2[0] = mad2[1]
# cargamos fase
series2[1] = mad2[6]
# cargamos dia de la semana, para cuando trabajemos con demanda
series2[2] = mad2[3]
#  cargamos amplitud, para quedarnos con MJO activas
series2[3] = mad2[7]
# series uruguay argentina chile
series2[4] = chi[1]

# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series2 = series2.loc[series2[3] > 1]
# sacamos los fines de semana
series2 = series2.loc[(series2[2] == 1) | (series2[2] == 2) | (series2[2] == 3) | (series2[4] == 1) | (series2[2] == 5)]

# VERANO
verano_C = series2.loc[(series2[0] == 1) | (series2[0] == 2) | (series2[0] == 12)]
f1Cv = verano_C.loc[verano_C[1] == 1]
f2Cv = verano_C.loc[verano_C[1] == 2]
f3Cv = verano_C.loc[verano_C[1] == 3]
f4Cv = verano_C.loc[verano_C[1] == 4]
f5Cv = verano_C.loc[verano_C[1] == 5]
f6Cv = verano_C.loc[verano_C[1] == 6]
f7Cv = verano_C.loc[verano_C[1] == 7]
f8Cv = verano_C.loc[verano_C[1] == 8]

# OTOÑO
otono_C = series2.loc[(series2[0] == 3) | (series2[0] == 4) | (series2[0] == 5)]
f1Co = otono_C.loc[otono_C[1] == 1]
f2Co = otono_C.loc[otono_C[1] == 2]
f3Co = otono_C.loc[otono_C[1] == 3]
f4Co = otono_C.loc[otono_C[1] == 4]
f5Co = otono_C.loc[otono_C[1] == 5]
f6Co = otono_C.loc[otono_C[1] == 6]
f7Co = otono_C.loc[otono_C[1] == 7]
f8Co = otono_C.loc[otono_C[1] == 8]

# INVIERNO
invierno_C = series2.loc[(series2[0] == 6) | (series2[0] == 7) | (series2[0] == 8)]
f1Ci = invierno_C.loc[invierno_C[1] == 1]
f2Ci = invierno_C.loc[invierno_C[1] == 2]
f3Ci = invierno_C.loc[invierno_C[1] == 3]
f4Ci = invierno_C.loc[invierno_C[1] == 4]
f5Ci = invierno_C.loc[invierno_C[1] == 5]
f6Ci = invierno_C.loc[invierno_C[1] == 6]
f7Ci = invierno_C.loc[invierno_C[1] == 7]
f8Ci = invierno_C.loc[invierno_C[1] == 8]

# primavera
primavera_C = series2.loc[(series2[0] == 9) | (series2[0] == 10) | (series2[0] == 11)]
f1Cp = primavera_C.loc[primavera_C[1] == 1]
f2Cp = primavera_C.loc[primavera_C[1] == 2]
f3Cp = primavera_C.loc[primavera_C[1] == 3]
f4Cp = primavera_C.loc[primavera_C[1] == 4]
f5Cp = primavera_C.loc[primavera_C[1] == 5]
f6Cp = primavera_C.loc[primavera_C[1] == 6]
f7Cp = primavera_C.loc[primavera_C[1] == 7]
f8Cp = primavera_C.loc[primavera_C[1] == 8]

chiver = [f1Cv[4].mean()*chi_p_v,f2Cv[4].mean()*chi_p_v,f3Cv[4].mean()*chi_p_v,f4Cv[4].mean()*chi_p_v,f5Cv[4].mean()*chi_p_v,f6Cv[4].mean()*chi_p_v,f7Cv[4].mean()*chi_p_v,f8Cv[4].mean()*chi_p_v]
chiver10 = [f1Cv[4].quantile(.3)*chi_p_v,f2Cv[4].quantile(.3)*chi_p_v,f3Cv[4].quantile(.3)*chi_p_v,f4Cv[4].quantile(.3)*chi_p_v,f5Cv[4].quantile(.3)*chi_p_v,f6Cv[4].quantile(.3)*chi_p_v,f7Cv[4].quantile(.3)*chi_p_v,f8Cv[4].quantile(.3)*chi_p_v]
chiver90 = [f1Cv[4].quantile(.7)*chi_p_v,f2Cv[4].quantile(.7)*chi_p_v,f3Cv[4].quantile(.7)*chi_p_v,f4Cv[4].quantile(.7)*chi_p_v,f5Cv[4].quantile(.7)*chi_p_v,f6Cv[4].quantile(.7)*chi_p_v,f7Cv[4].quantile(.7)*chi_p_v,f8Cv[4].quantile(.7)*chi_p_v]
chioto = [f1Co[4].mean()*chi_p_o,f2Co[4].mean()*chi_p_o,f3Co[4].mean()*chi_p_o,f4Co[4].mean()*chi_p_o,f5Co[4].mean()*chi_p_o,f6Co[4].mean()*chi_p_o,f7Co[4].mean()*chi_p_o,f8Co[4].mean()*chi_p_o ]
chiinv = [f1Ci[4].mean()*chi_p_i,f2Ci[4].mean()*chi_p_i,f3Ci[4].mean()*chi_p_i,f4Ci[4].mean()*chi_p_i,f5Ci[4].mean()*chi_p_i,f6Ci[4].mean()*chi_p_i,f7Ci[4].mean()*chi_p_i,f8Ci[4].mean()*chi_p_i ]
chipri = [f1Cp[4].mean()*chi_p_p,f2Cp[4].mean()*chi_p_p,f3Cp[4].mean()*chi_p_p,f4Cp[4].mean()*chi_p_p,f5Cp[4].mean()*chi_p_p,f6Cp[4].mean()*chi_p_p,f7Cp[4].mean()*chi_p_p,f8Cp[4].mean()*chi_p_p ]

#### ARGENTINA
series3 = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series3[0] = mad3[1]
# cargamos fase
series3[1] = mad3[6]
# cargamos dia de la semana, para cuando trabajemos con demanda
series3[2] = mad3[3]
#  cargamos amplitud, para quedarnos con MJO activas
series3[3] = mad3[7]
# series uruguay argentina chile
series3[4] = arg[1]*1000

# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series3 = series3.loc[series3[3] > 1]
# sacamos los fines de semana
series3 = series3.loc[(series3[2] == 1) | (series3[2] == 2) | (series3[2] == 3) | (series3[4] == 1) | (series3[2] == 5)]

# VERANO
verano_A = series3.loc[(series3[0] == 1) | (series3[0] == 2) | (series3[0] == 12)]
f1Av = verano_A.loc[verano_A[1] == 1]
f2Av = verano_A.loc[verano_A[1] == 2]
f3Av = verano_A.loc[verano_A[1] == 3]
f4Av = verano_A.loc[verano_A[1] == 4]
f5Av = verano_A.loc[verano_A[1] == 5]
f6Av = verano_A.loc[verano_A[1] == 6]
f7Av = verano_A.loc[verano_A[1] == 7]
f8Av = verano_A.loc[verano_A[1] == 8]

# OTOÑO
otono_A = series3.loc[(series3[0] == 3) | (series3[0] == 4) | (series3[0] == 5)]
f1Ao = otono_A.loc[otono_A[1] == 1]
f2Ao = otono_A.loc[otono_A[1] == 2]
f3Ao = otono_A.loc[otono_A[1] == 3]
f4Ao = otono_A.loc[otono_A[1] == 4]
f5Ao = otono_A.loc[otono_A[1] == 5]
f6Ao = otono_A.loc[otono_A[1] == 6]
f7Ao = otono_A.loc[otono_A[1] == 7]
f8Ao = otono_A.loc[otono_A[1] == 8]

# INVIERNO
invierno_A = series3.loc[(series3[0] == 6) | (series3[0] == 7) | (series3[0] == 8)]
f1Ai = invierno_A.loc[invierno_A[1] == 1]
f2Ai = invierno_A.loc[invierno_A[1] == 2]
f3Ai = invierno_A.loc[invierno_A[1] == 3]
f4Ai = invierno_A.loc[invierno_A[1] == 4]
f5Ai = invierno_A.loc[invierno_A[1] == 5]
f6Ai = invierno_A.loc[invierno_A[1] == 6]
f7Ai = invierno_A.loc[invierno_A[1] == 7]
f8Ai = invierno_A.loc[invierno_A[1] == 8]

# primavera
primavera_A = series3.loc[(series3[0] == 9) | (series3[0] == 10) | (series3[0] == 11)]
f1Ap = primavera_A.loc[primavera_A[1] == 1]
f2Ap = primavera_A.loc[primavera_A[1] == 2]
f3Ap = primavera_A.loc[primavera_A[1] == 3]
f4Ap = primavera_A.loc[primavera_A[1] == 4]
f5Ap = primavera_A.loc[primavera_A[1] == 5]
f6Ap = primavera_A.loc[primavera_A[1] == 6]
f7Ap = primavera_A.loc[primavera_A[1] == 7]
f8Ap = primavera_A.loc[primavera_A[1] == 8]

porc = 100/(1000*arg_cruda[3].mean())

argver = [f1Av[4].mean()*arg_p_v,f2Av[4].mean()*arg_p_v,f3Av[4].mean()*arg_p_v,f4Av[4].mean()*arg_p_v,f5Av[4].mean()*arg_p_v,f6Av[4].mean()*arg_p_v,f7Av[4].mean()*arg_p_v,f8Av[4].mean()*arg_p_v]
argver10 = [f1Av[4].quantile(.3)*arg_p_v,f2Av[4].quantile(.3)*arg_p_v,f3Av[4].quantile(.3)*arg_p_v,f4Av[4].quantile(.3)*arg_p_v,f5Av[4].quantile(.3)*arg_p_v,f6Av[4].quantile(.3)*arg_p_v,f7Av[4].quantile(.3)*arg_p_v,f8Av[4].quantile(.3)*arg_p_v]
argver90 = [f1Av[4].quantile(.7)*arg_p_v,f2Av[4].quantile(.7)*arg_p_v,f3Av[4].quantile(.7)*arg_p_v,f4Av[4].quantile(.7)*arg_p_v,f5Av[4].quantile(.7)*arg_p_v,f6Av[4].quantile(.7)*arg_p_v,f7Av[4].quantile(.7)*arg_p_v,f8Av[4].quantile(.7)*arg_p_v]
argoto = [f1Ao[4].mean()*arg_p_o,f2Ao[4].mean()*arg_p_o,f3Ao[4].mean()*arg_p_o,f4Ao[4].mean()*arg_p_o,f5Ao[4].mean()*arg_p_o,f6Ao[4].mean()*arg_p_o,f7Ao[4].mean()*arg_p_o,f8Ao[4].mean()*arg_p_o ]
arginv = [f1Ai[4].mean()*arg_p_i,f2Ai[4].mean()*arg_p_i,f3Ai[4].mean()*arg_p_i,f4Ai[4].mean()*arg_p_i,f5Ai[4].mean()*arg_p_i,f6Ai[4].mean()*arg_p_i,f7Ai[4].mean()*arg_p_i,f8Ai[4].mean()*arg_p_i ]
argpri = [f1Ap[4].mean()*arg_p_p,f2Ap[4].mean()*arg_p_p,f3Ap[4].mean()*arg_p_p,f4Ap[4].mean()*arg_p_p,f5Ap[4].mean()*arg_p_p,f6Ap[4].mean()*arg_p_p,f7Ap[4].mean()*arg_p_p,f8Ap[4].mean()*arg_p_p ]

X = [1,2,3,4,5,6,7,8]

fig, (ax1,ax2,ax3,ax4) = plt.subplots(1, 4,figsize=(9,2.5), sharey=True, sharex= True)

ax1.plot(X, uruver, linewidth = 2, alpha = 0.6, color = 'darkgreen')
# ~ ax1.fill_between(X,uruver10, uruver90, alpha=.2, linewidth=0, color = 'darkgreen')
# ~ ax1.fill_between(X,chiver10, chiver90, alpha=.2, linewidth=0, color = 'tomato')
# ~ ax1.fill_between(X,argver10, argver90, alpha=.2, linewidth=0, color = 'darkblue')
ax1.plot(X, argver, linewidth = 2, alpha = 0.6, color = 'darkblue')
ax1.plot(X, chiver, linewidth = 2, alpha = 0.6, color = 'tomato')
ax1.set_ylabel('power demand [%]', fontsize=14)
ax1.tick_params(labelsize=14)
ax1.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax1.set_yticks([-4,-2,0,2,4], ['-4','-2','0','2', '4'])
ax1.set_title('DJF', fontsize=13, weight='bold')
ax1.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)

ax2.plot(X, uruoto, linewidth = 2, alpha = 0.8, color = 'orange')
ax2.plot(X, argoto, linewidth = 2, alpha = 0.8, color = 'darkblue')
ax2.plot(X, chioto, linewidth = 2, alpha = 0.8, color = 'tomato')
ax2.tick_params(labelsize=14)
ax2.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax2.set_title('MAM', fontsize=13, weight='bold')
ax2.yaxis.set_tick_params(length=0)
ax2.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)

ax3.plot(X, uruinv, linewidth = 2, alpha = 0.8, color = 'orange')
ax3.plot(X, arginv, linewidth = 2, alpha = 0.8, color = 'darkblue')
ax3.plot(X, chiinv, linewidth = 2, alpha = 0.8, color = 'tomato')
ax3.tick_params(labelsize=14)
ax3.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax3.set_title('JJA', fontsize=13, weight='bold')
ax3.yaxis.set_tick_params(length=0)
ax3.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)

ax4.plot(X, urupri, label = 'Uruguay', linewidth = 2, alpha = 0.8, color = 'orange')
ax4.plot(X, argpri, label = 'Argentina', linewidth = 2, alpha = 0.8, color = 'darkblue')
ax4.plot(X, chipri, label = 'Chile', linewidth = 2, alpha = 0.8, color = 'tomato')
ax4.tick_params(labelsize=14)
ax4.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
ax4.set_title('SON', fontsize=13, weight='bold')
ax4.legend(bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=14).get_frame().set_edgecolor("white")
ax4.yaxis.set_tick_params(length=0)
ax4.axhline(y=0, color="black", linestyle="--", linewidth = 1.5, alpha = 0.7, zorder = 0)

fig.text(0.45, -0.1, 'MJO phase', fontsize=14)
fig.subplots_adjust(wspace=0.08)
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/demanda2.png',bbox_inches="tight", dpi=600)
plt.show()


