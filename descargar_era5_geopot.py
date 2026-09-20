"""
Descarga ERA5 geopotencial en niveles de presión, hemisferio sur, 2000-2022.

Variables : geopotencial (Z) en 1000 hPa y 200 hPa
Resolución: 1°×1° (suficiente para patrones de gran escala)
Frecuencia : 00/06/12/18 UTC → se promedia a media diaria al guardar
Área       : hemisferio sur completo (0°–90°S, todas las longitudes)
Salida     : ERA5_composites/geopot_daily/geopot_YYYY_MM.nc
             Variables: z1000, z200  [m²/s²], tiempo diario
"""

from __future__ import annotations

import cdsapi
import numpy as np
import xarray as xr
from pathlib import Path

BASE     = Path(__file__).resolve().parent
OUT_DIR  = BASE / "ERA5_composites" / "geopot_daily"
OUT_DIR.mkdir(parents=True, exist_ok=True)

YEARS  = range(2000, 2027)
MONTHS = range(1, 13)
DAYS   = [f"{d:02d}" for d in range(1, 32)]
TIMES  = ["00:00", "06:00", "12:00", "18:00"]
LEVELS = ["1000", "200"]


def main() -> None:
    client = cdsapi.Client()

    for yr in YEARS:
        for mo in MONTHS:
            out_nc = OUT_DIR / f"geopot_{yr}_{mo:02d}.nc"
            if out_nc.exists():
                print(f"  {yr}-{mo:02d}: ya existe, saltando")
                continue

            tmp = OUT_DIR / f"_tmp_geopot_{yr}_{mo:02d}.nc"
            print(f"  {yr}-{mo:02d}: descargando ...", end=" ", flush=True)
            try:
                client.retrieve(
                    "reanalysis-era5-pressure-levels",
                    {
                        "product_type": "reanalysis",
                        "variable": "geopotential",
                        "pressure_level": LEVELS,
                        "year":  str(yr),
                        "month": f"{mo:02d}",
                        "day":   DAYS,
                        "time":  TIMES,
                        "area":  [0, -180, -90, 180],   # hemisferio sur
                        "grid":  ["1.0", "1.0"],          # 1°×1°
                        "format": "netcdf",
                    },
                    str(tmp),
                )

                # Promediar a media diaria
                ds = xr.open_dataset(tmp)
                # Renombrar dim de tiempo si hace falta
                time_dim = next((d for d in ds.dims if "time" in d.lower()), "time")
                if time_dim != "time":
                    ds = ds.rename({time_dim: "time"})

                z = ds["z"]  # (time, level, lat, lon) o (time, lat, lon)

                # Separar niveles y promediar a diario
                if "pressure_level" in z.dims or "level" in z.dims:
                    lev_dim = "pressure_level" if "pressure_level" in z.dims else "level"
                    z1000 = (z.sel({lev_dim: 1000})
                              .drop_vars(lev_dim, errors="ignore")
                              .resample(time="1D").mean())
                    z200  = (z.sel({lev_dim: 200})
                              .drop_vars(lev_dim, errors="ignore")
                              .resample(time="1D").mean())
                else:
                    z1000_v = next(v for v in ds.data_vars if "1000" in v)
                    z200_v  = next(v for v in ds.data_vars if "200"  in v)
                    z1000 = ds[z1000_v].resample(time="1D").mean()
                    z200  = ds[z200_v].resample(time="1D").mean()

                ds.close()
                tmp.unlink(missing_ok=True)

                ds_out = xr.Dataset({
                    "z1000": z1000.astype(np.float32),
                    "z200":  z200.astype(np.float32),
                })
                ds_out.attrs["units"]    = "m2 s-2"
                ds_out.attrs["source"]   = "ERA5 reanalysis-era5-pressure-levels, 1deg, daily mean of 00/06/12/18 UTC"
                enc = {"zlib": True, "complevel": 4}
                ds_out.to_netcdf(out_nc, encoding={"z1000": enc, "z200": enc})
                print("OK")

            except Exception as e:
                tmp.unlink(missing_ok=True)
                print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
