import streamlit as st
import pandas as pd
import os
import json

def cargar_df(localizacion, localidades):
    if localizacion.lower() == 'galicia':
        df = df_galicia(localidades)
    else:
        df = pd.read_csv(f"data/processed/{localizacion.lower()}.csv", parse_dates=["fecha"])
    return df

def df_galicia(localidades):
    # Ruta absoluta desde el archivo actual
    base_path = os.path.dirname(os.path.abspath(__file__))  # directorio del script actual
    project_root = os.path.abspath(os.path.join(base_path, '..', '..'))  # sube hasta 'galizia_weather'
    folder = os.path.join(project_root, 'data', 'processed')

    dataframes = []

    if os.path.exists(folder):
        for archivo in os.listdir(folder):
            if archivo.endswith('.csv'):
                path_archivo = os.path.join(folder, archivo)
                df = pd.read_csv(path_archivo, index_col=0)
                df['ciudad'] = localidades[archivo.split(".")[0]] # columna con nombre de la ciudad
                dataframes.append(df)
    df_final = pd.concat(dataframes)
    df_final["fecha"] = pd.to_datetime(df["fecha"])
    #st.dataframe(df_final, use_container_width=True, height=500)
    return df_final

def df_grouped_conteo(df):
    df_grouped = df.groupby('fecha').agg({
    'temperatura': 'mean',
    'precipitacion': 'sum',
    'humedad': 'mean'
    }).reset_index()

    df_grouped['llovio'] = df_grouped['precipitacion'] > 0
    conteo_con = df_grouped["llovio"].sum()
    conteo_sin = len(df_grouped) - conteo_con
    conteo = [conteo_con, conteo_sin]
    conteo = [conteo_con, conteo_sin]
    etiquetas = ['Días con lluvia 🌧️', 'Días sin lluvia ☀️']

    df_conteo = pd.DataFrame({
        'Tipo de día': etiquetas,
        'Cantidad': conteo
    })
    return df_grouped, df_conteo

def clasificar_temperatura(temp, categorias):
    keys = list(categorias.keys())
    values = list(categorias.values())
    if temp < values[0]:
        return f'{keys[0]}'
    elif temp < values[1]:
        return f'{keys[1]}'
    else:
        return f'{keys[2]}'

def df_categorico(df, col, categorias):
    df['categoria'] = df[col].apply(lambda valor: clasificar_temperatura(valor, categorias))
    df["categoria"] = pd.Categorical(df["categoria"], categories=list(categorias.keys()), ordered=True)
    df_cat = df.groupby("categoria").size().reset_index(name='count')
    return df_cat