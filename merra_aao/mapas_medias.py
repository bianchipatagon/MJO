import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.feature as feature
from mpl_toolkits.axes_grid1 import AxesGrid
import numpy.ma as ma
import xarray as xr


########   uso AxesGrid  (rompe los huevos con el axes_class)
projection = ccrs.PlateCarree()
axes_class = (GeoAxes,
                    dict(projection=projection))
fig = plt.figure(1,(8,6))
axes = AxesGrid(fig, 111, axes_class=axes_class,
                    nrows_ncols=(3, 4),
                    axes_pad=0.1,
                    cbar_location='right',
                    cbar_mode='edge',
                    cbar_pad=0.2,
                    cbar_size='15%',
                    #direction="column",
                    label_mode='1')  # note the empty label_mode



for k, ax in enumerate(axes):
  trim = ('DJF', 'MAM', 'JJA', 'SON')[k%4]
  var = ('SLP', 'T2M', 'TOMI') [k//4]

  field = var+'_'+trim
  ds = xr.open_dataset('data/'+var+'_medias_trim.nc')
  im = ax.pcolormesh(ds['lon'].data, ds['lat'].data, ds[field].data, shading='nearest')


  ax.add_feature(feature.BORDERS,linewidth=0.5)
  ax.add_feature(feature.COASTLINE,linewidth=0.5)
  if trim=='SON':
     cb = axes.cbar_axes[k//4].colorbar(im)
#axes.cbar_axes[0].toggle_label(True)
for i in range(3):
   axes.cbar_axes[i].axis[axes.cbar_axes[i].orientation].set_label(('SLP', 'T2M', 'TOMI')[i])




fig.text(0.08, 0.78, 'DEF', ha='center',fontsize=13)
fig.text(0.08, 0.62, 'MAM', ha='center',fontsize=13)
fig.text(0.08, 0.43, 'JJA', ha='center',fontsize=13)
fig.text(0.08, 0.25, 'SON', ha='center',fontsize=13)
#plt.savefig('mapas3.png',dpi = 300 ,bbox_inches="tight")
plt.show()
