import pandas as pd
import numpy as np

df = pd.read_csv('/home/emi/Dropbox/DTEC/MJO/datos/demanda/demanda-horaria-chile2.txt', header=None, delimiter=';')
df.index= pd.date_range(start='2014-01-01', end='2023-01-01', freq = 'H')
print(df)

df = df.resample('D').sum()
print(df[1])

df[1].to_csv("/home/emi/Dropbox/DTEC/MJO/datos/demanda/demanda-chile-diario.csv")
