import pandas as pd
import numpy as np

# ~ df = pd.read_table('serie-prueba.txt', delimiter = ';', header=None)
# ~ df.index= pd.date_range(start='1984-01-01', end='2022-12-31', freq = 'D')
df = pd.read_csv('/home/emi/Documents/MJO/datos/AAO/aao.txt', header=None, delimiter=',')
df.index= pd.date_range(start='2000-01-01', end='2022-12-31', freq = 'D')

dmedio = df.groupby([df.index.day_of_year]).mean(numeric_only = True)
dmedio[[0, 1, 2]] = 0  # así me quedan las columnas con la fecha cuando reste abajo
print(dmedio)

#ahora tengo que indexar a df
#para que al enésimo día de cada año le
#pueda restar la dmedia de ese día del año
#son vectores de distinto tamaño pero pandas los resta igual 
#(siempre que no tenga índices repetidos uno de los dos?) 
                        
d1 = df.set_index(df.index.day_of_year)- dmedio  
fechas = pd.to_datetime(d1[0].astype("string")+'-'+d1[1].astype("string")+'-'+d1[2].astype("string"))
d2 = pd.Series(data = d1[3].to_numpy(), index = fechas)


#esto lo saqué de stackoverflow
month_to_season_dct = {
    1: 'DJF', 2: 'DJF',
    3: 'MAM', 4: 'MAM', 5: 'MAM',
    6: 'JJA', 7: 'JJA', 8: 'JJA',
    9: 'SON', 10: 'SON', 11: 'SON',
    12: 'DJF'
}
grp_ary = [month_to_season_dct.get(t_stamp.month) for t_stamp in df.index]

#agrego una colunma al dataframe
df['trim']= grp_ary
smedia = df.groupby([df['trim']]).mean(numeric_only=True)
# ???           d2.sort_index(inplace = True) # lis taylor
smedia[0]=0 # mismo que antes, en este caso solo importa el año
#otra vez resto vectores de distinto tamaño
s1 = df.groupby([df.index.year,df['trim']]).mean(numeric_only=True).droplevel(0)-smedia
s1.drop([1,2], axis=1, inplace = True)

#reacomodo en multiíndice
s2 = pd.Series(s1[3].to_numpy(), index = [s1.index, s1[0].astype("int").to_numpy()])
print(s2)

#tonces ahora tengo d2 y s1
#armo un dataframe para hacer la cuenta
dtotal = pd.DataFrame(index=df.index, data = df[0])
dtotal[0]=0 # lo inicializo

for i in d2.index: # para cada día de d2 resto el s2 de ese trimestre y año
    dtotal.loc[i] = d2.loc[i] - s2[month_to_season_dct[i.month], i.year]
print(dtotal)
dtotal.to_csv("/home/emi/Documents/MJO/datos/AAO/AAO_agrup.csv")


