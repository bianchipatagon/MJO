from scipy import signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import linregress
# Example timeseries
df = pd.read_csv('/home/emi/Documents/MJO/datos/demanda-brasil/carga_SE2.txt', header=None, delimiter=',')
df.index= pd.date_range(start='2007-01-01', end='2022-12-31', freq = 'D')
'''
x = np.arange(len(df))
X = sm.add_constant(x)  # agrega el término constante (intercepto)
modelo = sm.OLS(df[3], X).fit()
df['tendencia'] = modelo.predict(X)
'''

x = np.arange(len(df))
y = df[3].values

# Ajustar una regresión lineal
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Calcular la tendencia lineal
df['tendencia'] = intercept + slope * x
df['col_diff'] = df[3] - df['tendencia'] + intercept
df.to_csv('//home/emi/Documents/MJO/datos/demanda-brasil/carga_det.txt', index=False)  

print(df['col_diff'].mean())
df.plot(title='Serie con tendencia lineal')
plt.show()
print(df)
