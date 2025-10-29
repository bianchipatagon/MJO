#hoy es 26 ago 2024
# arranco con los merra que me pasó emi
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#ds = xr.open_dataset('slp_diarios.nc')



def verafilter(ds):
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
    d2 = df.groupby(grp_ary).mean()
##################################################################

    #primero declaro el dataset
    dsaux = xr.Dataset(
            {name +'_'+j:(["lat", "lon"], np.zeros((Nlat,Nlon))) for j in ('DJF', 'MAM', 'JJA', 'SON')},
            coords={
                "lat": ds['lat'].data,
                "lon": ds['lon'].data
            })


    #después lo asigno


    for j in ('DJF', 'MAM', 'JJA', 'SON'):
        # es True cuando fase y trimestre:



        composite = d2.loc[ j ].to_numpy().reshape(Nlat,Nlon)
        dsaux[name +'_'+j].data = composite


    dsaux.to_netcdf(name + '_medias_trim.nc')

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





