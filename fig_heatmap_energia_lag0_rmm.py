"""
Heatmaps fase × lag de energía usando FMO, siguiendo los scripts de Emilio.

- Índice: FMO.txt, formato tipo filtered.txt de Emilio
- Variables: ERA5 regional (rad, viento) + demanda sintética V2 (HDD/CDD)
- Lags 0-10 (igual a Emilio), fases 1-8 en Y, lags lag10→lag0 en X
- Amplitud > 1.0, como en los scripts de Emilio
- Normalización: group.mean() / σ_estacional × 100  (% de la σ estacional)
- Comparación: fase N vs resto de fases activas (Mann-Whitney U, p < 0.05)
- 3 figuras (una por variable): 4 filas (estaciones) × 2 cols (URU, ARG)
"""

from __future__ import annotations

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.stats import mannwhitneyu
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from agrupar_series_segun_paper import BASE, SERIES_DIR
from emilio_deseasonalize import emilio_deseasonalize

# ── Config ─────────────────────────────────────────────────────────────────────
MJO_INDEX   = "FMO"
MJO_FILE    = "FMO.txt"
YEARS       = range(2000, 2023)
AMP_THRESH  = 1.0
PVAL_THRESH = 0.05
PHASES      = list(range(1, 9))
N_LAGS      = 11                     # lags 0..10

SEASONS  = {"DJF": [12, 1, 2], "MAM": [3, 4, 5], "JJA": [6, 7, 8], "SON": [9, 10, 11]}
LAG_COLS = [f"lag{i}" for i in range(10, -1, -1)]   # lag10 izquierda → lag0 derecha

VARS_URU = {"uru-demanda_V2b": "URU Demand", "uru-rad": "Irradiance URU", "uru-viento": "Wind URU"}
VARS_ARG = {"arg-demanda_V2b": "ARG Demand", "arg-rad": "Irradiance ARG", "arg-viento": "Wind ARG"}

VARTYPES = {
    "demanda": ("Demanda",    LinearSegmentedColormap.from_list("D", ["slateblue", "white", "green"])),
    "rad":     ("Radiación",  LinearSegmentedColormap.from_list("R", ["dimgrey",   "white", "darkorange"])),
    "viento":  ("Viento",     LinearSegmentedColormap.from_list("V", ["steelblue", "white", "firebrick"])),
}

OUT_DIR = BASE / "resultados" / f"14_heatmap_energia_fase_lag_{MJO_INDEX.lower()}"


# ── Carga ──────────────────────────────────────────────────────────────────────
def load_energy_series() -> dict[str, pd.Series]:
    """Series brutas transformadas con la deseasonalización de Emilio
    (agrupado.py, 2 pasos), tal como se usa en las figs 2-5."""
    out = {}
    for key in list(VARS_URU) + list(VARS_ARG):
        s = pd.read_csv(SERIES_DIR / f"{key}.csv", index_col=0, parse_dates=True)
        s = pd.to_numeric(s.iloc[:, 0], errors="coerce").dropna().sort_index()
        out[key] = emilio_deseasonalize(s)
    return out


def vartype_of(key: str) -> str:
    for vt in ("demanda", "rad", "viento"):
        if vt in key:
            return vt
    raise ValueError(key)


def read_fmo_emilio(path: Path) -> pd.DataFrame:
    """Lee FMO.txt con el mismo layout que el filtered.txt de Emilio."""
    df = pd.read_csv(
        path,
        sep=r"[\s,]+",
        header=None,
        names=["year", "month", "day", "weekday", "x1", "x2", "phase", "amplitude"],
        engine="python",
    )
    df["date"] = pd.to_datetime(df[["year", "month", "day"]], errors="coerce")
    df = df.dropna(subset=["date"]).set_index("date").sort_index()
    for col in ["weekday", "x1", "x2", "phase", "amplitude"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["phase"] = df["phase"].where(df["phase"].between(1, 8), np.nan)
    return df


def read_rmm_bom(path: Path) -> pd.DataFrame:
    """Lee RMM_BOM_74toRealtime.txt (2 líneas header, 7 cols, espacios)."""
    df = pd.read_csv(
        path,
        skiprows=2,
        sep=r"\s+",
        header=None,
        names=["year", "month", "day", "rmm1", "rmm2", "phase", "amplitude"],
        engine="python",
        usecols=[0, 1, 2, 3, 4, 5, 6],
    )
    for col in ["rmm1", "rmm2", "phase", "amplitude"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[df["amplitude"] < 1e30]  # eliminar missing values (1.E36)
    df["date"] = pd.to_datetime(df[["year", "month", "day"]], errors="coerce")
    df = df.dropna(subset=["date"]).set_index("date").sort_index()
    df["phase"] = df["phase"].where(df["phase"].between(1, 8), np.nan)
    return df


def load_mjo(path: Path) -> pd.DataFrame:
    if "RMM_BOM" in path.name:
        return read_rmm_bom(path)
    return read_fmo_emilio(path)


# ── Cómputo ────────────────────────────────────────────────────────────────────
def compute_heatmaps(mjo: pd.DataFrame,
                     series: dict[str, pd.Series],
                     varkeys: list[str]) -> dict:
    """
    Retorna results[var][season] = (means_df, pvals_df)
    means en % de la σ estacional; shape (8 fases, 11 lags), cols lag10→lag0.
    """
    common = mjo.index
    for k in varkeys:
        common = common.intersection(series[k].index)
    common = common[(common.year >= YEARS.start) & (common.year < YEARS.stop)]

    mjo_al = mjo.loc[common]

    # σ estacional sobre toda la serie (no solo días activos MJO)
    seasonal_std: dict[str, dict[str, float]] = {}
    for k in varkeys:
        ser = series[k].reindex(common)
        seasonal_std[k] = {
            season: ser[common.month.isin(months)].std()
            for season, months in SEASONS.items()
        }

    s0 = pd.DataFrame({
        "month":     common.month,
        "phase":     mjo_al["phase"].values,
        "amplitude": mjo_al["amplitude"].values,
    })
    for k in varkeys:
        s0[k] = series[k].reindex(common).values

    mjo_cols = ["month", "phase", "amplitude"]

    all_lags = [s0]
    for lag in range(1, N_LAGS):
        p1 = s0[mjo_cols].iloc[:-lag].reset_index(drop=True)
        p2 = s0[varkeys].iloc[lag:].reset_index(drop=True)
        all_lags.append(pd.concat([p1, p2], axis=1))

    all_lags = [s.loc[s["amplitude"] > AMP_THRESH].copy() for s in all_lags]

    results = {k: {} for k in varkeys}

    for season, months in SEASONS.items():
        for k in varkeys:
            std_s = seasonal_std[k][season]
            means_mat = np.full((8, N_LAGS), np.nan)
            pvals_mat = np.full((8, N_LAGS), np.nan)

            for lag_idx, lag_df in enumerate(all_lags):
                seas = lag_df.loc[lag_df["month"].isin(months)]
                for ph_idx, ph in enumerate(PHASES):
                    grp  = seas.loc[seas["phase"].round() == ph, k].dropna()
                    rest = seas.loc[seas["phase"].round() != ph, k].dropna()
                    if len(grp) >= 3 and len(rest) >= 3:
                        means_mat[ph_idx, lag_idx] = grp.mean() / std_s * 100
                        _, p = mannwhitneyu(grp, rest, alternative="two-sided")
                        pvals_mat[ph_idx, lag_idx] = p

            lag_names = [f"lag{i}" for i in range(N_LAGS)]
            results[k][season] = (
                pd.DataFrame(means_mat, index=PHASES, columns=lag_names)[LAG_COLS],
                pd.DataFrame(pvals_mat, index=PHASES, columns=lag_names)[LAG_COLS],
            )

    return results


# ── Figura ─────────────────────────────────────────────────────────────────────
def plot_by_variable(vartype: str,
                     res_uru: dict, uru_key: str, uru_label: str,
                     res_arg: dict, arg_key: str, arg_label: str,
                     out: Path) -> None:
    """1 figura por variable: 4 filas (estaciones) × 2 cols (URU, ARG)."""
    _, cmap = VARTYPES[vartype]
    seasons = list(SEASONS.keys())
    pairs = [(res_uru, uru_key, uru_label), (res_arg, arg_key, arg_label)]

    # escala simétrica común a los dos países
    all_vals = np.concatenate([
        results[key][s][0].values.ravel()
        for results, key, _ in pairs
        for s in seasons
    ])
    all_vals = all_vals[~np.isnan(all_vals)]
    vabs = np.percentile(np.abs(all_vals), 95) if len(all_vals) else 1.0

    fig, axes = plt.subplots(4, 2, figsize=(8.25, 6), sharex=True, sharey=True)
    _, vname = VARTYPES[vartype]
    # ~ fig.suptitle(
        # ~ f"{VARTYPES[vartype][0]}  –  {MJO_INDEX}  |  amp > {AMP_THRESH}"
        # ~ f"  |  * p < {PVAL_THRESH}  |  {YEARS.start}–{YEARS.stop - 1}\n"
        # ~ f"anomalía [% of seasonal σ]  |  fase N vs resto activos",
        # ~ fontsize=9,
    # ~ )

    for col, (results, key, label) in enumerate(pairs):
        for row, season in enumerate(seasons):
            ax = axes[row, col]
            means_df, pvals_df = results[key][season]
            annot = np.where(pvals_df.values < PVAL_THRESH, "*", "")

            sns.heatmap(
                means_df, ax=ax, cmap=cmap,
                vmin=-vabs, vmax=vabs,
                cbar=False,
                annot=annot, fmt="",
                annot_kws={"size": 10, "color": "black", "va": "center"},
                yticklabels=[str(p) for p in PHASES],
            )
            ax.set_yticks(np.arange(len(PHASES)) + 0.5)
            ax.set_yticklabels([str(p) for p in PHASES], rotation=0, fontsize=8)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=7)
            ax.xaxis.set_tick_params(length=0)

            for _, spine in ax.spines.items():
                spine.set_visible(True)
                spine.set_linewidth(1)

            if row == 0:
                ax.set_title(label, fontsize=10, fontweight="bold")
            if col == 0:
                ax.set_ylabel(f"{season}\nMJO phase", fontsize=8)
            else:
                ax.set_ylabel("")
                ax.yaxis.set_tick_params(length=0, labelleft=True)

    fig.subplots_adjust(wspace=0.1, hspace=0.12, left=0.07, right=0.78, top=0.90, bottom=0.07)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=Normalize(-vabs, vabs))
    sm.set_array([])
    cax = fig.add_axes([0.81, 0.12, 0.022, 0.70])
    cbar = fig.colorbar(sm, cax=cax)
    cbar.set_label("% of seasonal σ", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"  → {out}")


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    print("Cargando series de energía...")
    series = load_energy_series()
    print(f"Cargando {MJO_INDEX}...")
    mjo = load_mjo(SERIES_DIR / MJO_FILE)

    all_keys = list(VARS_URU) + list(VARS_ARG)
    print("Computando heatmaps...")
    results = compute_heatmaps(mjo, series, all_keys)

    fig_dir = OUT_DIR / "figuras"

    for vartype in ("rad", "viento", "demanda"):
        uru_key = next(k for k in VARS_URU if vartype in k)
        arg_key = next(k for k in VARS_ARG if vartype in k)
        out = fig_dir / f"heatmap_{vartype}_fase_lag.png"
        plot_by_variable(
            vartype,
            results, uru_key, VARS_URU[uru_key],
            results, arg_key, VARS_ARG[arg_key],
            out,
        )

    print("Listo.")


if __name__ == "__main__":
    main()
