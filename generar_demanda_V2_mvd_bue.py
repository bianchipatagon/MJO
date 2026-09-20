"""
Genera series de demanda sintética (V2) usando ERA5 T2m de las regiones:
  - URU: Departamento de Montevideo  
  - ARG: Provincia de Buenos Aires   

Metodología (Bloomfield et al. 2021):
  HDD(t) = max(T_base_hdd - T(t), 0)
  CDD(t) = max(T(t) - T_base_cdd, 0)
  demand ~ a_base + a_h·HDD + a_c·CDD  [sin ciclo semanal]

Como no tenemos la demanda cruda para calibrar en escala absoluta,
regresamos la anomalía DOY de (HDD, CDD) contra la serie V1 (que ya
es anomalía DOY de la demanda observada). Los coeficientes a_h y a_c
se estiman por OLS. El resultado es la demanda sintética en la misma
escala que V1 pero sin ciclo semanal y usando temperatura ERA5 de MVD/BUE.

Salidas:
  series/uru-demanda_V2b.csv
  series/arg-demanda_V2b.csv
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import xarray as xr
from pathlib import Path

BASE     = Path(__file__).resolve().parent
T2M_DIR  = BASE / "ERA5_composites" / "t2m_daily"
SER_DIR  = BASE / "series"

# ── Cajas geográficas ──────────────────────────────────────────────────────────
# Departamento de Montevideo
MVD = {"lat": (-35.0, -34.45), "lon": (-56.55, -55.75)}
# Provincia de Buenos Aires
BUE = {"lat": (-35, -31.5),  "lon": (-63.0,  -57)}

REGIONS = {"uru": MVD, "arg": BUE}

# Umbrales Emilio (optim_umbral.ipynb, valor inicial / central del barrido)
T_BASE_HDD = 15.5   # °C
T_BASE_CDD = 22.0   # °C

YEARS_START = "2000-01-01"
YEARS_END   = "2022-12-31"


# ── Extracción T2m regional ────────────────────────────────────────────────────
def extract_t2m(box: dict) -> pd.Series:
    lat_s, lat_n = sorted(box["lat"])
    lon_w, lon_e = sorted(box["lon"])
    rows = []
    for nc in sorted(T2M_DIR.glob("t2m_*.nc")):
        with xr.open_dataset(nc) as ds:
            t2m = (
                ds["t2m"]
                .sel(latitude=slice(lat_n, lat_s), longitude=slice(lon_w, lon_e))
                - 273.15          # K → °C
            )
            for day in t2m.valid_time.values:
                val = float(t2m.sel(valid_time=day).mean())
                rows.append((pd.Timestamp(day).normalize(), val))
    s = pd.Series(dict(rows)).sort_index()
    s.index.name = "date"
    return s[YEARS_START:YEARS_END]


# ── Anomalía DOY ───────────────────────────────────────────────────────────────
def doy_anomaly(s: pd.Series) -> pd.Series:
    clim = s.groupby(s.index.dayofyear).mean()
    return s.groupby(s.index.dayofyear).transform(lambda g: g - clim[g.name])


# ── Regresión OLS en espacio de anomalías ─────────────────────────────────────
def fit_and_predict(hdd_anom: pd.Series, cdd_anom: pd.Series,
                    dem_v1: pd.Series) -> pd.Series:
    """
    Regresa dem_v1 (anomalía DOY observada) contra (HDD_anom, CDD_anom).
    Devuelve la demanda sintética en la misma escala que dem_v1.
    """
    common = hdd_anom.index.intersection(cdd_anom.index).intersection(dem_v1.index)
    X = np.column_stack([hdd_anom.loc[common].values,
                         cdd_anom.loc[common].values])
    y = dem_v1.loc[common].values

    # OLS sin intercepto (ambas series son anomalías, media ≈ 0)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    a_h, a_c = beta
    print(f"  a_hdd = {a_h:.2f}   a_cdd = {a_c:.2f}")

    synth = a_h * hdd_anom + a_c * cdd_anom
    r = np.corrcoef(synth.loc[common].values, y)[0, 1]
    print(f"  corr(synth, V1) = {r:.3f}")
    return synth


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    for region, box in REGIONS.items():
        print(f"\n{'='*50}")
        print(f"Región: {region.upper()}  box={box}")

        print("  Extrayendo T2m ERA5...")
        t2m = extract_t2m(box)
        print(f"  T2m: {len(t2m)} días  media={t2m.mean():.1f}°C  "
              f"min={t2m.min():.1f}  max={t2m.max():.1f}")

        hdd = (T_BASE_HDD - t2m).clip(lower=0)
        cdd = (t2m - T_BASE_CDD).clip(lower=0)

        hdd_anom = doy_anomaly(hdd)
        cdd_anom = doy_anomaly(cdd)

        # Cargar V1 como referencia de calibración
        dem_v1 = pd.read_csv(SER_DIR / f"{region}-demanda.csv",
                              index_col=0, parse_dates=True).iloc[:, 0]
        dem_v1 = pd.to_numeric(dem_v1, errors="coerce").dropna()

        print("  Calibrando regresión HDD/CDD → demanda:")
        synth = fit_and_predict(hdd_anom, cdd_anom, dem_v1)

        out = SER_DIR / f"{region}-demanda_V2b.csv"
        synth.to_csv(out, header=True)
        print(f"  Guardado: {out.name}")
        print(f"  Serie: media={synth.mean():.1f}  std={synth.std():.1f}")


if __name__ == "__main__":
    main()
