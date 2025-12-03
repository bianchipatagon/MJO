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


lats_s = [-22.15,-22.87,-25.37,-28.57,-31.32,-34.3,-37.73,-41.23,-42.28,-37.09,-38.61,-38.31,-40.03,-33.21,-32.77,-37.49,-39.56,-39.55,-28.74,-29.42,-43.06,-44.53,-45.65,-47.29,-32.59,-34.1,-30.41,-32.29]
lons_s = [-68.58,-68.97,-69.78,-71.45,-71.6,-71.61,-72.51,-73.15,-73.91,-59.73,-58.82,-62.28,-62.65,-65.08,-66.35,-64.74,-65.69,-69.76,-66.7,-63.72,-65.22,-66.44,-67.75,-66.99,-56.44,-56.09,-56.72,-53.91]

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

ds = xr.open_dataset('/home/emi/Dropbox/DTEC/MJO/datos/mjo/W_composite_2.nc')
ds1 = xr.open_dataset('data/SLP_composite.nc')

cmap = (mpl.colors.ListedColormap(['slateblue', 'mediumslateblue', 'lavender', 'white','palegreen' , 'mediumseagreen' ,'green' ])
        .with_extremes(over='darkgreen', under='darkslateblue'))
bounds = [0.8, 0.6, 0.4, 0.0, -0.4, -0.6, -0.8]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


for k, ax in enumerate(axes):
  i = k//8
  j = k%8
  trim = ('DJF', 'MAM', 'JJA', 'SON')[i]
  phase = j+1

  field = 'W' +str(phase)+'_'+trim
  field1 = 'SLP' +str(phase)+'_'+trim
  #construyo la correlación del índice i con el trimestre j

  #el shading nearest es para que las coord sean centro de píxel
  im = ax.pcolormesh(ds['lon'].data, ds['lat'].data, ds[field].data, shading='nearest', cmap = cmap, vmin= -0.8, vmax=0.8 )
  # ~ ax.contour(ds1['lon'].data, ds1['lat'].data, ds1[field1].data,colors="black", alpha = 0.8, linewidths= 0.5)
  ax.add_feature(feature.BORDERS,linewidth=0.8)
  ax.add_feature(feature.COASTLINE,linewidth=0.8)
  ax.plot(lons_s, lats_s, 'o', color='blue', ms="2", transform=ccrs.PlateCarree(), zorder=101, alpha = 0.7)
  ax.pcolormesh(lons_ele-180, lats_ele, np.squeeze(elev), vmin=1500, vmax=50000, cmap='Greys_r', alpha=0.8, zorder=101)
  ax.set_extent([-75.5, -52, -19,-52.4], crs=ccrs.PlateCarree())
  
  if trim=='DJF':
    ax.set_title(str(phase))
  if phase==1:
    ax.set_ylabel(trim)
    ax.set_yticks([])   # https://stackoverflow.com/questions/35479508/cartopy-set-xlabel-set-ylabel-not-ticklabels/35483665#35483665
    #esto de acá me volvió loco insulté al cartopy

cb = axes.cbar_axes[0].colorbar(im)
cb.set_label('wind speed [m/s]', fontsize = 12)
cb.ax.tick_params(labelsize=12) 

# ~ cbar_ax = fig.add_axes(([0.92, 0.15, 0.02, 0.6]))  #a la derecha
# ~ cbar=fig.colorbar(im, cax = cbar_ax)
# ~ cbar.set_label('Temperature [°c]', fontsize = 12)
# ~ cbar.ax.tick_params(labelsize=12) 

fig.text(0.42, 0.87, 'MJO phase', fontsize=14)
fig.subplots_adjust(wspace=0.1, hspace = 0.1)
plt.savefig('W.png',bbox_inches="tight", dpi=600)

plt.show()
