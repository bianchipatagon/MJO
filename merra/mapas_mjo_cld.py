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
                    nrows_ncols=(4, 8),
                    axes_pad=0.1,
                    cbar_location='right',
                    cbar_mode='single',
                    cbar_pad=0.2,
                    cbar_size='15%',
                    share_all=True,
                    label_mode='keep')

ds = xr.open_dataset('data/CLDTOT_composite.nc')
print('ds')
print(ds)

cmap = (mpl.colors.ListedColormap(['darkorange', 'orange', 'moccasin', 'white','lightgrey' , 'grey' ,'dimgrey' ])
        .with_extremes(over='black', under='orangered'))
bounds = [6.0, 4, 2, 0.0, -2, -4, -6]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

for k, ax in enumerate(axes):
  i = k//8
  j = k%8
  trim = ('DJF', 'MAM', 'JJA', 'SON')[i]
  phase = j+1

  field = 'CLDTOT' +str(phase)+'_'+trim
  #construyo la correlación del índice i con el trimestre j

  #el shading nearest es para que las coord sean centro de píxel
  # ~ im = ax.pcolormesh(ds['lon'].data, ds['lat'].data, ds[field].data*100, shading='nearest', cmap = 'Blues' , vmin=-7, vmax=7)
  im = ax.pcolormesh(ds['lon'].data, ds['lat'].data, ds[field].data*100, shading='nearest', cmap = cmap , vmin=-7, vmax=7)

  ax.add_feature(feature.BORDERS,linewidth=0.8)
  ax.add_feature(feature.COASTLINE,linewidth=0.8)
  ax.plot(lons_s, lats_s, 'o', color='purple', ms="2", transform=ccrs.PlateCarree(), zorder=101, alpha = 0.7)

  if trim=='DJF':
    ax.set_title(str(phase))
  if phase==1:
    ax.set_ylabel(trim)
    ax.set_yticks([])   # https://stackoverflow.com/questions/35479508/cartopy-set-xlabel-set-ylabel-not-ticklabels/35483665#35483665
    #esto de acá me volvió loco insulté al cartopy

cb = axes.cbar_axes[0].colorbar(im)
cb.set_label('cloud area fraction [%]', fontsize = 12)
cb.ax.tick_params(labelsize=12) 

fig.text(0.42, 0.87, 'MJO phase', fontsize=14)
fig.subplots_adjust(wspace=0.1, hspace = 0.1)
plt.savefig('CLD-cmap.png',bbox_inches="tight", dpi=600)

plt.show()
