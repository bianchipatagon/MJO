"""
Descarga ERA5 100m u/v wind horaria (mensual) y agrega a media diaria.

Salida: ERA5_composites/viento100_daily/viento100_{YYYY}_{MM}.nc
          variables: u100, v100 (componentes vector medio), ws100 (rapidez escalar media)  [m s**-1]
"""

from __future__ import annotations

import cdsapi
import numpy as np
import xarray as xr
from pathlib import Path
from era5_descarga_utils import AREA, YEARS, MONTHS, HOURS, DAYS, open_nc, daily_mean, daily_scalar_wind_speed, find_var

OUT_DIR = Path(__file__).resolve().parent / "ERA5_composites" / "viento100_daily"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    client = cdsapi.Client()
    for yr in YEARS:
        for mo in MONTHS:
            out_nc = OUT_DIR / f"viento100_{yr}_{mo:02d}.nc"
            if out_nc.exists():
                print(f"  ya existe: {out_nc.name}")
                continue
            tmp = OUT_DIR / f"_tmp_{yr}_{mo:02d}.nc"
            print(f"  {yr}-{mo:02d} ...", end=" ", flush=True)
            try:
                client.retrieve(
                    "reanalysis-era5-single-levels",
                    {
                        "product_type": "reanalysis",
                        "variable": [
                            "100m_u_component_of_wind",
                            "100m_v_component_of_wind",
                        ],
                        "year":   str(yr),
                        "month":  f"{mo:02d}",
                        "day":    DAYS,
                        "time":   HOURS,
                        "area":   AREA,
                        "format": "netcdf",
                    },
                    str(tmp),
                )
                ds   = open_nc(tmp)
                u_v  = find_var(ds, ["u100", "u_comp", "100m_u"])
                v_v  = find_var(ds, ["v100", "v_comp", "100m_v"])
                u    = daily_mean(ds, u_v)
                v    = daily_mean(ds, v_v)
                ws   = daily_scalar_wind_speed(ds, u_v, v_v)
                u.attrs  = {"long_name": "100m U wind component daily mean", "units": "m s**-1"}
                v.attrs  = {"long_name": "100m V wind component daily mean", "units": "m s**-1"}
                ws.attrs = {"long_name": "100m scalar wind speed daily mean", "units": "m s**-1"}
                xr.Dataset({"u100": u, "v100": v, "ws100": ws}).to_netcdf(
                    out_nc,
                    encoding={k: {"zlib": True, "complevel": 4} for k in ["u100", "v100", "ws100"]},
                )
                ds.close()
                tmp.unlink(missing_ok=True)
                print(f"OK ({out_nc.stat().st_size // 1024} KB)")
            except Exception as e:
                tmp.unlink(missing_ok=True)
                print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
