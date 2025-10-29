import pandas as pd
import numpy as np

df = pd.read_csv('//home/emi/Documents/MJO/datos/demanda-brasil/CARGA_BRASIL.csv', header=None, delimiter=';')
print(df)

carga_N = df.loc[df[0] == 'N']
carga_NE = df.loc[df[0] == 'NE']
carga_S = df.loc[df[0] == 'S']
carga_SE = df.loc[df[0] == 'SE']

carga_N.to_csv('//home/emi/Documents/MJO/datos/demanda-brasil/carga_N.csv', index=False)  
carga_NE.to_csv('//home/emi/Documents/MJO/datos/demanda-brasil/carga_NE.csv', index=False)  
carga_S.to_csv('//home/emi/Documents/MJO/datos/demanda-brasil/carga_S.csv', index=False)  
carga_SE.to_csv('//home/emi/Documents/MJO/datos/demanda-brasil/carga_SE.csv', index=False)  


