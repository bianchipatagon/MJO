"""
Extrae medias regionales ERA5 para los polígonos ARG y URU definidos en
fig_composites_mapas_energia.py, aplicando:
  1. Land-sea mask (lsm >= 0.5)   — excluye océano, Río de la Plata
  2. Elevación < 1000 m            — excluye Andes y terreno alto

Variables: ssrd [W m⁻²] y ws10 [m s⁻¹] (y ws100 cuando esté disponible).
Período: 2000-2022.

Salidas (cache_dir):
  era5_ssrd_uru.csv, era5_ssrd_arg.csv
  era5_ws10_uru.csv, era5_ws10_arg.csv
  (era5_ws100_uru.csv, era5_ws100_arg.csv — cuando descargue viento100)

NO CORRER hasta que esté completa la descarga de viento100_daily (276 archivos).
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
from shapely.geometry import Point, Polygon

BASE      = Path("/home/emi/Documents/MJO/MATILDE/scripts_v6")
SSRD_DIR  = BASE / "ERA5_composites/ssrd_daily"
VIENT_DIR = BASE / "ERA5_composites/viento_daily"
V100_DIR  = BASE / "ERA5_composites/viento100_daily"
LSM_FILE  = BASE / "ERA5_composites/orog_arg_uru.nc"   # contiene lsm
LSM_FILE  = '/home/emi/Documents/vientohidro2/datos/elev.0.5-deg.nc'
Z_FILE    = BASE / "ERA5_composites/z_arg_uru.nc"      # contiene z (geopotential)
CACHE_DIR = BASE / "resultados/18_composites_mapas_energia"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

G = 9.80665
ELEV_MAX  = 1000.0  # m
LSM_MIN   = 0.5

LONG_START = "2000-01-01"
LONG_END   = "2022-12-31"

# ── Polígonos de las regiones (lon, lat) ──────────────────────────────────────
# Tomados de fig_composites_mapas_energia.py
SSRD_BOXES = {
    "URU": Polygon([(-58,-30), (-55.75,-30), (-55.75,-33.5), (-58,-33.5)]),
    "ARG": Polygon([(-67.5,-22), (-63,-22), (-63,-33), (-70,-33)]),
}
WIND_BOXES = {
    "URU": Polygon([(-58,-30.5), (-54.5,-30.5), (-54.5,-34), (-58,-34)]),
    "ARG": Polygon([(-67, -26), (-57, -35), (-60, -50), (-70, -46)]),
}


def build_static_masks(lats: np.ndarray, lons: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns (lsm_mask, elev_mask) each of shape (n_lat, n_lon).
    lsm_mask:  True = land (lsm >= 0.5)
    elev_mask: True = elevation < 1000 m
    """
    ds_lsm = xr.open_dataset(LSM_FILE)
    # ~ ds_z   = xr.open_dataset(Z_FILE)

    # ~ lsm = ds_lsm["lsm"].isel(valid_time=0).interp(
    lsm = ds_lsm["data"].interp(
        lat=lats, lon=lons+180, method="nearest").values
    # ~ z   = ds_z["z"].isel(valid_time=0).interp(
        # ~ latitude=lats, longitude=lons, method="nearest").values / G

    # ~ ds_lsm.close(); ds_z.close()
    ds_lsm.close()

    # ~ return (lsm >= LSM_MIN), (z < ELEV_MAX)
    return (lsm >= LSM_MIN), (lsm < ELEV_MAX)


def polygon_mask(lats: np.ndarray, lons: np.ndarray, poly: Polygon) -> np.ndarray:
    """Boolean mask (n_lat, n_lon): True if grid point is inside polygon."""
    mask = np.zeros((len(lats), len(lons)), dtype=bool)
    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            mask[i, j] = poly.contains(Point(lon, lat))
    return mask


def extract_series(nc_dir: Path, variable: str, glob_pat: str,
                   combined_mask: np.ndarray,
                   target_lats: np.ndarray, target_lons: np.ndarray) -> pd.Series:
    """Average variable over grid points where combined_mask is True."""
    rows = []
    for nc in sorted(nc_dir.glob(glob_pat)):
        with xr.open_dataset(nc) as ds:
            region = ds[variable].sel(
                latitude=target_lats, longitude=target_lons, method="nearest"
            )
            for t_idx in range(len(region.valid_time)):
                slab = region.isel(valid_time=t_idx).values
                val  = np.nanmean(np.where(combined_mask, slab, np.nan))
                t    = pd.Timestamp(region.valid_time.values[t_idx]).normalize()
                rows.append((t, float(val)))
    s = pd.Series(dict(rows)).sort_index()
    s.index.name = "date"
    return s[LONG_START:LONG_END]


def process_variable(nc_dir: Path, variable: str, glob_pat: str,
                     boxes: dict[str, Polygon],
                     lsm_mask: np.ndarray, elev_mask: np.ndarray,
                     target_lats: np.ndarray, target_lons: np.ndarray,
                     out_prefix: str) -> None:
    for region_name, poly in boxes.items():
        out_csv = CACHE_DIR / f"{out_prefix}_{region_name.lower()}.csv"
        if out_csv.exists():
            print(f"  {out_csv.name} ya existe, saltando.")
            continue

        poly_m  = polygon_mask(target_lats, target_lons, poly)
        combined = poly_m & lsm_mask & elev_mask

        n_total = combined.size
        n_keep  = combined.sum()
        print(f"  {region_name}: {n_keep}/{n_total} puntos ({100*n_keep/n_total:.1f}%)")

        if n_keep == 0:
            print(f"  ADVERTENCIA: ningún punto en {region_name}, saltando.")
            continue

        print(f"  Extrayendo {variable} {region_name}...")
        s = extract_series(nc_dir, variable, glob_pat, combined, target_lats, target_lons)
        s.to_csv(out_csv, header=True)
        print(f"  Guardado: {out_csv.name}")


def main(include_ws100: bool = False) -> None:
    # ── Grid de referencia (ssrd usa misma grid que viento) ───────────────────
    ref = xr.open_dataset(sorted(SSRD_DIR.glob("ssrd_*.nc"))[0])
    all_lats = ref.latitude.values
    all_lons = ref.longitude.values
    ref.close()

    # Bounding box amplio que cubra todos los polígonos
    lat_min = min(poly.bounds[1] for poly in {**SSRD_BOXES, **WIND_BOXES}.values()) - 0.5
    lat_max = max(poly.bounds[3] for poly in {**SSRD_BOXES, **WIND_BOXES}.values()) + 0.5
    lon_min = min(poly.bounds[0] for poly in {**SSRD_BOXES, **WIND_BOXES}.values()) - 0.5
    lon_max = max(poly.bounds[2] for poly in {**SSRD_BOXES, **WIND_BOXES}.values()) + 0.5

    lat_mask = (all_lats >= lat_min) & (all_lats <= lat_max)
    lon_mask = (all_lons >= lon_min) & (all_lons <= lon_max)
    target_lats = all_lats[lat_mask]
    target_lons = all_lons[lon_mask]
    print(f"Grid: {len(target_lats)} lats × {len(target_lons)} lons")

    # ── Máscaras estáticas ────────────────────────────────────────────────────
    print("Construyendo máscaras LSM + elevación...")
    lsm_mask, elev_mask = build_static_masks(target_lats, target_lons)
    print(f"  Tierra: {lsm_mask.sum()}/{lsm_mask.size}  "
          f"(<1000m): {elev_mask.sum()}/{elev_mask.size}  "
          f"Ambas: {(lsm_mask & elev_mask).sum()}/{lsm_mask.size}")

    # ── ssrd ──────────────────────────────────────────────────────────────────
    print("\n=== SSRD ===")
    process_variable(SSRD_DIR, "ssrd", "ssrd_*.nc",
                     SSRD_BOXES, lsm_mask, elev_mask,
                     target_lats, target_lons, "era5_ssrd")

    # ── ws10 ─────────────────────────────────────────────────────────────────
    print("\n=== ws10 ===")
    process_variable(VIENT_DIR, "ws10", "viento_*.nc",
                     WIND_BOXES, lsm_mask, elev_mask,
                     target_lats, target_lons, "era5_ws10")

    # ── ws100 (solo si está disponible y completo) ────────────────────────────
    if include_ws100:
        n_files = len(list(V100_DIR.glob("viento100_*.nc")))
        if n_files < 270:
            print(f"\nws100: solo {n_files} archivos disponibles, esperá descarga completa.")
        else:
            print("\n=== ws100 ===")
            process_variable(V100_DIR, "ws100", "viento100_*.nc",
                             WIND_BOXES, lsm_mask, elev_mask,
                             target_lats, target_lons, "era5_ws100")

    print("\nListo.")


if __name__ == "__main__":
    import sys
    include_ws100 = "--ws100" in sys.argv
    main(include_ws100=include_ws100)
