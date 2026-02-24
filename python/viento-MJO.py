import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from scipy.signal import detrend
import seaborn as sns
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, Normalize

#################################
#######VIENTO####################
#################################

Vuru = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-vie-agrup.csv', header=None, delimiter=',', na_values='-99')
Varg = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-vie-agrup.csv', header=None, delimiter=',', na_values='-99')
Vchi = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-vie-agrup.csv', header=None, delimiter=',', na_values='-99')

Vuru_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-vie.txt', header=None, delimiter=';', na_values='-99')
Varg_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-vie.txt', header=None, delimiter=';', na_values='-99')
Vchi_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-vie.txt', header=None, delimiter=';', na_values='-99')

# ~ Vmad = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, RMM1, RMM2, phase, amplitude
Vmad = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/filtered.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, RMM1, RMM2, phase, amplitude

# lag 0
series0 = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series0[0] = Vmad[1]
# cargamos fase
series0[1] = Vmad[6]
# cargamos dia de la semana, para cuando trabajemos con demanda
series0[2] = Vmad[3]
#  cargamos amplitud, para quedarnos con MJO activas
series0[3] = Vmad[7]
# series uruguay argentina chile
series0[4] = Vuru[1]
series0[5] = Varg[1]
series0[6] = Vchi[1]
print(series0)

# lag 1
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[1:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-1].reset_index(drop=True)   # rows 0..n-2
series1 = pd.concat([part1, part2], axis=1)

# lag 2
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[2:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-2].reset_index(drop=True)   # rows 0..n-2
series2 = pd.concat([part1, part2], axis=1)


# lag 3
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[3:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-3].reset_index(drop=True)   # rows 0..n-2
series3 = pd.concat([part1, part2], axis=1)


# lag 4
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[4:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-4].reset_index(drop=True)   # rows 0..n-2
series4 = pd.concat([part1, part2], axis=1)

# lag 5
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[5:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-5].reset_index(drop=True)   # rows 0..n-2
series5 = pd.concat([part1, part2], axis=1)

# lag 6
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[6:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-6].reset_index(drop=True)   # rows 0..n-2
series6 = pd.concat([part1, part2], axis=1)

# lag 7
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[7:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-7].reset_index(drop=True)   # rows 0..n-2
series7 = pd.concat([part1, part2], axis=1)

# lag 8
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[8:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-8].reset_index(drop=True)   # rows 0..n-2
series8 = pd.concat([part1, part2], axis=1)

# lag 9
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[9:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-9].reset_index(drop=True)   # rows 0..n-2
series9 = pd.concat([part1, part2], axis=1)

# lag 10
remove_last_cols  = [0,1,2,3] 
remove_first_cols  = [4,5,6] 
part2 = series0[remove_first_cols].iloc[10:].reset_index(drop=True)   # rows 1..n-1
part1 = series0[remove_last_cols].iloc[:-10].reset_index(drop=True)   # rows 0..n-2
series10 = pd.concat([part1, part2], axis=1)

# nos quedamos con MJO activos, esto es cuando la amplitud es >= 1
series0 = series0.loc[series0[3] > 1]
series1 = series1.loc[series1[3] > 1]
series2 = series2.loc[series2[3] > 1]
series3 = series3.loc[series3[3] > 1]
series4 = series4.loc[series4[3] > 1]
series5 = series5.loc[series5[3] > 1]
series6 = series6.loc[series6[3] > 1]
series7 = series7.loc[series7[3] > 1]
series8 = series8.loc[series8[3] > 1]
series9 = series9.loc[series9[3] > 1]
series10 = series10.loc[series10[3] > 1]

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

####lag0

# VERANO
verano = series0.loc[(series0[0] == 1) | (series0[0] == 2) | (series0[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series0.loc[(series0[0] == 3) | (series0[0] == 4) | (series0[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series0.loc[(series0[0] == 6) | (series0[0] == 7) | (series0[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series0.loc[(series0[0] == 9) | (series0[0] == 10) | (series0[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver0 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver0 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver0 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto0 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto0 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto0 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv0 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv0 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv0 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri0 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri0 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri0 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag1

# VERANO
verano = series1.loc[(series1[0] == 1) | (series1[0] == 2) | (series1[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series1.loc[(series1[0] == 3) | (series1[0] == 4) | (series1[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series1.loc[(series1[0] == 6) | (series1[0] == 7) | (series1[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series1.loc[(series1[0] == 9) | (series1[0] == 10) | (series1[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver1 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver1 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver1 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto1 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto1 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto1 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv1 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv1 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv1 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri1 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri1 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri1 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag2

# VERANO
verano = series2.loc[(series2[0] == 1) | (series2[0] == 2) | (series2[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series2.loc[(series2[0] == 3) | (series2[0] == 4) | (series2[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series2.loc[(series2[0] == 6) | (series2[0] == 7) | (series2[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series2.loc[(series2[0] == 9) | (series2[0] == 10) | (series2[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver2 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver2 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver2 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto2 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto2 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto2 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv2 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv2 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv2 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri2 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri2 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri2 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag3

# VERANO
verano = series3.loc[(series3[0] == 1) | (series3[0] == 2) | (series3[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series3.loc[(series3[0] == 3) | (series3[0] == 4) | (series3[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series3.loc[(series3[0] == 6) | (series3[0] == 7) | (series3[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series3.loc[(series3[0] == 9) | (series3[0] == 10) | (series3[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver3 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver3 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver3 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto3 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto3 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto3 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv3 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv3 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv3 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri3 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri3 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri3 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag4

# VERANO
verano = series4.loc[(series4[0] == 1) | (series4[0] == 2) | (series4[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series4.loc[(series4[0] == 3) | (series4[0] == 4) | (series4[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series4.loc[(series4[0] == 6) | (series4[0] == 7) | (series4[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series4.loc[(series4[0] == 9) | (series4[0] == 10) | (series4[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver4 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver4 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver4 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto4 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto4 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto4 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv4 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv4 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv4 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri4 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri4 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri4 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag5

# VERANO
verano = series5.loc[(series5[0] == 1) | (series5[0] == 2) | (series5[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series5.loc[(series5[0] == 3) | (series5[0] == 4) | (series5[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series5.loc[(series5[0] == 6) | (series5[0] == 7) | (series5[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series5.loc[(series5[0] == 9) | (series5[0] == 10) | (series5[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver5 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver5 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver5 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto5 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto5 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto5 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv5 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv5 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv5 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri5 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri5 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri5 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag6

# VERANO
verano = series6.loc[(series6[0] == 1) | (series6[0] == 2) | (series6[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series6.loc[(series6[0] == 3) | (series6[0] == 4) | (series6[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series6.loc[(series6[0] == 6) | (series6[0] == 7) | (series6[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series6.loc[(series6[0] == 9) | (series6[0] == 10) | (series6[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver6 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver6 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver6 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto6 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto6 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto6 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv6 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv6 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv6 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri6 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri6 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri6 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag7

# VERANO
verano = series7.loc[(series7[0] == 1) | (series7[0] == 2) | (series7[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series7.loc[(series7[0] == 3) | (series7[0] == 4) | (series7[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series7.loc[(series7[0] == 6) | (series7[0] == 7) | (series7[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series7.loc[(series7[0] == 9) | (series7[0] == 10) | (series7[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver7 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver7 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver7 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto7 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto7 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto7 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv7 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv7 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv7 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri7 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri7 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri7 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag8

# VERANO
verano = series8.loc[(series8[0] == 1) | (series8[0] == 2) | (series8[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series8.loc[(series8[0] == 3) | (series8[0] == 4) | (series8[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series8.loc[(series8[0] == 6) | (series8[0] == 7) | (series8[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series8.loc[(series8[0] == 9) | (series8[0] == 10) | (series8[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver8 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver8 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver8 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto8 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto8 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto8 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv8 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv8 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv8 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri8 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri8 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri8 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag9

# VERANO
verano = series9.loc[(series9[0] == 1) | (series9[0] == 2) | (series9[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series9.loc[(series9[0] == 3) | (series9[0] == 4) | (series9[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series9.loc[(series9[0] == 6) | (series9[0] == 7) | (series9[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series9.loc[(series9[0] == 9) | (series9[0] == 10) | (series9[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver9 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver9 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver9 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]

Vuruoto9 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto9 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto9 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv9 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv9 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv9 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri9 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri9 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri9 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]

####lag10

# VERANO
verano = series10.loc[(series10[0] == 1) | (series10[0] == 2) | (series10[0] == 12)]
Vf1v = verano.loc[verano[1] == 1]
Vf2v = verano.loc[verano[1] == 2]
Vf3v = verano.loc[verano[1] == 3]
Vf4v = verano.loc[verano[1] == 4]
Vf5v = verano.loc[verano[1] == 5]
Vf6v = verano.loc[verano[1] == 6]
Vf7v = verano.loc[verano[1] == 7]
Vf8v = verano.loc[verano[1] == 8]

# OTOÑO
otono = series10.loc[(series10[0] == 3) | (series10[0] == 4) | (series10[0] == 5)]
Vf1o = otono.loc[otono[1] == 1]
Vf2o = otono.loc[otono[1] == 2]
Vf3o = otono.loc[otono[1] == 3]
Vf4o = otono.loc[otono[1] == 4]
Vf5o = otono.loc[otono[1] == 5]
Vf6o = otono.loc[otono[1] == 6]
Vf7o = otono.loc[otono[1] == 7]
Vf8o = otono.loc[otono[1] == 8]

# INVIERNO
invierno = series10.loc[(series10[0] == 6) | (series10[0] == 7) | (series10[0] == 8)]
Vf1i = invierno.loc[invierno[1] == 1]
Vf2i = invierno.loc[invierno[1] == 2]
Vf3i = invierno.loc[invierno[1] == 3]
Vf4i = invierno.loc[invierno[1] == 4]
Vf5i = invierno.loc[invierno[1] == 5]
Vf6i = invierno.loc[invierno[1] == 6]
Vf7i = invierno.loc[invierno[1] == 7]
Vf8i = invierno.loc[invierno[1] == 8]

# primavera
primavera = series10.loc[(series10[0] == 9) | (series10[0] == 10) | (series10[0] == 11)]
Vf1p = primavera.loc[primavera[1] == 1]
Vf2p = primavera.loc[primavera[1] == 2]
Vf3p = primavera.loc[primavera[1] == 3]
Vf4p = primavera.loc[primavera[1] == 4]
Vf5p = primavera.loc[primavera[1] == 5]
Vf6p = primavera.loc[primavera[1] == 6]
Vf7p = primavera.loc[primavera[1] == 7]
Vf8p = primavera.loc[primavera[1] == 8]

Vuruver10 = [Vf1v[4].mean()*Vuru_p_v,Vf2v[4].mean()*Vuru_p_v,Vf3v[4].mean()*Vuru_p_v,Vf4v[4].mean()*Vuru_p_v,Vf5v[4].mean()*Vuru_p_v,Vf6v[4].mean()*Vuru_p_v,Vf7v[4].mean()*Vuru_p_v,Vf8v[4].mean()*Vuru_p_v ]
Vargver10 = [Vf1v[5].mean()*Varg_p_v,Vf2v[5].mean()*Varg_p_v,Vf3v[5].mean()*Varg_p_v,Vf4v[5].mean()*Varg_p_v,Vf5v[5].mean()*Varg_p_v,Vf6v[5].mean()*Varg_p_v,Vf7v[5].mean()*Varg_p_v,Vf8v[5].mean()*Varg_p_v ]
Vchiver10 = [Vf1v[6].mean()*Vchi_p_v,Vf2v[6].mean()*Vchi_p_v,Vf3v[6].mean()*Vchi_p_v,Vf4v[6].mean()*Vchi_p_v,Vf5v[6].mean()*Vchi_p_v,Vf6v[6].mean()*Vchi_p_v,Vf7v[6].mean()*Vchi_p_v,Vf8v[6].mean()*Vchi_p_v ]
print(Vargver10)
Vuruoto10 = [Vf1o[4].mean()*Vuru_p_o,Vf2o[4].mean()*Vuru_p_o,Vf3o[4].mean()*Vuru_p_o,Vf4o[4].mean()*Vuru_p_o,Vf5o[4].mean()*Vuru_p_o,Vf6o[4].mean()*Vuru_p_o,Vf7o[4].mean()*Vuru_p_o,Vf8o[4].mean()*Vuru_p_o ]
Vargoto10 = [Vf1o[5].mean()*Varg_p_o,Vf2o[5].mean()*Varg_p_o,Vf3o[5].mean()*Varg_p_o,Vf4o[5].mean()*Varg_p_o,Vf5o[5].mean()*Varg_p_o,Vf6o[5].mean()*Varg_p_o,Vf7o[5].mean()*Varg_p_o,Vf8o[5].mean()*Varg_p_o ]
Vchioto10 = [Vf1o[6].mean()*Vchi_p_o,Vf2o[6].mean()*Vchi_p_o,Vf3o[6].mean()*Vchi_p_o,Vf4o[6].mean()*Vchi_p_o,Vf5o[6].mean()*Vchi_p_o,Vf6o[6].mean()*Vchi_p_o,Vf7o[6].mean()*Vchi_p_o,Vf8o[6].mean()*Vchi_p_o ]

Vuruinv10 = [Vf1i[4].mean()*Vuru_p_i,Vf2i[4].mean()*Vuru_p_i,Vf3i[4].mean()*Vuru_p_i,Vf4i[4].mean()*Vuru_p_i,Vf5i[4].mean()*Vuru_p_i,Vf6i[4].mean()*Vuru_p_i,Vf7i[4].mean()*Vuru_p_i,Vf8i[4].mean()*Vuru_p_i ]
Varginv10 = [Vf1i[5].mean()*Varg_p_i,Vf2i[5].mean()*Varg_p_i,Vf3i[5].mean()*Varg_p_i,Vf4i[5].mean()*Varg_p_i,Vf5i[5].mean()*Varg_p_i,Vf6i[5].mean()*Varg_p_i,Vf7i[5].mean()*Varg_p_i,Vf8i[5].mean()*Varg_p_i ]
Vchiinv10 = [Vf1i[6].mean()*Vchi_p_i,Vf2i[6].mean()*Vchi_p_i,Vf3i[6].mean()*Vchi_p_i,Vf4i[6].mean()*Vchi_p_i,Vf5i[6].mean()*Vchi_p_i,Vf6i[6].mean()*Vchi_p_i,Vf7i[6].mean()*Vchi_p_i,Vf8i[6].mean()*Vchi_p_i ]

Vurupri10 = [Vf1p[4].mean()*Vuru_p_p,Vf2p[4].mean()*Vuru_p_p,Vf3p[4].mean()*Vuru_p_p,Vf4p[4].mean()*Vuru_p_p,Vf5p[4].mean()*Vuru_p_p,Vf6p[4].mean()*Vuru_p_p,Vf7p[4].mean()*Vuru_p_p,Vf8p[4].mean()*Vuru_p_p ]
Vargpri10 = [Vf1p[5].mean()*Varg_p_p,Vf2p[5].mean()*Varg_p_p,Vf3p[5].mean()*Varg_p_p,Vf4p[5].mean()*Varg_p_p,Vf5p[5].mean()*Varg_p_p,Vf6p[5].mean()*Varg_p_p,Vf7p[5].mean()*Varg_p_p,Vf8p[5].mean()*Varg_p_p ]
Vchipri10 = [Vf1p[6].mean()*Vchi_p_p,Vf2p[6].mean()*Vchi_p_p,Vf3p[6].mean()*Vchi_p_p,Vf4p[6].mean()*Vchi_p_p,Vf5p[6].mean()*Vchi_p_p,Vf6p[6].mean()*Vchi_p_p,Vf7p[6].mean()*Vchi_p_p,Vf8p[6].mean()*Vchi_p_p ]


Vargver = pd.DataFrame({
    'lag10': Vargver10,
    'lag9': Vargver9,
    'lag8': Vargver8,
    'lag7': Vargver7,
    'lag6': Vargver6,
    'lag5': Vargver5,
    'lag4': Vargver4,
    'lag3': Vargver3,
    'lag2': Vargver2,
    'lag1': Vargver1,
    'lag0': Vargver0
})

Vargoto = pd.DataFrame({
    'lag10': Vargoto10,
    'lag9': Vargoto9,
    'lag8': Vargoto8,
    'lag7': Vargoto7,
    'lag6': Vargoto6,
    'lag5': Vargoto5,
    'lag4': Vargoto4,
    'lag3': Vargoto3,
    'lag2': Vargoto2,
    'lag1': Vargoto1,
    'lag0': Vargoto0
})

Varginv = pd.DataFrame({
    'lag10': Varginv10,
    'lag9': Varginv9,
    'lag8': Varginv8,
    'lag7': Varginv7,
    'lag6': Varginv6,
    'lag5': Varginv5,
    'lag4': Varginv4,
    'lag3': Varginv3,
    'lag2': Varginv2,
    'lag1': Varginv1,
    'lag0': Varginv0
})

Vargpri = pd.DataFrame({
    'lag10': Vargpri10,
    'lag9': Vargpri9,
    'lag8': Vargpri8,
    'lag7': Vargpri7,
    'lag6': Vargpri6,
    'lag5': Vargpri5,
    'lag4': Vargpri4,
    'lag3': Vargpri3,
    'lag2': Vargpri2,
    'lag1': Vargpri1,
    'lag0': Vargpri0
})

Vuruver = pd.DataFrame({
    'lag10': Vuruver10,
    'lag9': Vuruver9,
    'lag8': Vuruver8,
    'lag7': Vuruver7,
    'lag6': Vuruver6,
    'lag5': Vuruver5,
    'lag4': Vuruver4,
    'lag3': Vuruver3,
    'lag2': Vuruver2,
    'lag1': Vuruver1,
    'lag0': Vuruver0
})

Vuruoto = pd.DataFrame({
    'lag10': Vuruoto10,
    'lag9': Vuruoto9,
    'lag8': Vuruoto8,
    'lag7': Vuruoto7,
    'lag6': Vuruoto6,
    'lag5': Vuruoto5,
    'lag4': Vuruoto4,
    'lag3': Vuruoto3,
    'lag2': Vuruoto2,
    'lag1': Vuruoto1,
    'lag0': Vuruoto0
})

Vuruinv = pd.DataFrame({
    'lag10': Vuruinv10,
    'lag9': Vuruinv9,
    'lag8': Vuruinv8,
    'lag7': Vuruinv7,
    'lag6': Vuruinv6,
    'lag5': Vuruinv5,
    'lag4': Vuruinv4,
    'lag3': Vuruinv3,
    'lag2': Vuruinv2,
    'lag1': Vuruinv1,
    'lag0': Vuruinv0
})

Vurupri = pd.DataFrame({
    'lag10': Vurupri10,
    'lag9': Vurupri9,
    'lag8': Vurupri8,
    'lag7': Vurupri7,
    'lag6': Vurupri6,
    'lag5': Vurupri5,
    'lag4': Vurupri4,
    'lag3': Vurupri3,
    'lag2': Vurupri2,
    'lag1': Vurupri1,
    'lag0': Vurupri0
})

Vchiver = pd.DataFrame({
    'lag10': Vchiver10,
    'lag9': Vchiver9,
    'lag8': Vchiver8,
    'lag7': Vchiver7,
    'lag6': Vchiver6,
    'lag5': Vchiver5,
    'lag4': Vchiver4,
    'lag3': Vchiver3,
    'lag2': Vchiver2,
    'lag1': Vchiver1,
    'lag0': Vchiver0
})

Vchioto = pd.DataFrame({
    'lag10': Vchioto10,
    'lag9': Vchioto9,
    'lag8': Vchioto8,
    'lag7': Vchioto7,
    'lag6': Vchioto6,
    'lag5': Vchioto5,
    'lag4': Vchioto4,
    'lag3': Vchioto3,
    'lag2': Vchioto2,
    'lag1': Vchioto1,
    'lag0': Vchioto0
})

Vchiinv = pd.DataFrame({
    'lag10': Vchiinv10,
    'lag9': Vchiinv9,
    'lag8': Vchiinv8,
    'lag7': Vchiinv7,
    'lag6': Vchiinv6,
    'lag5': Vchiinv5,
    'lag4': Vchiinv4,
    'lag3': Vchiinv3,
    'lag2': Vchiinv2,
    'lag1': Vchiinv1,
    'lag0': Vchiinv0
})

Vchipri = pd.DataFrame({
    'lag10': Vchipri10,
    'lag9': Vchipri9,
    'lag8': Vchipri8,
    'lag7': Vchipri7,
    'lag6': Vchipri6,
    'lag5': Vchipri5,
    'lag4': Vchipri4,
    'lag3': Vchipri3,
    'lag2': Vchipri2,
    'lag1': Vchipri1,
    'lag0': Vchipri0
})

vmin = min(Vargver.min().min(), Vargoto.min().min(), Varginv.min().min(), Vargpri.min().min(),Vuruver.min().min(), Vuruoto.min().min(), Vuruinv.min().min(), Vurupri.min().min(),Vchiver.min().min(), Vchioto.min().min(), Vchiinv.min().min(), Vchipri.min().min())
vmax = max(Vargver.max().max(), Vargoto.max().max(), Varginv.max().max(), Vargpri.max().max(),Vuruver.max().max(), Vuruoto.max().max(), Vuruinv.max().max(), Vurupri.max().max(),Vchiver.max().max(), Vchioto.max().max(), Vchiinv.max().max(), Vchipri.max().max())
print(vmin)
print(vmax)

colors = ["slateblue", "white", "green"] 

# 2. Create the custom colormap object
# 'BlueToGreenDiverging' is a name for your custom colormap
custom_cmap = LinearSegmentedColormap.from_list("BlueToGreenDiverging", colors)
# ~ figax = plt.subplots(nrows=1,ncols=1,figsize=(5,2.5), sharey=True)
fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4, 3,figsize=(7,5), sharex= True, sharey=True)

ax1.set_title('Argentina  ', fontsize=13)
sns.heatmap(Vargver, annot=False,cmap=custom_cmap, ax=ax1, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0)
ax1.xaxis.set_tick_params(length=0)

sns.heatmap(Vargoto, annot=False,cmap=custom_cmap, ax=ax4,yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax4.set_yticklabels(ax4.get_yticklabels(), rotation=0)
ax4.xaxis.set_tick_params(length=0)

sns.heatmap(Varginv, annot=False,cmap=custom_cmap, ax=ax7, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax7.set_yticklabels(ax7.get_yticklabels(), rotation=0)
ax7.xaxis.set_tick_params(length=0)

sns.heatmap(Vargpri, annot=False,cmap=custom_cmap, ax=ax10, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax10.set_yticklabels(ax10.get_yticklabels(), rotation=0)

ax2.set_title('Uruguay', fontsize=13)
sns.heatmap(Vuruver, annot=False,cmap=custom_cmap, ax=ax2, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax2.xaxis.set_tick_params(length=0)
ax2.yaxis.set_tick_params(length=0)

sns.heatmap(Vuruoto, annot=False,cmap=custom_cmap, ax=ax5,yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax5.xaxis.set_tick_params(length=0)
ax5.yaxis.set_tick_params(length=0)

sns.heatmap(Vuruinv, annot=False,cmap=custom_cmap, ax=ax8, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax8.xaxis.set_tick_params(length=0)
ax8.yaxis.set_tick_params(length=0)

sns.heatmap(Vurupri, annot=False,cmap=custom_cmap, ax=ax11, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax11.yaxis.set_tick_params(length=0)

ax3.set_title('Chile', fontsize=13)
sns.heatmap(Vchiver, annot=False,cmap=custom_cmap, ax=ax3, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax3.xaxis.set_tick_params(length=0)
ax3.yaxis.set_tick_params(length=0)

sns.heatmap(Vchioto, annot=False,cmap=custom_cmap, ax=ax6,yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax6.xaxis.set_tick_params(length=0)
ax6.yaxis.set_tick_params(length=0)

sns.heatmap(Vchiinv, annot=False,cmap=custom_cmap, ax=ax9, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax9.xaxis.set_tick_params(length=0)
ax9.yaxis.set_tick_params(length=0)

sns.heatmap(Vchipri, annot=False,cmap=custom_cmap, ax=ax12, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-10.5, vmax=10.5,cbar=False)
ax12.yaxis.set_tick_params(length=0)

cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
norm = plt.Normalize(vmin=-10.5, vmax=10.5)
sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm)
cbar= fig.colorbar(sm, ax=(ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10,ax11,ax12), location='right', shrink=0.8, cax=cbar_ax)
cbar.set_label('variation [%]', fontsize=14)

fig.subplots_adjust(wspace=0.1, hspace=0.1)
fig.text(0.86, 0.77, 'DJF', fontsize = 14, rotation='vertical')
fig.text(0.86, 0.57, 'MAM', fontsize = 14, rotation='vertical')
fig.text(0.86, 0.39, 'JJA', fontsize = 14, rotation='vertical')
fig.text(0.86, 0.19, 'SON', fontsize = 14, rotation='vertical')
fig.text(0.05, 0.42, 'MJO phase', fontsize=14, rotation='vertical')
fig.subplots_adjust(right=0.85)

plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/heatplot.png',bbox_inches="tight", dpi=600)


'''
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
plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/paisesV-filt.png',bbox_inches="tight", dpi=600)
'''
