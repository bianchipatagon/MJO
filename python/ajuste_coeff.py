import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import calendar
'''
### ARGENTINA
# serie emi temp
dft=pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/temp-arg.txt', sep=';', header=None, names=['year', 'month', 'day', 'value'])
dft['value'] = pd.to_numeric(dft['value'], errors='coerce')
temp=dft.set_index(pd.to_datetime(dft[['year', 'month', 'day']]) )['value']
# serie emi demanda
dfd = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/arg-dem.txt', sep=';', header=None, names=['year', 'month', 'day', 'value'], decimal=',')
dfd['value'] = pd.to_numeric(dfd['value'], errors='coerce')
dem=dfd.set_index(pd.to_datetime(dfd[['year', 'month', 'day']]))['value']

### URUGUAY
# serie emi temp
dft=pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/temp-uru.txt', sep=';', header=None, names=['year', 'month', 'day', 'value'])
dft['value'] = pd.to_numeric(dft['value'], errors='coerce')
temp=dft.set_index(pd.to_datetime(dft[['year', 'month', 'day']]) )['value']
# serie emi demanda
dfd = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/uru-dem.txt', sep=';', header=None, names=['year', 'month', 'day', 'value'], decimal=',')
dfd['value'] = pd.to_numeric(dfd['value'], errors='coerce')
dem=dfd.set_index(pd.to_datetime(dfd[['year', 'month', 'day']]))['value']
'''

### CHILE
# serie emi temp
dft=pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/temp-chi.txt', sep=';', header=None, names=['year', 'month', 'day', 'value'])
dft['value'] = pd.to_numeric(dft['value'], errors='coerce')
temp=dft.set_index(pd.to_datetime(dft[['year', 'month', 'day']]) )['value']
# serie emi demanda
dfd = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/ajuste/chi-dem2.txt', sep=';', header=None, names=['year', 'month', 'day', 'value'], decimal=',')
dfd['value'] = pd.to_numeric(dfd['value'], errors='coerce')
dem=dfd.set_index(pd.to_datetime(dfd[['year', 'month', 'day']]))['value']

# preparo dataframes que necesito
T_base_hdd = 15.5
T_base_cdd = 22.0

df = pd.DataFrame()
df['dem'] = dem
df['temp'] = temp 
df['hdd'] = (T_base_hdd - temp).clip(lower=0)
df['cdd'] = (temp - T_base_cdd).clip(lower=0)
df['t'] = np.arange(len(df))
df['cero'] = np.ones(len(df))

#recorto el período que voy a usar > 2017 para CHILE
df = df.loc[(df.index.year > 2018) & (df.index.year < 2022)]

# ajusto una forma más sencilla todavía
X = df[['cero','t','temp']].values
y = df['dem'].values
beta = np.linalg.solve(X.T @ X, X.T @ y)
df['dem3']=X@beta
# ~ print(',\t'.join(f"{x:.2f}" for x in beta))

# el modelo de 4 parámetros
X = df[['cero','t', 'hdd', 'cdd']].values
y = df['dem'].values
beta = np.linalg.solve(X.T @ X, X.T @ y)
df['dem4']=X@beta
# ~ print(',\t'.join(f"{x:.2f}" for x in beta))

# el modelo de 9 parámetros (sin la lineal)
dummies = pd.get_dummies(df.index.dayofweek, prefix='dow', drop_first=True)
dummies.set_index(df.index, inplace = True)
X = np.concat([
    df[['cero', 'hdd', 'cdd']],
    dummies.values
], axis=1)
y = df['dem'].values
# print(X.shape, y.shape)
beta9 = np.linalg.solve(X.T @ X, X.T @ y)
df['dem9']=X@beta9
# ~ print(',\t'.join(f"{x:.2f}" for x in beta))

# el modelo de 10 parámetros
dummies = pd.get_dummies(df.index.dayofweek, prefix='dow', drop_first=True)
dummies.set_index(df.index, inplace = True)
X = np.concat([
    df[['cero', 't', 'hdd', 'cdd']],
    dummies.values
], axis=1)
y = df['dem'].values
# print(X.shape, y.shape)
beta = np.linalg.solve(X.T @ X, X.T @ y)
df['dem10']=X@beta
# ~ print(',\t'.join(f"{x:.2f}" for x in beta))
dias = list(calendar.day_abbr)

# vuelvo a definir df en todo el período
df=pd.DataFrame()
df['dem'] = dem
df['temp'] = temp 
df['hdd'] = (T_base_hdd - temp).clip(lower=0)
df['cdd'] = (temp - T_base_cdd).clip(lower=0)
# df['t'] = np.arange(len(df))
df['cero'] = np.ones(len(df))
dummies = pd.get_dummies(df.index.dayofweek, prefix='dow', drop_first=True)
dummies.set_index(df.index, inplace = True)
X = np.concat([
    df[['cero', 'hdd', 'cdd']],
    dummies.values
], axis=1)
plt.figure(figsize=(4,3))
df['dem9']=X@beta9
df[['dem','dem9']].resample('ME').mean().plot(ax=plt.gca())
# ~ plt.show()
# ~ df[['temp', 'dem', 'dem9']].to_csv('dem9.csv',float_format='%6.1f')

#conseguite los daatseries de temperatura

# luego:

df=pd.DataFrame()
df['temp'] = temp 
df['hdd'] = (T_base_hdd - temp).clip(lower=0)
df['cdd'] = (temp - T_base_cdd).clip(lower=0)
df['cero'] = np.ones(len(df))
dummies = pd.get_dummies(df.index.dayofweek, prefix='dow', drop_first=True)
X = np.concat([
    df[['cero', 'hdd', 'cdd']],
    dummies.values
], axis=1)
plt.figure(figsize=(4,3))
df['dem9']=X@beta9
df['dem9'].resample('ME').mean().plot(ax=plt.gca())
df[['dem9']].to_csv('demCHI.csv',float_format='%6.1f')

plt.show()
