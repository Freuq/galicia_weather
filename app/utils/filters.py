# utils/filters.py
import os
import pandas as pd
import streamlit as st

MESES_ORDENADOS = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def cargar_df(localizacion):
    if localizacion.lower() == 'galicia':
        df = df_galicia()
    else:
        df = pd.read_csv(f"data/processed/{localizacion.lower()}.csv", parse_dates=["fecha"])
    return df
    
def df_galicia():
    # Ruta absoluta desde el archivo actual
    base_path = os.path.dirname(os.path.abspath(__file__))  # directorio del script actual
    project_root = os.path.abspath(os.path.join(base_path, '..', '..'))  # sube hasta 'galizia_weather'
    folder = os.path.join(project_root, 'data', 'processed')

    print(f"📁 Ruta usada: {folder}")

    dataframes = []

    if os.path.exists(folder):
        for archivo in os.listdir(folder):
            if archivo.endswith('.csv'):
                path_archivo = os.path.join(folder, archivo)
                df = pd.read_csv(path_archivo, index_col=0)
                #df['archivo'] = archivo  # columna con nombre del archivo
                dataframes.append(df)
    df_final = pd.concat(dataframes, ignore_index=True)
    df = df_final.groupby('fecha').mean().round(2).reset_index()
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df

#def coors(localizacion):   

def aplicar_filtros(df):
    # Asegúrate de que las columnas necesarias existan
    df["year"] = df["fecha"].dt.year
    df["mes_num"] = df["fecha"].dt.month
    df["mes_nombre"] = df["mes_num"].map(MESES_ORDENADOS)

    # Filtro año
    años = sorted(df["year"].unique(), reverse=True)
    año_seleccionado = st.sidebar.selectbox("Selecciona un año", ["Todos"] + años)

    df_filtrado = df.copy()
    if año_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["year"] == año_seleccionado]

    # Filtro mes
    meses_disponibles = sorted(df_filtrado["mes_num"].unique())
    meses_nombres = [MESES_ORDENADOS[m] for m in meses_disponibles]
    mes_seleccionado = st.sidebar.selectbox("Selecciona un mes", ["Todos"] + meses_nombres)

    if mes_seleccionado != "Todos":
        mes_num = [k for k, v in MESES_ORDENADOS.items() if v == mes_seleccionado][0]
        df_filtrado = df_filtrado[df_filtrado["mes_num"] == mes_num]

    return df_filtrado, año_seleccionado, mes_seleccionado

def cargar_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


