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
    
    
for file in ['santiago', 'coruna', 'lugo', 'pontevedra', 'ourense', 'vigo']:
    clean_weather_data(file)