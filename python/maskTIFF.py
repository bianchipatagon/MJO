import rasterio
import numpy as np

with rasterio.open("/home/emi/Dropbox/DTEC/MJO/datos/poblacion/tifs/population.tif") as src:
    data = src.read(1)  # read first band
    profile = src.profile

# Mask condition
masked_data = np.where(data, src.nodata, data)

# Save masked raster
with rasterio.open("population_masked.tif", "w", **profile) as dst:
    dst.write(masked_data, 1)
