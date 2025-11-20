import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.feature as feature
from mpl_toolkits.axes_grid1 import AxesGrid
import numpy.ma as ma
import xarray as xr
import matplotlib as mpl
from netCDF4 import Dataset


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
                    nrows_ncols=(4, 3),
                    axes_pad=0.1,
                    cbar_location='right',
                    cbar_mode='single',
                    cbar_pad=0.2,
                    cbar_size='5%',
                    share_all=True,
                    label_mode='keep')

ds = xr.open_dataset('data/T2M_composite_aao.nc')
ds1 = xr.open_dataset('data/SLP_composite_aao.nc')

cmap = (mpl.colors.ListedColormap(['royalblue', 'cornflowerblue', 'lightsteelblue', 'white','lightsalmon' , 'salmon' ,'red' ])
        .with_extremes(over='darkred', under='darkblue'))
bounds = [1.5, 1, 0.5, 0.0, 0.5, 1, 1.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

for k, ax in enumerate(axes):
  i = k//3
  j = k%3
    # ~ # Skip middle column (j == 1)
  # ~ if j == 1:
    # ~ ax.set_visible(False)  # Hide the middle column axes
    # ~ continue
  trim = ('DJF', 'MAM', 'JJA', 'SON')[i]
  # ~ phase = j if j < 1 else j - 1  # Adjust phase: 0 stays 0, 2 becomes 1

  phase = j

  field = 'T2M' +str(phase)+trim
  field1 = 'SLP' +str(phase)+trim
  #construyo la correlación del índice i con el trimestre j

  #el shading nearest es para que las coord sean centro de píxel
  im = ax.pcolormesh(ds['lon'].data, ds['lat'].data, ds[field].data, cmap = cmap, vmin= -1.5, vmax=1.5 )
  # ~ ax.contour(ds1['lon'].data, ds1['lat'].data, ds1[field1].data,colors="black", alpha = 0.8, linewidths= 0.5)
  ax.add_feature(feature.BORDERS,linewidth=0.8)
  ax.add_feature(feature.COASTLINE,linewidth=0.8)
  ax.pcolormesh(lons_ele-180, lats_ele, np.squeeze(elev), vmin=1500, vmax=50000, cmap='Greys_r', alpha=0.8, zorder=101)
  ax.set_extent([-75.5, -52, -19,-52.4], crs=ccrs.PlateCarree())

  
cb = axes.cbar_axes[0].colorbar(im)
cb.set_label('temperatura [°c]', fontsize = 12)
cb.ax.tick_params(labelsize=12) 

fig.text(0.3, 0.75, 'DEF', fontsize = 12, rotation='vertical')
fig.text(0.3, 0.56, 'MAM', fontsize = 12, rotation='vertical')
fig.text(0.3, 0.37, 'JJA', fontsize = 12, rotation='vertical')
fig.text(0.3, 0.18, 'SON', fontsize = 12, rotation='vertical')

fig.text(0.37, 0.89, '<-1', fontsize=12)
fig.text(0.57, 0.89, '>+1', fontsize=12)
fig.text(0.44, 0.92, 'Indice AAO', fontsize=14)
  
plt.savefig('t2.png',bbox_inches="tight", dpi=300)
# ~ plt.show()
