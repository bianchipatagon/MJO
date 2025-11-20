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
# ~ projection = ccrs.PlateCarree()
# ~ axes_class = (GeoAxes,
                    # ~ dict(projection=projection))
# ~ fig = plt.figure(1,(8,6))
# ~ axes = AxesGrid(fig, 111, axes_class=axes_class,
                    # ~ nrows_ncols=(4, 3),
                    # ~ axes_pad=0.1,
                    # ~ cbar_location='right',
                    # ~ cbar_mode='single',
                    # ~ cbar_pad=0.2,
                    # ~ cbar_size='5%',
                    # ~ share_all=True,
                    # ~ label_mode='keep')

ds = xr.open_dataset('data/T2M_composite_aao.nc')
ds1 = xr.open_dataset('data/SLP_composite_aao.nc')

cmap = (mpl.colors.ListedColormap(['royalblue', 'cornflowerblue', 'lightsteelblue', 'white','lightsalmon' , 'salmon' ,'red' ])
        .with_extremes(over='darkred', under='darkblue'))
bounds = [1.5, 1, 0.5, 0.0, 0.5, 1, 1.5]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

fig, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8)) = plt.subplots(2, 4, figsize=(6,4), subplot_kw={'projection': ccrs.PlateCarree()})

im = ax1.pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M2DJF'].data, cmap = cmap, vmin= -1.5, vmax=1.5 , transform=ccrs.PlateCarree())
ax1.add_feature(feature.BORDERS,linewidth=1.1)
ax1.add_feature(feature.COASTLINE,linewidth=1.1)
ax1.set_title('DEF', fontsize=12)

im = ax2.pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M2MAM'].data, cmap = cmap, vmin= -1.5, vmax=1.5 , transform=ccrs.PlateCarree())
ax2.add_feature(feature.BORDERS,linewidth=1.1)
ax2.add_feature(feature.COASTLINE,linewidth=1.1)
ax2.set_title('MAM', fontsize=12)

im = ax3.pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M2JJA'].data, cmap = cmap, vmin= -1.5, vmax=1.5 , transform=ccrs.PlateCarree())
ax3.add_feature(feature.BORDERS,linewidth=1.1)
ax3.add_feature(feature.COASTLINE,linewidth=1.1)
ax3.set_title('JJA', fontsize=12)

im = ax4.pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M2SON'].data, cmap = cmap, vmin= -1.5, vmax=1.5 , transform=ccrs.PlateCarree())
ax4.add_feature(feature.BORDERS,linewidth=1.1)
ax4.add_feature(feature.COASTLINE,linewidth=1.1)
ax4.set_title('SON', fontsize=12)

im = ax5.pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M0DJF'].data, cmap = cmap, vmin= -1.5, vmax=1.5 , transform=ccrs.PlateCarree())
ax5.add_feature(feature.BORDERS,linewidth=1.1)
ax5.add_feature(feature.COASTLINE,linewidth=1.1)

im = ax6.pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M0MAM'].data, cmap = cmap, vmin= -1.5, vmax=1.5 , transform=ccrs.PlateCarree())
ax6.add_feature(feature.BORDERS,linewidth=1.1)
ax6.add_feature(feature.COASTLINE,linewidth=1.1)

im = ax7.pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M0JJA'].data, cmap = cmap, vmin= -1.5, vmax=1.5 , transform=ccrs.PlateCarree())
ax7.add_feature(feature.BORDERS,linewidth=1.1)
ax7.add_feature(feature.COASTLINE,linewidth=1.1)

im = ax8.pcolormesh(ds['lon'].data, ds['lat'].data, ds['T2M0SON'].data, cmap = cmap, vmin= -1.5, vmax=1.5 , transform=ccrs.PlateCarree())
ax8.add_feature(feature.BORDERS,linewidth=1.1)
ax8.add_feature(feature.COASTLINE,linewidth=1.1)


cb_ax = fig.add_axes([0.92, 0.1, 0.04, 0.8])
# ~ cb_ax = fig.add_axes([0.6, 0.1, 0.25, 0.8])

cbar = fig.colorbar(im, cax=cb_ax)
cbar.set_label('temperatura [°c]', fontsize = 12)
# ~ cb = axes.cbar_axes.colorbar(im)
# ~ cb.set_label('temperatura [°c]', fontsize = 12)
cbar.ax.tick_params(labelsize=12) 

# ~ fig.text(0.3, 0.75, 'DEF', fontsize = 12, rotation='vertical')
# ~ fig.text(0.3, 0.56, 'MAM', fontsize = 12, rotation='vertical')
# ~ fig.text(0.3, 0.37, 'JJA', fontsize = 12, rotation='vertical')
# ~ fig.text(0.3, 0.18, 'SON', fontsize = 12, rotation='vertical')

fig.text(0.07, 0.27, '<-1', fontsize=12)
fig.text(0.06, 0.67, '>+1', fontsize=12)
fig.text(0.02, 0.4, 'Indice AAO []', fontsize=14, rotation='vertical')
fig.subplots_adjust(hspace=0.1,wspace=0.1)

plt.savefig('t3.png',bbox_inches="tight", dpi=300)
# ~ plt.show()
