import numpy as N
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from scipy.signal import detrend
import seaborn as sns
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, Normalize
from scipy.stats import mannwhitneyu

#################################
#######SOL####################
#################################

Vuru = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-sol-agrup.csv', header=None, delimiter=',', na_values='-99')
Varg = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-sol-agrup.csv', header=None, delimiter=',', na_values='-99')
Vchi = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-sol-agrup.csv', header=None, delimiter=',', na_values='-99')

Vuru_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/uru-sol.txt', header=None, delimiter=';', na_values='-99')
Varg_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/arg-sol.txt', header=None, delimiter=';', na_values='-99')
Vchi_cruda = pd.read_csv('/home/emi/Documents/MJO/datos/series viento-sol/chi-sol.txt', header=None, delimiter=';', na_values='-99')


# ~ Vmad = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/WH.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, RMM1, RMM2, phase, amplitude
Vmad = pd.read_csv('/home/emi/Documents/MJO/datos/mjo/filtered.txt', header=None, delimiter=',', na_values='-99') ### year, month, day, day of week, RMM1, RMM2, phase, amplitude

# lag 0
series0 = pd.DataFrame()
# cargamos mes, para despues filtrar por estacion
series0[0] = Vmad[1]
# cargamos fase
series0[1] = Vmad[6]
# cargamos dia de la semana, para cuando trabajemos con demanda
series0[2] = Vmad[3]
#  cargamos amplitud, para quedarnos con MJO activas
series0[3] = Vmad[7]
# series uruguay argentina chile
series0[4] = Vuru[1]
series0[5] = Varg[1]
series0[6] = Vchi[1]
# ~ print(series0)

# Build lag series (lag 0 to lag 10)
remove_last_cols  = [0, 1, 2, 3]
remove_first_cols = [4, 5, 6]
all_lags = [series0]
for lag in range(1, 11):
    part1 = series0[remove_last_cols].iloc[:-lag].reset_index(drop=True)
    part2 = series0[remove_first_cols].iloc[lag:].reset_index(drop=True)
    all_lags.append(pd.concat([part1, part2], axis=1))

# Keep only active MJO events (amplitude > 1)
all_lags = [s.loc[s[3] > 1] for s in all_lags]

## calculamos los promedios estacionales de las series crudas. Esto sirve para sacar los porcentajes

Vuru_c_ver = Vuru_cruda.loc[(Vuru_cruda[1] == 1) | (Vuru_cruda[1] == 2) | (Vuru_cruda[1] == 12)]
Vuru_c_oto = Vuru_cruda.loc[(Vuru_cruda[1] == 3) | (Vuru_cruda[1] == 4) | (Vuru_cruda[1] == 5)]
Vuru_c_inv = Vuru_cruda.loc[(Vuru_cruda[1] == 6) | (Vuru_cruda[1] == 7) | (Vuru_cruda[1] == 8)]
Vuru_c_pri = Vuru_cruda.loc[(Vuru_cruda[1] == 9) | (Vuru_cruda[1] == 10) |(Vuru_cruda[1] == 11)]

Vuru_p_v = 100/Vuru_c_ver[3].mean()
Vuru_p_o = 100/Vuru_c_oto[3].mean()
Vuru_p_i = 100/Vuru_c_inv[3].mean()
Vuru_p_p = 100/Vuru_c_pri[3].mean()

Vchi_c_ver = Vchi_cruda.loc[(Vchi_cruda[1] == 1) | (Vchi_cruda[1] == 2) | (Vchi_cruda[1] == 12)]
Vchi_c_oto = Vchi_cruda.loc[(Vchi_cruda[1] == 3) | (Vchi_cruda[1] == 4) | (Vchi_cruda[1] == 5)]
Vchi_c_inv = Vchi_cruda.loc[(Vchi_cruda[1] == 6) | (Vchi_cruda[1] == 7) | (Vchi_cruda[1] == 8)]
Vchi_c_pri = Vchi_cruda.loc[(Vchi_cruda[1] == 9) | (Vchi_cruda[1] == 10) | (Vchi_cruda[1] == 11)]

Vchi_p_v = 100/Vchi_c_ver[3].mean()
Vchi_p_o = 100/Vchi_c_oto[3].mean()
Vchi_p_i = 100/Vchi_c_inv[3].mean()
Vchi_p_p = 100/Vchi_c_pri[3].mean()

Varg_c_ver = Varg_cruda.loc[(Varg_cruda[1] == 1) | (Varg_cruda[1] == 2) | (Varg_cruda[1] == 12)]
Varg_c_oto = Varg_cruda.loc[(Varg_cruda[1] == 3) | (Varg_cruda[1] == 4) | (Varg_cruda[1] == 5)]
Varg_c_inv = Varg_cruda.loc[(Varg_cruda[1] == 6) | (Varg_cruda[1] == 7) | (Varg_cruda[1] == 8)]
Varg_c_pri = Varg_cruda.loc[(Varg_cruda[1] == 9) | (Varg_cruda[1] == 10) | (Varg_cruda[1] == 11)]

Varg_p_v = 100/Varg_c_ver[3].mean()
Varg_p_o = 100/Varg_c_oto[3].mean()
Varg_p_i = 100/Varg_c_inv[3].mean()
Varg_p_p = 100/Varg_c_pri[3].mean()

#### seasonal means and p-values per phase and lag

def mwu_pval(group, rest):
    group, rest = group.dropna(), rest.dropna()
    if len(group) < 3 or len(rest) < 3:
        return 1.0
    _, p = mannwhitneyu(group, rest, alternative='two-sided')
    return p

season_defs = {
    'ver': {'months': [1, 2, 12], 'pf': {'uru': Vuru_p_v, 'arg': Varg_p_v, 'chi': Vchi_p_v}},
    'oto': {'months': [3, 4, 5],  'pf': {'uru': Vuru_p_o, 'arg': Varg_p_o, 'chi': Vchi_p_o}},
    'inv': {'months': [6, 7, 8],  'pf': {'uru': Vuru_p_i, 'arg': Varg_p_i, 'chi': Vchi_p_i}},
    'pri': {'months': [9, 10, 11],'pf': {'uru': Vuru_p_p, 'arg': Varg_p_p, 'chi': Vchi_p_p}},
}
country_cols = {'uru': 4, 'arg': 5, 'chi': 6}

means_store = {c: {s: [] for s in season_defs} for c in country_cols}
pvals_store = {c: {s: [] for s in season_defs} for c in country_cols}

for series in all_lags:
    for sname, sinfo in season_defs.items():
        season_df = series.loc[series[0].isin(sinfo['months'])]
        for cname, col in country_cols.items():
            pf = sinfo['pf'][cname]
            means_row, pvals_row = [], []
            for ph in range(1, 9):
                group = season_df.loc[season_df[1] == ph, col].dropna()
                rest  = season_df.loc[season_df[1] != ph, col].dropna()
                means_row.append(group.mean() * pf)
                pvals_row.append(mwu_pval(group, rest))
            means_store[cname][sname].append(means_row)
            pvals_store[cname][sname].append(pvals_row)

lag_cols = ['lag10', 'lag9', 'lag8', 'lag7', 'lag6', 'lag5', 'lag4', 'lag3', 'lag2', 'lag1', 'lag0']

def make_df(store, country, season):
    return pd.DataFrame({f'lag{i}': store[country][season][i] for i in range(11)})[lag_cols]

Vargver = make_df(means_store, 'arg', 'ver')
Vargoto = make_df(means_store, 'arg', 'oto')
Varginv = make_df(means_store, 'arg', 'inv')
Vargpri = make_df(means_store, 'arg', 'pri')
Vuruver = make_df(means_store, 'uru', 'ver')
Vuruoto = make_df(means_store, 'uru', 'oto')
Vuruinv = make_df(means_store, 'uru', 'inv')
Vurupri = make_df(means_store, 'uru', 'pri')
Vchiver = make_df(means_store, 'chi', 'ver')
Vchioto = make_df(means_store, 'chi', 'oto')
Vchiinv = make_df(means_store, 'chi', 'inv')
Vchipri = make_df(means_store, 'chi', 'pri')

Pargver = make_df(pvals_store, 'arg', 'ver')
Pargoto = make_df(pvals_store, 'arg', 'oto')
Parginv = make_df(pvals_store, 'arg', 'inv')
Pargpri = make_df(pvals_store, 'arg', 'pri')
Puruver = make_df(pvals_store, 'uru', 'ver')
Puruoto = make_df(pvals_store, 'uru', 'oto')
Puruinv = make_df(pvals_store, 'uru', 'inv')
Purupri = make_df(pvals_store, 'uru', 'pri')
Pchiver = make_df(pvals_store, 'chi', 'ver')
Pchioto = make_df(pvals_store, 'chi', 'oto')
Pchiinv = make_df(pvals_store, 'chi', 'inv')
Pchipri = make_df(pvals_store, 'chi', 'pri')

vmin = min(Vargver.min().min(), Vargoto.min().min(), Varginv.min().min(), Vargpri.min().min(),Vuruver.min().min(), Vuruoto.min().min(), Vuruinv.min().min(), Vurupri.min().min(),Vchiver.min().min(), Vchioto.min().min(), Vchiinv.min().min(), Vchipri.min().min())
vmax = max(Vargver.max().max(), Vargoto.max().max(), Varginv.max().max(), Vargpri.max().max(),Vuruver.max().max(), Vuruoto.max().max(), Vuruinv.max().max(), Vurupri.max().max(),Vchiver.max().max(), Vchioto.max().max(), Vchiinv.max().max(), Vchipri.max().max())

print(vmin)
print(vmax)

colors = ["dimgrey", "white", "darkorange"]

# 2. Create the custom colormap object
# 'BlueToGreenDiverging' is a name for your custom colormap
custom_cmap = LinearSegmentedColormap.from_list("BlueToGreenDiverging", colors)
# ~ figax = plt.subplots(nrows=1,ncols=1,figsize=(5,2.5), sharey=True)
fig, ((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12)) = plt.subplots(4, 3,figsize=(7,5), sharex= True, sharey=True)

# ~ annot_matrix = N.where(Vargver > 5  , '*', '')
annot_matrix = N.where(Pargver < 0.05, '*', '')
ax1.set_title('Argentina  ', fontsize=13)
sns.heatmap(Vargver,cmap=custom_cmap, ax=ax1, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center'})
ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0)
ax1.xaxis.set_tick_params(length=0)

annot_matrix = N.where(Pargoto < 0.05, '*', '')
sns.heatmap(Vargoto, cmap=custom_cmap, ax=ax4,yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False)
ax4.set_yticklabels(ax4.get_yticklabels(), rotation=0)
ax4.xaxis.set_tick_params(length=0)

annot_matrix = N.where(Parginv < 0.05, '*', '')
sns.heatmap(Varginv,cmap=custom_cmap, ax=ax7, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax7.set_yticklabels(ax7.get_yticklabels(), rotation=0)
ax7.xaxis.set_tick_params(length=0)

annot_matrix = N.where(Pargpri < 0.05, '*', '')
sns.heatmap(Vargpri, cmap=custom_cmap, ax=ax10, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax10.set_yticklabels(ax10.get_yticklabels(), rotation=0)

ax2.set_title('Uruguay', fontsize=13)
annot_matrix = N.where(Puruver < 0.05, '*', '')
sns.heatmap(Vuruver, cmap=custom_cmap, ax=ax2, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax2.xaxis.set_tick_params(length=0)
ax2.yaxis.set_tick_params(length=0)

annot_matrix = N.where(Puruoto < 0.05, '*', '')
sns.heatmap(Vuruoto,cmap=custom_cmap, ax=ax5,yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax5.xaxis.set_tick_params(length=0)
ax5.yaxis.set_tick_params(length=0)

annot_matrix = N.where(Puruinv < 0.05, '*', '')
sns.heatmap(Vuruinv, cmap=custom_cmap, ax=ax8, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax8.xaxis.set_tick_params(length=0)
ax8.yaxis.set_tick_params(length=0)

annot_matrix = N.where(Purupri < 0.05, '*', '')
sns.heatmap(Vurupri, cmap=custom_cmap, ax=ax11, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax11.yaxis.set_tick_params(length=0)

ax3.set_title('Chile', fontsize=13)
annot_matrix = N.where(Pchiver < 0.05, '*', '')
sns.heatmap(Vchiver, cmap=custom_cmap, ax=ax3, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax3.xaxis.set_tick_params(length=0)
ax3.yaxis.set_tick_params(length=0)

annot_matrix = N.where(Pchioto < 0.05, '*', '')
sns.heatmap(Vchioto, cmap=custom_cmap, ax=ax6,yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax6.xaxis.set_tick_params(length=0)
ax6.yaxis.set_tick_params(length=0)

annot_matrix = N.where(Pchiinv < 0.05, '*', '')
sns.heatmap(Vchiinv, cmap=custom_cmap, ax=ax9, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax9.xaxis.set_tick_params(length=0)
ax9.yaxis.set_tick_params(length=0)

annot_matrix = N.where(Pchipri < 0.05, '*', '')
sns.heatmap(Vchipri, cmap=custom_cmap, ax=ax12, yticklabels=['1', '2', '3', '4', '5', '6', '7', '8'], vmin =-14, vmax=14,cbar=False, annot=annot_matrix, fmt='', annot_kws={'size': 12, 'color': 'black','va': 'center_baseline'})
ax12.yaxis.set_tick_params(length=0)

cbar_ax = fig.add_axes([0.90, 0.15, 0.02, 0.7])
norm = plt.Normalize(vmin=-10.5, vmax=10.5)
sm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm)
cbar= fig.colorbar(sm, ax=(ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10,ax11,ax12), location='right', shrink=0.8, cax=cbar_ax)
cbar.set_label('variation [%]', fontsize=14)

fig.subplots_adjust(wspace=0.1, hspace=0.1)
fig.text(0.86, 0.77, 'DJF', fontsize = 14, rotation='vertical')
fig.text(0.86, 0.57, 'MAM', fontsize = 14, rotation='vertical')
fig.text(0.86, 0.39, 'JJA', fontsize = 14, rotation='vertical')
fig.text(0.86, 0.19, 'SON', fontsize = 14, rotation='vertical')
fig.text(0.05, 0.42, 'MJO phase', fontsize=14, rotation='vertical')
fig.subplots_adjust(right=0.85)

plt.savefig('/home/emi/Dropbox/DTEC/MJO/imagenes/heatplotS.png',bbox_inches="tight", dpi=600)
