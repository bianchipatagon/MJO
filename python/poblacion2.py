import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
# ~ from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
import matplotlib as mpl
import numpy as np
import matplotlib.patches as mpatches

with rasterio.open('/home/emi/Documents/MJO/datos/poblacion/tifs/population.tif') as pop:
    im6 = pop.read(1) 
    ext6 = [pop.bounds.left, pop.bounds.right, pop.bounds.bottom, pop.bounds.top]
    nodata = pop.nodata  # Get NoData value
    data = np.ma.masked_equal(im6, nodata)
    data = np.ma.masked_where(data < 30, data)
    
cmap = (mpl.colors.ListedColormap(['red', 'red', 'red', 'red','red' , 'red' ,'red' ])
        .with_extremes(over='red', under='red'))
# ~ cmap = (mpl.colors.ListedColormap(['dimgrey', 'dimgrey', 'dimgrey', 'dimgrey','dimgrey' , 'dimgrey' ,'dimgrey' ])
        # ~ .with_extremes(over='dimgrey', under='dimgrey'))
        
lats_w = [-22.15,-22.87,-25.37,-28.57,-31.32,-34.3,-37.73,-41.23,-42.28,-37.09,-38.61,-38.31,-40.03,-33.21,-32.77,-37.49,-39.56,-39.55,-28.74,-29.42,-43.06,-44.53,-45.65,-47.29,-32.59,-34.1,-30.41,-32.29]
lons_w = [-68.58,-68.97,-69.78,-71.45,-71.6,-71.61,-72.51,-73.15,-73.91,-59.73,-58.82,-62.28,-62.65,-65.08,-66.35,-64.74,-65.69,-69.76,-66.7,-63.72,-65.22,-66.44,-67.75,-66.99,-56.44,-56.09,-56.72,-53.91]
sizes_w = [109,12.5,9,193,46,50,32.4,129,101,175,38,203.4,55.2,48,112.5,40,113,100,217,8,155,24.15,99,126,50,49.5,67.2,51.7]

lats_s = [-22.77,-29.13,-24.11,-33.1,-27,-20.27,-20.75,-30,-31.23,-32.25,-25.5,-31.72,-33.3,-30.74,-31.6,-33.1,-30.31,-28.03,-28.14,-26.04,-24.09,-36.22,-30.87,-32.6]
lons_s = [-69.47,-70.9,-68.46,-70.66,-70.15,-69.75,-68.99,-70.65,-70.9,-71,-70.1,-65.05,-66.12,-69.61,-70.07,-68.19,-66.67,-67.59,-66.8,-65.91,-66.72,-65.43,-57.46,-57.44]
sizes_s = [210,196,180,127,100,26,170,138,3,3,85,65,22,72,82,5,22.5,22,27,98,315,7,134,24]

def main():
    fig = plt.figure(figsize=(3, 4))

#### mapa 1 ####

    ax1 = fig.add_subplot(1, 1, 1,
                          projection=ccrs.PlateCarree())
    im = ax1.imshow(data, extent=ext6, cmap=cmap, vmin= 0, vmax=300, label = '> 30 people/km^2')
    ax1.set_extent([-75, -52, -20,-57], crs=ccrs.PlateCarree())
    ax1.coastlines(resolution="50m",linewidth=1, color='black')
    ax1.add_feature(cfeature.BORDERS)
    ax1.add_feature(cfeature.OCEAN)
    ax1.tick_params(labelsize=10)
    ax1.set_yticks([-25, -35, -45, -55], crs=ccrs.PlateCarree())
    ax1.set_xticks([-72, -65, -58], crs=ccrs.PlateCarree())
    # ~ ax1.text(-67, -29, 'Arg')
    # ~ ax1.text(-57.5, -33, 'Uru')
    # ~ ax1.text(-70.5, -24, 'Chi')
    ax1.add_patch(mpatches.Circle(xy=[-59.3, -34.52], radius=2, color='red', alpha=0.9,fill=False, transform=ccrs.PlateCarree(), zorder=30))
    ax1.add_patch(mpatches.Circle(xy=[-56.2, -34.4], radius=1, color='red', alpha=0.9,fill=False, transform=ccrs.PlateCarree(), zorder=30))
    ax1.add_patch(mpatches.Circle(xy=[-70.66, -33.5], radius=2, color='red', alpha=0.9,fill=False, transform=ccrs.PlateCarree(), zorder=30))
    # ~ ax1.plot(lons_w, lats_w, 'o', color='blue', ms="2", transform=ccrs.PlateCarree(), zorder=101)
    ax1.scatter(lons_w, lats_w, s=sizes_w, c='blue', alpha=0.7, transform=ccrs.PlateCarree(), label = 'wind')
    ax1.scatter(lons_s, lats_s, s=sizes_s, c='gold', alpha=0.7, transform=ccrs.PlateCarree(), label = 'solar')
    # ~ ax1.plot(lons_s, lats_s, 'o', color='orangered', ms="2", transform=ccrs.PlateCarree(), zorder=101, alpha = 0.7)
    # ~ fig.colorbar(im, ax=ax1, label='Population density \n [people/km^2]')
    ax1.legend(bbox_to_anchor=(0.55, 0.32), loc=2, borderaxespad=0., fontsize=8, framealpha=1).get_frame().set_edgecolor("white")
    ax1.set_ylabel("Latitude [°]", fontsize=10)
    ax1.set_xlabel("Longitude [°]", fontsize=10)
    plt.savefig('poblacion.png', dpi=600, bbox_inches="tight")

    # ~ plt.show()

if __name__ == '__main__':
    main()


