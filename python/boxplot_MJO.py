import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import math


sol = pd.read_csv('rad_SSA.txt', header=None, delimiter=',', na_values='-99')
mad = pd.read_csv('prueba_MJO.txt', header=None, delimiter=',', na_values='-99')

series = pd.DataFrame()
series[0] = mad[5]
for i in range(1, 26):
	series[i] = sol[i-1]

f1 = series.loc[series[0] == 1]
f2 = series.loc[series[0] == 2]
f3 = series.loc[series[0] == 3]
f4 = series.loc[series[0] == 4]
f5 = series.loc[series[0] == 5]
f6 = series.loc[series[0] == 6]
f7 = series.loc[series[0] == 7]
f8 = series.loc[series[0] == 8]

print(f1)
print(f1[1].mean())

prom1 = []
prom2 = []
prom3 = []
prom4 = []
prom5 = []
prom6 = []
prom7 = []
prom8 = []

for i in range(1, 26):
	prom1.append(f1[i].mean())
for i in range(1, 26):
	prom2.append(f2[i].mean())
for i in range(1, 26):
	prom3.append(f3[i].mean())
for i in range(1, 26):
	prom4.append(f4[i].mean())
for i in range(1, 26):
	prom5.append(f5[i].mean())
for i in range(1, 26):
	prom6.append(f6[i].mean())
for i in range(1, 26):
	prom7.append(f7[i].mean())
for i in range(1, 26):
	prom8.append(f8[i].mean())

promedios = [prom1, prom2, prom3,prom4, prom5, prom6, prom7, prom8]

fig, ax = plt.subplots(nrows=1,ncols=1, figsize=(6,5))

ax.boxplot(promedios, whis=(0, 100), showmeans=True, meanline = True, notch=True)
ax.set_xlabel('fase MJO', fontsize=14)
ax.set_ylabel('irradianza [kW-hr/m^2/day]', fontsize=14)
ax.tick_params(labelsize=14)
ax.set_xticks([1,2,3,4,5,6,7,8], ['1','2','3','4','5','6','7','8'])
plt.savefig('boxplot-solar.png',bbox_inches="tight")
plt.show()

