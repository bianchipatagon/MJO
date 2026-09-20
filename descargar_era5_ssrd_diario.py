"""
Descarga ERA5 surface_solar_radiation_downwards horaria (mensual) y agrega
a media diaria en W/m².

Salida: ERA5_composites/ssrd_daily/ssrd_{YYYY}_{MM}.nc  — variable 'ssrd' [W m**-2]
"""

from __future__ import annotations

import cdsapi
from pathlib import Path
from era5_descarga_utils import AREA, YEARS, MONTHS, HOURS, DAYS, open_nc, daily_sum_to_watts, find_var
import xarray as xr

OUT_DIR = Path(__file__).resolve().parent / "ERA5_composites" / "ssrd_daily"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    client = cdsapi.Client()
    for yr in YEARS:
        for mo in MONTHS:
            out_nc = OUT_DIR / f"ssrd_{yr}_{mo:02d}.nc"
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
                        "variable":     "surface_solar_radiation_downwards",
                        "year":         str(yr),
                        "month":        f"{mo:02d}",
                        "day":          DAYS,
                        "time":         HOURS,
                        "area":         AREA,
                        "format":       "netcdf",
                    },
                    str(tmp),
                )
                ds  = open_nc(tmp)
                var = find_var(ds, ["ssrd", "ssr"])
                da  = daily_sum_to_watts(ds, var)
                da.attrs = {"long_name": "Surface solar radiation downwards daily mean", "units": "W m**-2"}
                xr.Dataset({"ssrd": da}).to_netcdf(
                    out_nc, encoding={"ssrd": {"zlib": True, "complevel": 4}}
                )
                ds.close()
                tmp.unlink(missing_ok=True)
                print(f"OK ({out_nc.stat().st_size // 1024} KB)")
            except Exception as e:
                tmp.unlink(missing_ok=True)
                print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
