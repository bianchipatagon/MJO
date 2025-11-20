import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.feature as feature
from mpl_toolkits.axes_grid1 import AxesGrid
import numpy.ma as ma
import xarray as xr
from netCDF4 import Dataset
import matplotlib as mpl

elevat = '/home/emi/Documents/vientohidro2/datos/elev.0.5-deg.nc'
archivo8 = Dataset(elevat, mode ='r')
lons_ele = archivo8.variables['lon'][:]
lats_ele = archivo8.variables['lat'][:]
lons_ele = lons_ele - 180
elev = archivo8.variables['data'][:]
elev = ma.masked_where(elev < 1500, elev)

########   uso AxesGrid  (rompe los huevos con el axes_class)
projection = ccrs.PlateCarree()
axes_class = (GeoAxes,
                    dict(projection=projection))
fig = plt.figure(1,(8,6))
axes = AxesGrid(fig, 111, axes_class=axes_class,
                    nrows_ncols=(4, 8),
                    axes_pad=0.1,
                    cbar_location='right',
                    cbar_mode='single',
                    cbar_pad=0.2,
                    cbar_size='15%',
                    share_all=True,
                    label_mode='keep')

ds = xr.open_dataset('data/T2M_composite.nc')
print('ds')
print(ds)

cmap = (mpl.colors.ListedColormap(['royalblue', 'cornflowerblue', 'lightsteelblue', 'white','lightsalmon' , 'salmon' ,'red' ])
        .with_extremes(over='darkred', under='darkblue'))
bounds = [1.5, 1, 0.5, 0.0, 0.5, 1, 1.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

for k, ax in enumerate(axes):
  i = k//8
  j = k%8
  trim = ('DJF', 'MAM', 'JJA', 'SON')[i]
  phase = j+1

  field = 'T2M' +str(phase)+'_'+trim
  #construyo la correlación del índice i con el trimestre j

  #el shading nearest es para que las coord sean centro de píxel
  # ~ im = ax.pcolormesh(ds['lon'].data, ds['lat'].data, ds[field].data, shading='nearest', cmap = 'RdYlBu_r' , vmin=-1.5, vmax=1.5)
  im = ax.pcolormesh(ds['lon'].data, ds['lat'].data, ds[field].data, shading='nearest', cmap = cmap , vmin=-1.5, vmax=1.5)
  # ~ im = ax.pcolormesh(ds['lon'].data, ds['lat'].data, ds[field].data, shading='nearest', cmap = 'RdYlBu_r')
  ax.add_feature(feature.BORDERS,linewidth=0.8)
  ax.add_feature(feature.COASTLINE,linewidth=0.8)
  ax.pcolormesh(lons_ele-180, lats_ele, np.squeeze(elev), vmin=1500, vmax=50000, cmap='Greys_r', alpha=0.8, zorder=101)
  ax.set_extent([-75.5, -52, -19,-52.4], crs=ccrs.PlateCarree())


  if trim=='DJF':
    ax.set_title(str(phase))
  if phase==1:
    ax.set_ylabel(trim)
    ax.set_yticks([])   # https://stackoverflow.com/questions/35479508/cartopy-set-xlabel-set-ylabel-not-ticklabels/35483665#35483665
    #esto de acá me volvió loco insulté al cartopy

cb = axes.cbar_axes[0].colorbar(im)
cb.set_label('temperatura [°c]', fontsize = 12)
cb.ax.tick_params(labelsize=12) 

# ~ cbar_ax = fig.add_axes(([0.92, 0.15, 0.02, 0.6]))  #a la derecha
# ~ cbar=fig.colorbar(im, cax = cbar_ax)
# ~ cbar.set_label('Temperature [°c]', fontsize = 12)
# ~ cbar.ax.tick_params(labelsize=12) 

fig.text(0.42, 0.87, 'fase MJO ', fontsize=14)
fig.subplots_adjust(wspace=0.1, hspace = 0.1)
plt.savefig('T2M.png',bbox_inches="tight", dpi=600)

plt.show()
