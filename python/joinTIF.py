import rasterio
from rasterio.merge import merge
import glob

# List of TIFF files
tif_files = glob.glob("/home/emi/Dropbox/DTEC/MJO/datos/poblacion/tifs/*.tif")

# Open all TIFFs
src_files_to_mosaic = [rasterio.open(fp) for fp in tif_files]

# Merge them
mosaic, out_trans = merge(src_files_to_mosaic)

# Write the merged output
out_meta = src_files_to_mosaic[0].meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans
})

with rasterio.open("population.tif", "w", **out_meta) as dest:
    dest.write(mosaic)
