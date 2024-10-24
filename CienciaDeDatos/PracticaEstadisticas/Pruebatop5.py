import streamlit as st
import pandas as pd
import numpy as np
import math
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import ConnectionPatch

# Lectura del DataFrame
df = pd.read_csv('../Final FBRef 2023-2024.csv')

# Definir las ligas disponibles
ligas_disponibles = ['Premier League', 'La Liga', 'Serie A', 'Fußball-Bundesliga', 'Ligue 1']

# Interfaz de Streamlit con sidebar
st.sidebar.markdown("<h1 style='text-align: center; font-size: 36px;'>Análisis de Mediocampistas</h1>", unsafe_allow_html=True)

# Selección de la liga en el sidebar
liga_seleccionada = st.sidebar.selectbox('Selecciona la liga', ligas_disponibles)

# Filtrar los datos según la liga seleccionada
mediocampistas = df[(df['Pos'].str.contains('MF') == True) & (df['Min'] > 840) & (df['Comp'] == liga_seleccionada)].reset_index(drop=True)

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

def calcular_area_poligono(x, y):
    """Función para calcular el área de un polígono."""
    # Calcular el producto cruzado entre los puntos
    cross_product = np.cross(x, np.roll(y, 1)) - np.cross(y, np.roll(x, 1))
    # Calcular el área como la mitad del módulo del producto cruzado
    area = 0.5 * np.abs(cross_product.sum())
    return area

def crear_radar_modificado(df, grupo, nombre_grupo, jugadores):
    """
    Crea un gráfico de radar modificado con múltiples ejes y animación.
    """
    # Número de categorías en el grupo
    N = len(grupo)
    
    # Etiquetas para las categorías
    etiquetas_personalizadas = [f'{i+1}º' for i in range(N)]

    # Obtener los valores de los jugadores seleccionados
    valores_jugadores = df[grupo].values
    
    # Crear una figura y ejes para el gráfico de radar
    fig, (axl, axr) = plt.subplots(ncols=2, figsize=(12, 6), subplot_kw=dict(polar=True))
    
    # Configuración del gráfico para el lado izquierdo (polígono)
    axl.set_aspect(1)
    axl.set_theta_offset(np.pi / 2)
    axl.set_theta_direction(-1)
    axl.set_xticks(np.linspace(0, 2*np.pi, N, endpoint=False))
    axl.set_xticklabels(etiquetas_personalizadas)
    
    # Configuración del gráfico para el lado derecho (línea)
    axr.set_aspect(1)
    axr.yaxis.set_visible(False)
    axr.xaxis.set_ticks([0, np.pi, 2 * np.pi], ["0", r"$\pi$", r"$2\pi$"])

    max_area = 0
    
    # Inicializar una lista para almacenar las áreas de los polígonos
    areas_poligonos = []
    
    # Crear polígono para cada jugador
    for jugador, valores in zip(jugadores, valores_jugadores):
        # Calcular los ángulos para cada categoría
        angulos = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        
        # Calcular el área del polígono para el jugador actual
        area_poligono = calcular_area_poligono(np.cos(angulos), np.sin(angulos))
        areas_poligonos.append(area_poligono)
        
        # Dibujar el polígono en el lado izquierdo
        axl.plot(angulos, valores, "o-", linewidth=2, label=jugador)
    
    # Calcular el máximo área para normalizar los valores
    max_area = max(areas_poligonos)
    
    # Crear una animación para mostrar la evolución de las líneas en el lado derecho
    def animate(i):
        # Calcular el factor de escala para normalizar las áreas
        scale_factor = areas_poligonos[i] / max_area
        
        # Calcular los ángulos y valores normalizados para el jugador actual
        angulos = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        valores = valores_jugadores[i] * scale_factor
        
        # Actualizar los datos de la línea en el lado derecho
        sine.set_data(angulos, valores)
        return sine,
    
    # Inicializar la línea en el lado derecho
    x = np.linspace(0, 2 * np.pi, 50)
    sine, = axr.plot(x, np.sin(x))
    
    # Crear la animación
    ani = animation.FuncAnimation(fig, animate, frames=len(jugadores), interval=100, repeat=False)
    
    # Ajustar el diseño de la figura y mostrarla
    plt.tight_layout()
    plt.show()
    # Número de categorías en el grupo
    N = len(grupo)
    
    # Etiquetas para las categorías
    etiquetas_personalizadas = [f'{i+1}º' for i in range(N)]

    # Obtener los valores de los jugadores seleccionados
    valores_jugadores = df[grupo].values
    
    # Crear una figura y ejes para el gráfico de radar
    fig, (axl, axr) = plt.subplots(ncols=2, figsize=(12, 6), subplot_kw=dict(polar=True))
    
    # Configuración del gráfico para el lado izquierdo (polígono)
    axl.set_aspect(1)
    axl.set_theta_offset(np.pi / 2)
    axl.set_theta_direction(-1)
    axl.set_xticks(np.linspace(0, 2*np.pi, N, endpoint=False))
    axl.set_xticklabels(etiquetas_personalizadas)
    
    # Configuración del gráfico para el lado derecho (línea)
    axr.set_aspect(1)
    axr.yaxis.set_visible(False)
    axr.xaxis.set_ticks([0, np.pi, 2 * np.pi], ["0", r"$\pi$", r"$2\pi$"])

    max_area = 0
    
    # Inicializar una lista para almacenar las áreas de los polígonos
    areas_poligonos = []
    
    # Crear polígono para cada jugador
    for jugador, valores in zip(jugadores, valores_jugadores):
        # Calcular los ángulos para cada categoría
        angulos = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        
        # Calcular el área del polígono para el jugador actual
        area_poligono = calcular_area_poligono(angulos, valores)
        areas_poligonos.append(area_poligono)
        
        # Dibujar el polígono en el lado izquierdo
        axl.plot(angulos, valores, "o-", linewidth=2, label=jugador)
    
    # Calcular el máximo área para normalizar los valores
    max_area = max(areas_poligonos)
    
    # Crear una animación para mostrar la evolución de las líneas en el lado derecho
    def animate(i):
        # Calcular el factor de escala para normalizar las áreas
        scale_factor = areas_poligonos[i] / max_area
        
        # Calcular los ángulos y valores normalizados para el jugador actual
        angulos = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        valores = valores_jugadores[i] * scale_factor
        
        # Actualizar los datos de la línea en el lado derecho
        sine.set_data(angulos, valores)
        return sine,
    
    # Inicializar la línea en el lado derecho
    x = np.linspace(0, 2 * np.pi, 50)
    sine, = axr.plot(x, np.sin(x))
    
    # Crear la animación
    ani = animation.FuncAnimation(fig, animate, frames=len(jugadores), interval=100, repeat=False)
    
    # Ajustar el diseño de la figura y mostrarla
    plt.tight_layout()
    plt.show()

# Llamada a la función para crear el gráfico de radar modificado
crear_radar_modificado(df_grupo_1, grupo_1, 'Grupo 1', jugadores)