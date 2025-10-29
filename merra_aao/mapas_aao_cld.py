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

lats_s = [-22.77,-29.13,-24.11,-33.1,-27,-20.27,-20.75,-30,-31.23,-32.25,-25.5,-31.72,-33.3,-30.74,-31.6,-33.1,-30.31,-28.03,-28.14,-26.04,-24.09,-36.22,-30.87,-32.6]
lons_s = [-69.47,-70.9,-68.46,-70.66,-70.15,-69.75,-68.99,-70.65,-70.9,-71,-70.1,-65.05,-66.12,-69.61,-70.07,-68.19,-66.67,-67.59,-66.8,-65.91,-66.72,-65.43,-57.46,-57.44]

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

ds = xr.open_dataset('data/CLDTOT_composite_aao.nc')
ds1 = xr.open_dataset('data/SLP_composite_aao.nc')

cmap = (mpl.colors.ListedColormap(['darkorange', 'orange', 'moccasin', 'white','lightgrey' , 'grey' ,'dimgrey' ])
        .with_extremes(over='black', under='orangered'))
bounds = [6.0, 4, 2, 0.0, -2, -4, -6]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

for k, ax in enumerate(axes):
  i = k//3
  j = k%3
  trim = ('DJF', 'MAM', 'JJA', 'SON')[i]
  phase = j

  field = 'CLDTOT' +str(phase)+trim
  field1 = 'SLP' +str(phase)+trim
  #construyo la correlación del índice i con el trimestre j

  #el shading nearest es para que las coord sean centro de píxel
  im = ax.pcolormesh(ds['lon'].data, ds['lat'].data, ds[field].data*100, cmap = cmap, vmin=-7, vmax=7)
  # ~ ax.contour(ds1['lon'].data, ds1['lat'].data, ds1[field1].data,colors="black", alpha = 0.8, linewidths= 0.5)
  ax.add_feature(feature.BORDERS,linewidth=0.8)
  ax.add_feature(feature.COASTLINE,linewidth=0.8)
  ax.plot(lons_s, lats_s, 'o', color='purple', ms="2", transform=ccrs.PlateCarree(), zorder=101, alpha = 0.7)
  
cb = axes.cbar_axes[0].colorbar(im)
cb.set_label('cloud area fraction [%]', fontsize = 12)
cb.ax.tick_params(labelsize=12) 

fig.text(0.3, 0.75, 'DJF', fontsize = 12, rotation='vertical')
fig.text(0.3, 0.56, 'MAM', fontsize = 12, rotation='vertical')
fig.text(0.3, 0.37, 'JJA', fontsize = 12, rotation='vertical')
fig.text(0.3, 0.18, 'SON', fontsize = 12, rotation='vertical')

fig.text(0.37, 0.89, '<-1', fontsize=12)
fig.text(0.46, 0.89, '[-1,1]', fontsize=12)
fig.text(0.57, 0.89, '>+1', fontsize=12)
fig.text(0.44, 0.92, 'SAM index', fontsize=14)
plt.savefig('CLD.png',bbox_inches="tight", dpi=600)
# ~ plt.show()
