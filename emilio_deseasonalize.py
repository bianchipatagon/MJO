"""
Reproduce el pipeline de deseasonalización de Vera & Cerne 

Cerne, S. B., & Vera, C. S. (2011). Influence of the intraseasonal variability on heat waves in subtropical South America. Climate Dynamics, 36(11), 2265-2277.

Dos pasos, en este orden:
  1) Restar la climatología por día del año (DOY).
  2) Restar la anomalía anual-por-estación: a cada día en (año Y, trimestre S)
     se le resta [mean(raw[Y,S]) − mean(raw[all Y, S])].

Notas:
- Sigue la convención de agrupado.py: los meses se mapean a trimestre por el
  mes-solo, sin cruzar año (Ene, Feb y Dic del MISMO año calendario van juntos
  como 'DJF'). No es la convención meteorológica DJF que cruza años.
- La media DOY y las medias anuales-estacionales se computan sobre TODA la
  serie disponible que se pasa (sin filtro adicional).
- Aplicar SOLO a series usadas en figuras 2–5 (heatmaps y boxplots).
  NO aplicar a composites espaciales (figs 6–8) porque esos operan sobre
  campos ERA5 grillados y su clima ya se computa distinto.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


MONTH_TO_SEASON = {
    1: "DJF", 2: "DJF", 12: "DJF",
    3: "MAM", 4: "MAM", 5: "MAM",
    6: "JJA", 7: "JJA", 8: "JJA",
    9: "SON", 10: "SON", 11: "SON",
}


def emilio_deseasonalize(s: pd.Series) -> pd.Series:
    """
    Devuelve la serie s tras aplicar los dos pasos de agrupado.py (Emilio).
    Preserva DatetimeIndex y NaN. Requiere pd.DatetimeIndex.
    """
    if not isinstance(s.index, pd.DatetimeIndex):
        raise TypeError("s debe tener DatetimeIndex")

    s = s.sort_index()
    idx = s.index

    # ── Paso 1: restar climatología DOY ──────────────────────────────────────
    doy = idx.day_of_year
    doy_clim = s.groupby(doy).mean()
    doy_map  = pd.Series(doy_clim.reindex(doy).values, index=idx)
    d1 = s - doy_map

    # ── Paso 2: restar anomalía anual-por-estación (sobre la SERIE CRUDA) ────
    #   season_year_mean[Y, S] − season_long_mean[S]  → se resta al día
    seasons = pd.Series([MONTH_TO_SEASON[m] for m in idx.month], index=idx)
    years   = pd.Series(idx.year, index=idx)

    season_long_mean = s.groupby(seasons).mean()                  # Series indexada por season
    season_year_mean = s.groupby([years, seasons]).mean()         # MultiIndex (year, season)

    # Alinear per-día: buscar (year, season) del día y calcular anom
    keys = list(zip(years.values, seasons.values))
    year_seas_anom_vals = np.array([
        season_year_mean.loc[(y, se)] - season_long_mean.loc[se]
        if (y, se) in season_year_mean.index else 0.0
        for (y, se) in keys
    ], dtype=float)
    year_seas_anom = pd.Series(year_seas_anom_vals, index=idx)

    return d1 - year_seas_anom


def emilio_deseasonalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica emilio_deseasonalize columna por columna."""
    out = {}
    for col in df.columns:
        s = df[col].dropna()
        out[col] = emilio_deseasonalize(s).reindex(df.index)
    return pd.DataFrame(out, index=df.index)
