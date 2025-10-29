#hoy es 26 ago 2024
# arranco con los merra que me pasó emi
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#ds = xr.open_dataset('slp_diarios.nc')


N =ds.sizes['time'] #  ds['slp']['time'].size
Nlat = ds.sizes['lat']
Nlon = ds.sizes['lon']
name = list(ds.keys())[0]
print(name)
df = pd.DataFrame( ds[name].data.reshape(N, -1)  )  # Reshape 3D to 2D

# Create MultiIndex for columns (lat, lon)
lats = ds['lat'].data
lons = ds['lon'].data
df.columns = pd.MultiIndex.from_product([lats, lons], names=['lat', 'lon'])
df.index = pd.DatetimeIndex(ds['time'].data, name='time')
df = df.loc[pd.date_range(start='20000101',end='20221231')]
##################################################################
#climatologico diario
d1 = df.sub(df.groupby(df.index.day_of_year).transform('mean') )   #.mean() es distinto cambia el índice no se bien cómo

#esto lo saqué de stackoverflow
month_to_season_dct = {
    1: 'DJF', 2: 'DJF',
    3: 'MAM', 4: 'MAM', 5: 'MAM',
    6: 'JJA', 7: 'JJA', 8: 'JJA',
    9: 'SON', 10: 'SON', 11: 'SON',
    12: 'DJF'
}
grp_ary = [month_to_season_dct.get(t_stamp.month) for t_stamp in df.index]
d2 = d1.sub(df.groupby([df.index.year, grp_ary]).transform('mean')) ## no la podés creer
d2 = d2.add(df.groupby(grp_ary).transform('mean')) # te morís
##################################################################

#chequeamos
# plt.clf()
# (df[-52,-75] - df[-52,-75].mean()).iloc[:200].plot()
# d1[-52,-75].iloc[:200].plot()
# d2[-52,-75].iloc[:200].plot()
# plt.gca().legend()
# plt.savefig('d1.png')


#     mjo = pd.read_csv('../serie_mjo.csv', delimiter = ",") #esto es en el cluster
#     dates_mjo = pd.to_datetime(mjo[['year','month','day']])
#
#     mjo = mjo.set_index(dates_mjo).loc[pd.date_range(start='20000101',end='20240701')]   #  .loc[df.index])
#
aao = pd.read_csv('AAO_agrup.txt',header=None)
aao[0]=pd.DatetimeIndex(aao[0])
aao.set_index(0, inplace=True)
aao.columns = ['amplitude']



#primero declaro el dataset vacío
dsaux = xr.Dataset(
        {name+str(i)+j:(["lat", "lon"], np.zeros((Nlat,Nlon))) for i in range(3) for j in ('DJF', 'MAM', 'JJA', 'SON')},
        coords={
            "lat": ds['lat'].data,
            "lon": ds['lon'].data
        })


#después lo asigno
print("#amplitudes > 1: " + str((abs(aao['amplitude'])>1).sum() ))
# for phase in range(1, 9):
for i in range(3):
    for j in ('DJF', 'MAM', 'JJA', 'SON'):
        # es True cuando fase y trimestre:
        if phase == 0:
            filas = (np.array(grp_ary)==j) & (aao['amplitude']<=-1)
        if phase == 1:
            filas = (np.array(grp_ary)==j) & (abs(aao['amplitude'])<1)
        if phase == 2:
            filas = (np.array(grp_ary)==j) & (aao['amplitude']>=1)
        print('mes_'+j+": ", filas.sum(), end = " ")
        phasecut = d2.loc[filas]
        composite = phasecut.mean().to_numpy().reshape(Nlat,Nlon)
        dsaux[name+str(i) +j].data = composite
print()
dsaux.to_netcdf(name + '_composite_aao.nc')

    return name

ds = xr.open_dataset('SLP.nc')
verafilter(ds)

ds = xr.open_dataset('T2M.nc')
verafilter(ds)

ds = xr.open_dataset('TS.nc')
verafilter(ds)

ds = xr.open_dataset('T2M.nc')
verafilter(ds)

ds = xr.open_dataset('U50M.nc')
verafilter(ds)

ds = xr.open_dataset('V50M.nc')
verafilter(ds)

d1 = xr.open_dataset('SWGDN.nc')
d2 = xr.open_dataset('SWTDN.nc')
ds = xr.Dataset(
            {'TOMI': (["time", "lat", "lon"], d1['SWGDN'].data/d2['SWTDN'].data  ) },
            coords={
                "time": d1['time'].data,
                "lat": d1['lat'].data,
                "lon": d1['lon'].data
            })
verafilter(ds)





