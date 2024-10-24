import numpy as np
import pandas as pd
from scipy import stats
import math
from math import pi
import matplotlib.pyplot as plt
import streamlit as st

# Lectura del DataFrame
df = pd.read_csv('../Final FBRef 2023-2024.csv')

# Definir las ligas disponibles
ligas_disponibles = ['Premier League', 'La Liga', 'Serie A', 'Bundesliga', 'Ligue 1']

# Interfaz de Streamlit con sidebar
st.sidebar.markdown("<h1 style='text-align: center; font-size: 36px;'>Estadísticas\n Ligas Europeas</h1>", unsafe_allow_html=True)

# Selección de la liga en el sidebar
liga_seleccionada = st.sidebar.selectbox('Selecciona la liga', ligas_disponibles)

# Filtrar los datos según la liga seleccionada
mediocampistas = df[(df['Pos'].str.contains('GK') != True) & (df['Min'] > 1400) & (df['Comp'].str.contains(liga_seleccionada) == True) & (df['Starts'] > 10)].reset_index(drop=True)

lista_valores = [
    'Player','Squad','Shots', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'AvgShotDistance', 'FKShots', 'PK', 'PKsAtt',
    'PassesCompleted', 'PassesAttempted', 'TotCmp%', 'TotalPassDist', 'ProgPassDist', 'ShortPassCmp', 'ShortPassAtt', 'ShortPassCmp%',
    'MedPassCmp', 'MedPassAtt', 'MedPassCmp%', 'LongPassCmp', 'LongPassAtt', 'LongPassCmp%', 'Assists', 'xAG', 'xA', 'A-xAG', 'KeyPasses',
    'Final1/3Cmp', 'PenAreaCmp', 'CrsPenAreaCmp', 'ProgPasses', 'LivePass', 'DeadPass', 'FKPasses', 'ThruBalls', 'Switches', 'Crs',
    'ThrowIn', 'CK', 'InSwingCK', 'OutSwingCK', 'StrCK', 'Cmpxxx', 'PassesToOff', 'PassesBlocked', 'SCA', 'SCA90', 'SCAPassLive', 'SCAPassDead',
    'SCADrib', 'SCASh', 'SCAFld', 'SCADef', 'GCA', 'GCA90', 'GCAPassLive', 'GCAPassDead', 'GCADrib', 'GCASh', 'GCAFld', 'GCADef', 'Tkl',
    'TklWinPoss', 'Def3rdTkl', 'Mid3rdTkl', 'Att3rdTkl', 'DrbTkl', 'DrbPastAtt', 'DrbTkl%', 'DrbPast', 'Blocks', 'ShBlocks', 'PassBlocks',
    'Int', 'Tkl+Int', 'Clr', 'Err', 'Fls', 'Recov', 'AerialWins', 'AerialLoss', 'AerialWin%', 'Touches', 'DefPenTouch', 'Def3rdTouch',
    'Mid3rdTouch', 'Att3rdTouch', 'AttPenTouch', 'LiveTouch', 'AttDrb', 'SuccDrb', 'DrbSucc%', 'TimesTackled', 'TimesTackled%', 'Carries',
    'TotalCarryDistance', 'ProgCarryDistance', 'ProgCarries', 'CarriesToFinalThird', 'CarriesToPenArea', 'CarryMistakes', 'Disposesed',
    'ReceivedPass', 'ProgPassesRec'
]

# Grupos de estadísticas
grupo_shots = [
    'Shots', 'SoT', 'SoT%', 'Sh/90', 'SoT/90', 'G/Sh', 'G/SoT', 'AvgShotDistance', 'FKShots', 'PK', 'PKsAtt'
]

grupo_pases = [
    'PassesCompleted', 'PassesAttempted', 'TotCmp%', 'TotalPassDist', 'ProgPassDist', 'ShortPassCmp', 'ShortPassAtt',
    'ShortPassCmp%', 'MedPassCmp', 'MedPassAtt', 'MedPassCmp%', 'LongPassCmp', 'LongPassAtt', 'LongPassCmp%', 'Assists',
    'xAG', 'xA', 'A-xAG', 'KeyPasses', 'Final1/3Cmp', 'PenAreaCmp', 'CrsPenAreaCmp', 'ProgPasses'
]

grupo_tipos_de_pases = [
    'LivePass', 'DeadPass', 'FKPasses', 'ThruBalls', 'Switches', 'Crs', 'ThrowIn', 'CK', 'InSwingCK', 'OutSwingCK',
    'StrCK', 'Cmpxxx', 'PassesToOff', 'PassesBlocked'
]

grupo_creacion_de_goles_tiros = [
    'SCA', 'SCA90', 'SCAPassLive', 'SCAPassDead', 'SCADrib', 'SCASh', 'SCAFld', 'SCADef', 'GCA', 'GCA90', 'GCAPassLive',
    'GCAPassDead', 'GCADrib', 'GCASh', 'GCAFld', 'GCADef'
]

grupo_acciones_defensivas = [
    'Tkl', 'TklWinPoss', 'Def3rdTkl', 'Mid3rdTkl', 'Att3rdTkl', 'DrbTkl', 'DrbPastAtt', 'DrbTkl%', 'DrbPast', 'Blocks',
    'ShBlocks', 'PassBlocks', 'Int', 'Tkl+Int', 'Clr', 'Err'
]

grupo_rendimiento = [
    'Fls', 'Recov', 'AerialWins', 'AerialLoss', 'AerialWin%'
]

grupo_posesion = [
    'Touches', 'DefPenTouch', 'Def3rdTouch', 'Mid3rdTouch', 'Att3rdTouch', 'AttPenTouch', 'LiveTouch', 'AttDrb',
    'SuccDrb', 'DrbSucc%', 'TimesTackled', 'TimesTackled%', 'Carries', 'TotalCarryDistance', 'ProgCarryDistance',
    'ProgCarries', 'CarriesToFinalThird', 'CarriesToPenArea', 'CarryMistakes', 'Disposesed', 'ReceivedPass',
    'ProgPassesRec'
]

grupos = {
    'Shots': grupo_shots,
    'Pases': grupo_pases,
    'Tipos de Pases': grupo_tipos_de_pases,
    'Creación de Goles/Tiros': grupo_creacion_de_goles_tiros,
    'Acciones Defensivas': grupo_acciones_defensivas,
    'Rendimiento': grupo_rendimiento,
    'Posesión': grupo_posesion
}

mediosdef = mediocampistas[lista_valores].reset_index(drop=True).fillna(0)
jugadores = list(mediosdef.Player.unique())

# Crear DataFrames para cada grupo
dfs_grupos = {}
for nombre_grupo, grupo in grupos.items():
    dfs_grupos[nombre_grupo] = pd.DataFrame(columns=['Nombre', 'Equipo'] + grupo)

for jugador in jugadores:
    player = mediosdef.loc[mediosdef['Player'] == jugador].reset_index()
    equipo = player.loc[0, 'Squad']  # Obtener el nombre del equipo

    for nombre_grupo, grupo in grupos.items():
        player_values = player.loc[0, grupo].values  # Obtener los valores de los parámetros del grupo
        percentiles = [math.floor(stats.percentileofscore(mediosdef[stat], value)) for stat, value in zip(grupo, player_values)]
        diccionario = {'Nombre': jugador, 'Equipo': equipo}
        diccionario.update({grupo[i]: percentiles[i] for i in range(len(grupo))})
        df_temp = pd.DataFrame([diccionario])
        dfs_grupos[nombre_grupo] = pd.concat([dfs_grupos[nombre_grupo], df_temp], ignore_index=True)

# Cálculo de las puntuaciones totales
for nombre_grupo, df in dfs_grupos.items():
    df[f'Puntuacion_Total_{nombre_grupo}'] = df[grupos[nombre_grupo]].sum(axis=1)
    dfs_grupos[nombre_grupo] = df.sort_values(by=f'Puntuacion_Total_{nombre_grupo}', ascending=False).reset_index(drop=True)

def calcular_area_poligono(angulos, valores):
    # Convertir los ángulos y valores a coordenadas cartesianas
    x = [v * np.cos(a) for a, v in zip(angulos, valores)]
    y = [v * np.sin(a) for a, v in zip(angulos, valores)]

    # Aplicar la fórmula de Shoelace para calcular el área del polígono
    area = 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    return area

# Función para crear el gráfico de radar
def crear_radar_modificado(df1, df2, grupo, nombre_grupo, jugador1, jugador2):
    categorias = grupo
    N = len(categorias)
    

    # Obtener el apellido del primer jugador
    apellido_jugador1 = jugador1.split()[1] if len(jugador1.split()) > 1 else jugador1
    
    # Obtener el apellido del segundo jugador
    apellido_jugador2 = jugador2.split()[1] if len(jugador2.split()) > 1 else jugador2

    # Valores del primer jugador
    valores1 = df1[grupo].values.flatten().tolist()
    valores1 += valores1[:1]
    
    # Valores del segundo jugador
    valores2 = df2[grupo].values.flatten().tolist()
    valores2 += valores2[:1]
    
    # Calcular los ángulos de los ejes del radar
    angulos = [n / float(N) * 2 * np.pi for n in range(N)]
    angulos += angulos[:1]

    # Inicializa el gráfico de radar
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(polar=True))

    # Dibuja los ejes con las etiquetas
    ax.plot(angulos, valores1, linewidth=1, linestyle='solid', label=f"{apellido_jugador1}")
    ax.fill(angulos, valores1, 'b', alpha=0.2)

    ax.plot(angulos, valores2, linewidth=1, linestyle='solid', label=f"{apellido_jugador2}", color='r')
    ax.fill(angulos, valores2, 'r', alpha=0.2)
    
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias)
    ax.set_title(f'Gráfico de Radar - {nombre_grupo}')
    
    # Calcular el área del polígono para cada jugador
    area_poligono1 = calcular_area_poligono(angulos, valores1)
    area_poligono2 = calcular_area_poligono(angulos, valores2)
    
    # Añadir la leyenda
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    
    
    
    # Retornar la figura y el área del polígono para ambos jugadores
    return fig, area_poligono1, area_poligono2




# Selección del grupo estadístico
grupo_seleccionado = st.sidebar.selectbox('Selecciona el grupo estadístico', list(grupos.keys()))

# Filtrado de jugadores por equipo
equipos_disponibles = sorted(mediocampistas['Squad'].unique())
equipo_seleccionado1 = st.sidebar.selectbox('Selecciona el equipo del Jugador 1', equipos_disponibles)
jugadores_equipo1 = sorted(mediocampistas[mediocampistas['Squad'] == equipo_seleccionado1]['Player'].unique())
jugador1 = st.sidebar.selectbox('Selecciona el Jugador 1', jugadores_equipo1)

equipo_seleccionado2 = st.sidebar.selectbox('Selecciona el equipo del Jugador 2', equipos_disponibles)
jugadores_equipo2 = sorted(mediocampistas[mediocampistas['Squad'] == equipo_seleccionado2]['Player'].unique())
jugador2 = st.sidebar.selectbox('Selecciona el Jugador 2', jugadores_equipo2)

# Obtener los datos del jugador 1 y 2
df_jugador1 = dfs_grupos[grupo_seleccionado][dfs_grupos[grupo_seleccionado]['Nombre'] == jugador1]
df_jugador2 = dfs_grupos[grupo_seleccionado][dfs_grupos[grupo_seleccionado]['Nombre'] == jugador2]

# Crear el gráfico de radar comparativo para los jugadores seleccionados
fig, area_poligono1, area_poligono2  = crear_radar_modificado(df_jugador1, df_jugador2, grupos[grupo_seleccionado], grupo_seleccionado, jugador1, jugador2)

# CSS personalizado para centrar el texto y aumentar el tamaño de la fuente
st.markdown("""
    <style>
    .center-text {
        text-align: center;
    }
    .dataframe tbody td {
        text-align: center;
        font-size: 16px; /* Aumenta el tamaño de la fuente en las celdas del cuerpo de la tabla */
    }
    .dataframe thead th {
        text-align: center;
        font-size: 18px; /* Aumenta el tamaño de la fuente en las celdas de la cabecera de la tabla */
    }
    </style>
""", unsafe_allow_html=True)

# Mostrar el gráfico
st.pyplot(fig)



st.write(f"<div class='center-text' style='font-size: 25px;' >Área del polígono de {jugador1}: {area_poligono1:.2f}</div>", unsafe_allow_html=True)
st.write(f"<div class='center-text'>(Posición {df_jugador1.index[0] + 1}º)</div>", unsafe_allow_html=True)

st.write(f"<div class='center-text' style='font-size: 25px;' >Área del polígono de {jugador2}: {area_poligono2:.2f}</div>", unsafe_allow_html=True)
st.write(f"<div class='center-text'>(Posición {df_jugador2.index[0] + 1}º)</div>", unsafe_allow_html=True)


#
if jugador1 == jugador2:
    st.warning("Por favor selecciona dos jugadores diferentes para comparar.")
else:
    # Crear DataFrame para la tabla comparativa
    comparacion = pd.DataFrame(columns=['Estadística', jugador1, jugador2])
    comparacion['Estadística'] = grupos[grupo_seleccionado]  # Usar las estadísticas del grupo seleccionado
    comparacion[jugador1] = dfs_grupos[grupo_seleccionado].loc[dfs_grupos[grupo_seleccionado]['Nombre'] == jugador1, grupos[grupo_seleccionado]].values.flatten()
    comparacion[jugador2] = dfs_grupos[grupo_seleccionado].loc[dfs_grupos[grupo_seleccionado]['Nombre'] == jugador2, grupos[grupo_seleccionado]].values.flatten()

    # Mostrar estadísticas de ambos jugadores en un único expander, con formato vertical
    with st.expander('Comparación de Estadísticas'):
        st.dataframe(comparacion, height=450, width=700)

# Mostrar la tabla con los jugadores y puntuaciones totales
st.write(f"<div class='center-text' style='font-size: 34px;' >Puntuaciones Totales del Grupo {grupo_seleccionado}</div>", unsafe_allow_html=True)
st.dataframe(dfs_grupos[grupo_seleccionado][['Nombre', 'Equipo', f'Puntuacion_Total_{grupo_seleccionado}']], height=450, width=900)