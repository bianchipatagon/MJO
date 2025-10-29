#hoy es 26 ago 2024
# arranco con los merra que me pasó emi

import numpy as np

import glob
import xarray as xr
import pandas as pd

#lista1 = glob.glob("MERRA2_401.tavg1_2d_rad_Nx.202109*.nc")
lista1 = glob.glob("MERRA2_*.nc")


data =  xr.open_dataset(lista1[0])
Ndias = len(lista1)
Nlat = data['lat'].size
Nlon = data['lon'].size

wind_array = np.zeros((Ndias, Nlat, Nlon)).astype(np.float32)

dates = pd.date_range(start= '20000101', periods = Ndias)
dates_copy = dates




for file in lista1:
  data =  xr.open_dataset(file)
  fecha = pd.Timestamp( file.split("/")[-1].split(".")[-3] )
#  for name in list(data.keys()):
#    np_arrays[name][dates.get_loc(fecha),:,:] = np.mean(data[name].data,0)  #promedio las horas del día

  wind_array[dates.get_loc(fecha),:,:] = np.mean(np.sqrt(np.square(data['U50M'].data) + np.square(data['V50M'].data)), 0)

  dates_copy = dates_copy.drop(fecha) #ojo es un datetimeindex
  print('\033[1A', end = '\x1b[2K') #LINE_UP,end = LINE_CLEAR )
  print(dates_copy.size )

ds = xr.Dataset(
    {
        W: (["time", "lat", "lon"], wind_array)
    },
    coords={
        "time": dates,
        "lat": data['lat'].data,
        "lon": data['lon'].data
    }
)
ds.to_netcdf('../emi3/W.nc')
