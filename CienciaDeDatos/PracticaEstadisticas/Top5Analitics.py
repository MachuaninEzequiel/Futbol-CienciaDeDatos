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
st.sidebar.markdown("<h1 style='text-align: center; font-size: 36px;'>Análisis de Mediocampistas</h1>", unsafe_allow_html=True)

# Selección de la liga en el sidebar
liga_seleccionada = st.sidebar.selectbox('Selecciona la liga', ligas_disponibles)

# Filtrar los datos según la liga seleccionada
mediocampistas = df[(df['Pos'].str.contains('GK') != True) & (df['Min'] > 1400) & (df['Comp'].str.contains(liga_seleccionada) == True)].reset_index(drop=True)

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
def crear_radar_modificado(df, grupo, nombre_grupo, jugador_seleccionado):
    categorias = grupo
    N = len(categorias)
    etiquetas_personalizadas = [f'{i+1}º' for i in range(N)]

    valores = df[categorias].values.flatten().tolist()
    valores += valores[:1]

    # Calcula los ángulos de los ejes del radar
    angulos = [n / float(N) * 2 * np.pi for n in range(N)]
    angulos += angulos[:1]

    # Inicializa el gráfico de radar
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw=dict(polar=True))

    # Dibuja los ejes con las etiquetas
    ax.plot(angulos, valores, linewidth=1, linestyle='solid')
    ax.fill(angulos, valores, 'b', alpha=0.2)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(etiquetas_personalizadas)
    ax.set_title(f'Gráfico de Radar - {nombre_grupo} - {jugador_seleccionado}')
    
    # Calcular el área del polígono
    area_poligono = calcular_area_poligono(angulos, valores)

    # Retornar la figura y el área del polígono
    return fig, area_poligono

# Selección de grupo y jugador en el sidebar
grupo_seleccionado = st.sidebar.selectbox('Selecciona el grupo', list(grupos.keys()))
jugador_seleccionado = st.sidebar.selectbox('Selecciona el jugador', jugadores)

# Mostrar el gráfico en la parte principal
df_jugador = dfs_grupos[grupo_seleccionado][dfs_grupos[grupo_seleccionado]['Nombre'] == jugador_seleccionado]
fig, area_poligono = crear_radar_modificado(df_jugador, grupos[grupo_seleccionado], grupo_seleccionado, jugador_seleccionado)

# Mostrar la figura en la parte principal
st.pyplot(fig)
st.write(f"Área del polígono: {area_poligono:.2f}")

# Botón para mostrar estadísticas
with st.expander('Estadísticas del Jugador'):
    st.table(df_jugador)



# Shots == Shots,SoT,SoT%,Sh/90,SoT/90,G/Sh,G/SoT,AvgShotDistance,FKShots,PK,PKsAtt

# Pases == PassesCompleted,PassesAttempted,TotCmp%,TotalPassDist,ProgPassDist,ShortPassCmp,ShortPassAtt,ShortPassCmp%,MedPassCmp,MedPassAtt,MedPassCmp%,LongPassCmp,LongPassAtt,LongPassCmp%,Assists,xAG,xA,A-xAG,KeyPasses,Final1/3Cmp,PenAreaCmp,CrsPenAreaCmp,ProgPasses
# TiposDePases == LivePass,DeadPass,FKPasses,ThruBalls,Switches,Crs,ThrowIn,CK,InSwingCK,OutSwingCK,StrCK,Cmpxxx,PassesToOff,PassesBlocked

# CreacionDeGoles/Tiros == SCA,SCA90,SCAPassLive,SCAPassDead,SCADrib,SCASh,SCAFld,SCADef,GCA,GCA90,GCAPassLive,GCAPassDead,GCADrib,GCASh,GCAFld,GCADef

# AccionesDefensivas == Tkl,TklWinPoss,Def3rdTkl,Mid3rdTkl,Att3rdTkl,DrbTkl,DrbPastAtt,DrbTkl%,DrbPast,Blocks,ShBlocks,PassBlocks,Int,Tkl+Int,Clr,Err
# Rendimiento ==        Fls(faltas cometidas), Recov,AerialWins,AerialLoss,AerialWin%

# Posesion(Toques/Traslado/Recepcion) == Touches,DefPenTouch,Def3rdTouch,Mid3rdTouch,Att3rdTouch,AttPenTouch,LiveTouch,AttDrb,SuccDrb,DrbSucc%,TimesTackled,TimesTackled%,Carries,TotalCarryDistance,ProgCarryDistance,ProgCarries,CarriesToFinalThird,CarriesToPenArea,CarryMistakes,Disposesed,ReceivedPass,ProgPassesRec  

# Data/90min ==  G-xGPer90,npG-xGPer90,PassesCompletedPer90,PassesAttemptedPer90,TotCmp%Per90,TotalPassDistPer90,ProgPassDistPer90,ShortPassCmpPer90,ShortPassAttPer90,ShortPassCmp%Per90,MedPassCmpPer90,MedPassAttPer90,MedPassCmp%Per90,LongPassCmpPer90,LongPassAttPer90,LongPassCmp%Per90,AssistsPer90,xAGPer90,xAPer90,A-xAGPer90,KeyPassesPer90,Final1/3CmpPer90,PenAreaCmpPer90,CrsPenAreaCmpPer90,ProgPassesPer90,LivePassPer90,DeadPassPer90,FKPassesPer90,ThruBallsPer90,SwitchesPer90,CrsPer90,ThrowInPer90,CKPer90,InSwingCKPer90,OutSwingCKPer90,StrCKPer90,CmpxxxPer90,PassesToOffPer90,PassesBlockedPer90,SCAPer90,SCA90Per90,SCAPassLivePer90,SCAPassDeadPer90,SCADribPer90,SCAShPer90,SCAFldPer90,SCADefPer90,GCAPer90,GCA90Per90,GCAPassLivePer90,GCAPassDeadPer90,GCADribPer90,GCAShPer90,GCAFldPer90,GCADefPer90,TklPer90,TklWinPossPer90,Def3rdTklPer90,Mid3rdTklPer90,Att3rdTklPer90,DrbTklPer90,DrbPastAttPer90,DrbTkl%Per90,DrbPastPer90,BlocksPer90,ShBlocksPer90,PassBlocksPer90,IntPer90,Tkl+IntPer90,ClrPer90,ErrPer90,TouchesPer90,DefPenTouchPer90,Def3rdTouchPer90,Mid3rdTouchPer90,Att3rdTouchPer90,AttPenTouchPer90,LiveTouchPer90,AttDrbPer90,SuccDrbPer90,DrbSucc%Per90,TimesTackledPer90,TimesTackled%Per90,CarriesPer90,TotalCarryDistancePer90,ProgCarryDistancePer90,ProgCarriesPer90,CarriesToFinalThirdPer90,CarriesToPenAreaPer90,CarryMistakesPer90,DisposesedPer90,ReceivedPassPer90,ProgPassesRecPer90,YellowsPer90,RedsPer90,Yellow2Per90,FlsPer90,FldPer90,OffPer90,PKwonPer90,PKconPer90,OGPer90,RecovPer90,AerialWinsPer90,AerialLossPer90,AerialWin%Per90,90sPer90,AvgTeamPoss,OppTouches,TeamMins,TeamTouches90
# MasDataCalculada ==  pAdjTkl+IntPer90,pAdjClrPer90,pAdjShBlocksPer90,pAdjPassBlocksPer90,pAdjIntPer90,pAdjDrbTklPer90,pAdjTklWinPossPer90,pAdjDrbPastPer90,pAdjAerialWinsPer90,pAdjAerialLossPer90