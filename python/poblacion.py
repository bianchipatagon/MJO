import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
import pandas as pd
import geopandas as gpd

cities = r'/home/emi/Dropbox/DTEC/MJO/datos/poblacion/yk247bg4748/data/ne_10m_urban_areas_landscan.shp'
cities = ShapelyFeature(Reader(cities).geometries(),
                                ccrs.PlateCarree(), facecolor='none')

def main():
    fig = plt.figure(figsize=(3, 4))

#### mapa 1 ####

    ax1 = fig.add_subplot(1, 1, 1,
                          projection=ccrs.PlateCarree())
    ax1.set_extent([-75, -52, -20,-57], crs=ccrs.PlateCarree())
    ax1.coastlines(resolution="10m",linewidth=0.7, color='black')
    ax1.add_feature(cfeature.BORDERS)
    ax1.add_feature(cfeature.OCEAN)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax1.xaxis.set_major_formatter(lon_formatter)
    ax1.yaxis.set_major_formatter(lat_formatter)
    ax1.add_feature(cities,linewidth=0.8,edgecolor='grey', facecolor='grey')
    ax1.set_yticks([-25, -35, -45, -55], crs=ccrs.PlateCarree())
    ax1.set_xticks([-72, -65, -58], crs=ccrs.PlateCarree())
    ax1.tick_params(axis='both', labelsize=6)
    
    plt.savefig('poblacion.png', dpi=600, bbox_inches="tight")

    # ~ plt.show()

if __name__ == '__main__':
    main()
