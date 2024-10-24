from griffis_soccer_analysis.fbref_code import *
import pandas as pd
from scipy import stats
import math
from math import pi
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


df = pd.read_csv('../Final FBRef Next 12 Leagues.csv')
df.head()

df.Pos.value_counts()
df.Min.describe()
mediocampistas = df[(df['Pos'].str.contains('MF') == True) &  (df['Min'] > 840 )].reset_index(drop=True)
list(df.columns)

lista_valores = [
    'Player',
    'Squad',
    'TklPer90',
    'TklWinPossPer90',
    'Mid3rdTklPer90',
    'Def3rdTklPer90',
    'Att3rdTklPer90',
    'DrbTklPer90',
    'DrbPastAttPer90',
    'DrbTkl%Per90',
    'DrbPastPer90',
    'BlocksPer90',
    'ShBlocksPer90',
    'PassBlocksPer90',
    'IntPer90',
    'Tkl+IntPer90',
    'ClrPer90',
    'ErrPer90',
    'RecovPer90',
    'pAdjShBlocksPer90',
    'pAdjPassBlocksPer90',
    'pAdjIntPer90',
    'pAdjDrbTklPer90',
    'pAdjTklWinPossPer90',
    'pAdjDrbPastPer90',
    'pAdjAerialWinsPer90',
    'pAdjAerialLossPer90',
]

# Grupo 1 de columnas para el primer total
grupo_1 = [
    'TklPer90',
    'TklWinPossPer90',
    'Def3rdTklPer90',
    'Mid3rdTklPer90',
    'Att3rdTklPer90',
    'DrbTklPer90',
    'DrbPastAttPer90',
    'DrbTkl%Per90',
    'DrbPastPer90',
    'BlocksPer90',
    'ShBlocksPer90',
    'PassBlocksPer90',
    'IntPer90',
    'Tkl+IntPer90',
    'ClrPer90',
    'ErrPer90',
    'RecovPer90'
]

# Grupo 2 de columnas para el segundo total
grupo_2 = [
    'pAdjShBlocksPer90',
    'pAdjPassBlocksPer90',
    'pAdjIntPer90',
    'pAdjDrbTklPer90',
    'pAdjTklWinPossPer90',
    'pAdjDrbPastPer90',
    'pAdjAerialWinsPer90',
    'pAdjAerialLossPer90'
]

mediocampistas[lista_valores].reset_index(drop=True)

mediosdef = mediocampistas[lista_valores].reset_index(drop=True).fillna(0)
jugadores = list(mediosdef.Player.unique())

# DataFrame para grupo 1
df_grupo_1 = pd.DataFrame(columns=['Nombre', 'Equipo'] + grupo_1)

# DataFrame para grupo 2
df_grupo_2 = pd.DataFrame(columns=['Nombre', 'Equipo'] + grupo_2)

for jugador in jugadores:
    player = mediosdef.loc[mediosdef['Player'] == jugador].reset_index()
    equipo = player.loc[0, 'Squad']  # Obtener el nombre del equipo

    # Calcular percentiles para el grupo 1
    player_values_grupo_1 = player.loc[0, grupo_1].values  # Obtener los valores de los parámetros del grupo 1
    percentiles_grupo_1 = []
    for x in range(len(grupo_1)):
        percentile = math.floor(stats.percentileofscore(mediosdef[grupo_1[x]], player_values_grupo_1[x]))
        percentiles_grupo_1.append(percentile)
    diccionario_grupo_1 = {'Nombre': jugador, 'Equipo': equipo}
    diccionario_grupo_1.update({grupo_1[i]: percentiles_grupo_1[i] for i in range(len(grupo_1))})
    df1 = pd.DataFrame([diccionario_grupo_1])
    df_grupo_1 = pd.concat([df_grupo_1, df1], ignore_index=True)

    # Calcular percentiles para el grupo 2
    player_values_grupo_2 = player.loc[0, grupo_2].values  # Obtener los valores de los parámetros del grupo 2
    percentiles_grupo_2 = []
    for x in range(len(grupo_2)):
        percentile = math.floor(stats.percentileofscore(mediosdef[grupo_2[x]], player_values_grupo_2[x]))
        percentiles_grupo_2.append(percentile)
    diccionario_grupo_2 = {'Nombre': jugador, 'Equipo': equipo}
    diccionario_grupo_2.update({grupo_2[i]: percentiles_grupo_2[i] for i in range(len(grupo_2))})
    df2 = pd.DataFrame([diccionario_grupo_2])
    df_grupo_2 = pd.concat([df_grupo_2, df2], ignore_index=True)

# Cálculo de las puntuaciones totales
df_grupo_1['Puntuacion_Total_Grupo_1'] = df_grupo_1[grupo_1].sum(axis=1)
df_grupo_2['Puntuacion_Total_Grupo_2'] = df_grupo_2[grupo_2].sum(axis=1)

# Ordenar los DataFrames basados en las puntuaciones totales
df_grupo_1 = df_grupo_1.sort_values(by='Puntuacion_Total_Grupo_1', ascending=False).reset_index(drop=True)
df_grupo_2 = df_grupo_2.sort_values(by='Puntuacion_Total_Grupo_2', ascending=False).reset_index(drop=True)

enzoperez_grupo_1 = df_grupo_1[df_grupo_1['Nombre'] == 'Enzo Pérez']
enzoperez_grupo_2 = df_grupo_2[df_grupo_2['Nombre'] == 'Enzo Pérez']

def crear_radar_modificado(df, grupo, nombre_grupo):
    categorias = grupo
    N = len(categorias)
    etiquetas_personalizadas = [f'{i+1}º' for i in range(N)]

    valores = df[categorias].values.flatten().tolist()
    valores += valores[:1]

    # Calcula los ángulos de los ejes del radar
    angulos = [n / float(N) * 2 * np.pi for n in range(N)]
    angulos += angulos[:1]

    # Inicializa el gráfico de radar
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12), subplot_kw=dict(polar=True))

    # Dibuja los ejes con las etiquetas en el primer eje
    ax1.plot(angulos, valores, linewidth=1, linestyle='solid')
    ax1.fill(angulos, valores, 'b', alpha=0.2)
    ax1.set_xticks(angulos[:-1])
    ax1.set_xticklabels(etiquetas_personalizadas)
    ax1.set_title(f'Gráfico de Radar - {nombre_grupo}')


    ax2.axis('off')

    half = (N + 1) // 2
    for i, categoria in enumerate(categorias):
        col = 0.1 if i < half else 0.5
        row = 0.95 - (i % half) * 0.1
        ax2.text(col, row, f'{i+1}: {categoria}', transform=ax2.transAxes, fontsize=10)

    plt.show()


crear_radar_modificado(enzoperez_grupo_1, grupo_1, 'Grupo 1')

