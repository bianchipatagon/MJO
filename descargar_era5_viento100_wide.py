"""
Extiende los archivos ERA5 viento100 al dominio geopot [-110,-20].

Los archivos existentes (viento100_daily/) cubren [-90,-30].
Solo descarga las fajas faltantes:
  - Oeste: [-110, -90]
  - Este:  [-30,  -20]

Luego combina oeste + existente + este y guarda en viento100_daily_wide/.
Si el archivo wide ya existe, lo saltea.

Los pedidos a CDS pasan la mayor parte del tiempo en cola del lado del
servidor, así que se mandan varios en simultáneo (ThreadPoolExecutor) en
vez de esperar uno por uno: mientras un pedido espera en cola, otros
pueden estar procesándose o descargándose.
"""

from __future__ import annotations

import threading
import cdsapi
import numpy as np
import xarray as xr
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from era5_descarga_utils import YEARS, MONTHS, HOURS, DAYS, open_nc, daily_mean, daily_scalar_wind_speed, find_var

SRC_DIR  = Path(__file__).resolve().parent / "ERA5_composites" / "viento100_daily"
OUT_DIR  = Path(__file__).resolve().parent / "ERA5_composites" / "viento100_daily_wide"
TMPW_DIR = OUT_DIR / "_tmp_west"
TMPE_DIR = OUT_DIR / "_tmp_east"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TMPW_DIR.mkdir(parents=True, exist_ok=True)
TMPE_DIR.mkdir(parents=True, exist_ok=True)

AREA_WEST = [15, -110, -60, -90]   # faja oeste, solo 20° nuevos
AREA_EAST = [15,  -30, -60, -20]   # faja este,  solo 10° nuevos

VARS_OUT = ["u100", "v100", "ws100"]

# Pedidos simultáneos a CDS (2 meses en paralelo = 4 pedidos: oeste+este
# de cada uno). CDS no publica un límite fijo por usuario; si la cola
# empieza a tardar más de lo normal por mandar muchos a la vez, bajar
# este número.
MAX_WORKERS = 4

_thread_local = threading.local()


def _client() -> cdsapi.Client:
    """Un cdsapi.Client por hilo (evita compartir sesión HTTP entre threads)."""
    if not hasattr(_thread_local, "client"):
        _thread_local.client = cdsapi.Client()
    return _thread_local.client


def download_strip(yr, mo, area, tmp_path):
    """Descarga una faja horaria y agrega a media diaria. Retorna Dataset."""
    if tmp_path.exists():
        return _to_daily(open_nc(tmp_path))
    raw = tmp_path.with_suffix(".raw.nc")
    _client().retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type": "reanalysis",
            "variable": ["100m_u_component_of_wind", "100m_v_component_of_wind"],
            "year":   str(yr),
            "month":  f"{mo:02d}",
            "day":    DAYS,
            "time":   HOURS,
            "area":   area,
            "format": "netcdf",
        },
        str(raw),
    )
    ds = open_nc(raw)
    result = _to_daily(ds)
    ds.close()
    raw.unlink(missing_ok=True)
    return result


def _to_daily(ds):
    u_v = find_var(ds, ["u100", "u_comp", "100m_u"])
    v_v = find_var(ds, ["v100", "v_comp", "100m_v"])
    u  = daily_mean(ds, u_v)
    v  = daily_mean(ds, v_v)
    ws = daily_scalar_wind_speed(ds, u_v, v_v)
    return xr.Dataset({"u100": u, "v100": v, "ws100": ws})


def merge_and_save(yr, mo, ds_west, ds_east, out_nc):
    """Combina oeste + existente + este a lo largo de longitud y guarda."""
    src = SRC_DIR / f"viento100_{yr}_{mo:02d}.nc"
    if not src.exists():
        print(f"    WARN: no existe {src.name}, saltando")
        return
    ds_mid = xr.open_dataset(src).load()
    merged = xr.concat([ds_west, ds_mid, ds_east], dim="longitude").sortby("longitude")
    enc = {k: {"zlib": True, "complevel": 4} for k in VARS_OUT}
    merged.to_netcdf(out_nc, encoding=enc)
    ds_mid.close()


def process_month(yr, mo, out_nc):
    print(f"  {yr}-{mo:02d}: oeste...", flush=True)
    ds_w = download_strip(yr, mo, AREA_WEST, TMPW_DIR / f"w_{yr}_{mo:02d}.nc")
    print(f"  {yr}-{mo:02d}: este...", flush=True)
    ds_e = download_strip(yr, mo, AREA_EAST, TMPE_DIR / f"e_{yr}_{mo:02d}.nc")
    print(f"  {yr}-{mo:02d}: merge...", flush=True)
    merge_and_save(yr, mo, ds_w, ds_e, out_nc)
    size = f"{out_nc.stat().st_size // 1024} KB" if out_nc.exists() else "sin archivo"
    print(f"  {yr}-{mo:02d}: OK ({size})", flush=True)


def main() -> None:
    pending = []
    for yr in YEARS:
        for mo in MONTHS:
            out_nc = OUT_DIR / f"viento100_{yr}_{mo:02d}.nc"
            if out_nc.exists():
                print(f"  ya existe: {out_nc.name}")
                continue
            pending.append((yr, mo, out_nc))

    print(f"  {len(pending)} meses pendientes, {MAX_WORKERS} descargas en paralelo", flush=True)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(process_month, yr, mo, out_nc): (yr, mo)
            for yr, mo, out_nc in pending
        }
        for fut in futures:
            yr, mo = futures[fut]
            try:
                fut.result()
            except Exception as e:
                print(f"  {yr}-{mo:02d}: ERROR: {e}", flush=True)


if __name__ == "__main__":
    main()
