"""
Descarga ERA5 2m_temperature horaria (mensual) y agrega a media, máxima y mínima diaria.

Salida: ERA5_composites/t2m_daily/t2m_{YYYY}_{MM}.nc  — variables t2m, t2m_max, t2m_min [K]
"""

from __future__ import annotations

import cdsapi
from pathlib import Path
from era5_descarga_utils import AREA, YEARS, MONTHS, HOURS, DAYS, open_nc, daily_mean, daily_max, daily_min, find_var
import xarray as xr

OUT_DIR = Path(__file__).resolve().parent / "ERA5_composites" / "t2m_daily"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    client = cdsapi.Client()
    for yr in YEARS:
        for mo in MONTHS:
            out_nc = OUT_DIR / f"t2m_{yr}_{mo:02d}.nc"
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
                        "variable":     "2m_temperature",
                        "year":         str(yr),
                        "month":        f"{mo:02d}",
                        "day":          DAYS,
                        "time":         HOURS,
                        "area":         AREA,
                        "format":       "netcdf",
                    },
                    str(tmp),
                )
                ds   = open_nc(tmp)
                var  = find_var(ds, ["t2m", "2m_temp"])
                mean = daily_mean(ds, var)
                tmax = daily_max(ds, var)
                tmin = daily_min(ds, var)
                mean.attrs = {"long_name": "2m temperature daily mean", "units": "K"}
                tmax.attrs = {"long_name": "2m temperature daily max",  "units": "K"}
                tmin.attrs = {"long_name": "2m temperature daily min",  "units": "K"}
                xr.Dataset({"t2m": mean, "t2m_max": tmax, "t2m_min": tmin}).to_netcdf(
                    out_nc,
                    encoding={k: {"zlib": True, "complevel": 4} for k in ["t2m", "t2m_max", "t2m_min"]},
                )
                ds.close()
                tmp.unlink(missing_ok=True)
                print(f"OK ({out_nc.stat().st_size // 1024} KB)")
            except Exception as e:
                tmp.unlink(missing_ok=True)
                print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
