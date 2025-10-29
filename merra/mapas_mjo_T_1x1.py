import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.feature as feature
from mpl_toolkits.axes_grid1 import AxesGrid
import numpy.ma as ma
import xarray as xr




ds = xr.open_dataset('data/T2M_composite.nc')
print('ds')
print(ds)

fig, ax = plt.subplots(nrows=4,ncols=8, subplot_kw={'projection': ccrs.PlateCarree()}, figsize=(14,8))

cs1=ax[0,0].pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M1_DJF'].data, shading='nearest', cmap = 'bwr' , vmin=-1.5, vmax=1.5)
ax[0,0].add_feature(feature.BORDERS,linewidth=0.8)
ax[0,0].add_feature(feature.COASTLINE,linewidth=0.8)

cs1=ax[0,1].pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M2_DJF'].data, shading='nearest', cmap = 'bwr' , vmin=-1.5, vmax=1.5)
ax[0,1].add_feature(feature.BORDERS,linewidth=0.8)
ax[0,1].add_feature(feature.COASTLINE,linewidth=0.8)

cs1=ax[2,2].pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M3_JJA'].data, shading='nearest', cmap = 'bwr' , vmin=-1.5, vmax=1.5)
ax[2,2].add_feature(feature.BORDERS,linewidth=0.8)
ax[2,2].add_feature(feature.COASTLINE,linewidth=0.8)

cbar = plt.colorbar(cs1,ax=[ax[0,0], ax[0,1], ax[2,2]])
cbar.set_label('rainfall [mm]', fontsize = 14)
cbar.ax.tick_params(labelsize=14) 

cax = cbar.ax
pos1 = cax.get_position()
xshift = pos1.width * -12
pos2 = [pos1.x0-xshift, pos1.y0, pos1.width, pos1.height]
cax.set_position(pos2)
plt.show()
