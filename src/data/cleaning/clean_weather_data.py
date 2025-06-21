import numpy as np
import pandas as pd
import os

def clean_weather_data(file):
    # project directory
    current_directory = os.getcwd()
    folder = current_directory.split("\\")[-1]
    if folder != 'galizia_weather':
        os.chdir('..')
        print(os.getcwd()) 
    else:
        print(os.getcwd())
    
    # path and file
    path = f"data/raw/{file}.csv"
    df = pd.read_csv(path, delimiter=";", skiprows=2)
    print(df.shape)

    # changes and cleaning
    df["Fecha"] = pd.to_datetime(df["Fecha"], dayfirst=True)
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    df_pivot = df.pivot_table(
        index="Fecha",
        columns="Variable",
        values="Valor",
        aggfunc="first"
    )

    df_pivot.columns = [col.strip().split(" ")[0].lower() for col in df_pivot.columns]
    df_pivot = df_pivot.rename(columns={
        "temperatura": "temperatura",
        "humedad": "humedad",
        "lluvia": "precipitacion"
    })
    df_pivot = df_pivot.reset_index()
    df_pivot = df_pivot.rename(columns={"Fecha":"fecha"})
    df_pivot.to_csv(f'data/processed/{file}.csv')
    print(file)
    print(df_pivot.head())

def df_galicia(localidades):
    # Ruta absoluta desde el archivo actual
    base_path = os.path.dirname(os.path.abspath(__file__))  # directorio del script actual
    project_root = os.path.abspath(os.path.join(base_path, '..', '..', '..'))  # sube hasta 'galizia_weather'
    folder = os.path.join(project_root, 'data', 'processed')
   
    dataframes = []

    if os.path.exists(folder):
        for archivo in os.listdir(folder):
            if archivo.endswith('.csv'):
                path_archivo = os.path.join(folder, archivo)
                df = pd.read_csv(path_archivo, index_col=0)
                df['ciudad'] = localidades[archivo.split(".")[0]] # columna con nombre de la ciudad
                dataframes.append(df)
    print(len(dataframes))
    df_final = pd.concat(dataframes)
    df_final["fecha"] = pd.to_datetime(df["fecha"])
    path = os.path.join(folder, 'galicia')
    archivo = "galicia.csv"
    df_final.to_csv(os.path.join(path, archivo))
    return df_final 
    
for file in ['santiago', 'coruna', 'lugo', 'pontevedra', 'ourense', 'vigo']:
    clean_weather_data(file)

localidades = {
    "santiago": "Santiago de Compostela",
    "coruna": "Coruña",
    "lugo": "Lugo",
    "ourense": "Ourense",
    "pontevedra": "Pontevedra",
    "vigo": "Vigo"}

df = df_galicia(localidades)