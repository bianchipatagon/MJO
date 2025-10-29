import glob
from datetime import datetime
import pandas as pd
import xarray as xr
import glob
import numpy as np



lista1 = glob.glob("MERRA2_*.nc")
lista1.sort()
df = pd.DataFrame()
k = 0
for file in lista1:
  k += 1
  # fecha = file.split("/")[-1].split(".")[-3]
  ds = xr.open_dataset(file)
  fecha = ds.RangeBeginningDate
  pddate = pd.to_datetime(fecha)
  if(k%10 == 0): print(fecha)

  data = ds.sel(lat = [-34.86, -34.59, -33.43],
                lon = [-56.166, -58.38, -70.65],
                method = 'nearest')
  data = np.mean(data['CLDTOT'].values, 0)
  data = np.diag(data)

  #paso el array a formato pandas
  pdata = pd.DataFrame( [data], index = [pddate])
  #apilo
  df = pd.concat([df, pdata])
df.sort_index(inplace = True)
df.to_pickle('cldtot.pkl')
