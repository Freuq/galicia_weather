import requests
import pandas as pd
from datetime import date, timedelta, datetime
import json
import os
import streamlit as st

def getForecastInfo():
    
    def cargar_api_key(ruta="api_key.txt"):
        with open(ruta, "r") as f:
            return f.read().strip()

    API_KEY = cargar_api_key()

    place_coors_dict = {}

    with open("data/processed/place_coords.json", "r") as f:
        place_coors_dict = json.load(f)

    today = date.today()

    tomorrowDay = today + timedelta(days=1)
    inicio = datetime.combine(tomorrowDay, datetime.min.time())
    final = datetime.combine(tomorrowDay, datetime.max.time()).replace(microsecond=0)

    startDay = inicio.strftime("%Y-%m-%dT%H:%M:%S")
    endDay = final.strftime("%Y-%m-%dT%H:%M:%S")

    # URL de la API de MeteoSIX (ajústala según el endpoint exacto)
    url = "http://servizos.meteogalicia.es/apiv4/getNumericForecastInfo"

    for i in ['santiago', 'coruna', 'lugo', 'pontevedra', 'ourense', 'vigo']:
        params = {
            "API_KEY": API_KEY,
            "coords": ", ".join(map(str, place_coors_dict[i]["coors"])),
            "variables" : "sky_state,temperature,precipitation_amount,relative_humidity",
            "lang": "es",
            # startTime y endTime yyyy-MM-ddTHH:mm:ss
            "startTime": startDay,
            "endTime": endDay
        }
        

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
                # Guardar el JSON si quieres inspeccionarlo
            with open(f"data/raw/getForecast/forecast_{i}.json", "w") as f:
                json.dump(data, f, indent=4)

            
def cleanForecastInfo():
    with open("data/raw/getForecast/forecast_santiago.json", "r") as f:
        forecast_data = json.load(f)

    # 0 sky_state, 1 temperature, 2 precipitation_amount, 3 humidity_relative

    for i in ['santiago', 'coruna', 'lugo', 'pontevedra', 'ourense', 'vigo']:
        with open(f"data/raw/getForecast/forecast_{i}.json", "r") as f:
            forecast_data = json.load(f)
        
        dict_ = {}
        time_path = forecast_data["features"][0]['properties']["days"][0]['variables'][0]["values"]
        list_time = [date["timeInstant"] for date in time_path]
        dict_["time"] = list_time
        for idx, param in enumerate(["sky_state", "temperature", "precipitation", "humidity"]):

            values = forecast_data["features"][0]['properties']["days"][0]['variables'][idx]["values"]
            list_ = []
            for v in values:
                list_.append(v["value"])
            dict_[param] = list_

        df_forecast = pd.DataFrame(dict_)
        #print(df_forecast.head())
        df_forecast.to_csv(f"data/processed/forecast/{i}.csv")
        
def df_forecast(localidades):
    # Ruta absoluta desde el archivo actual
    base_path = os.path.dirname(os.path.abspath(__file__))  # directorio del script actual
    project_root = os.path.abspath(os.path.join(base_path, '..', '..'))  # sube hasta 'galizia_weather'
    folder = os.path.join(project_root, 'data', 'processed', 'forecast')

    dataframes = []
    print(folder)
    if os.path.exists(folder):
        for archivo in os.listdir(folder):
            if archivo.endswith('.csv'):
                path_archivo = os.path.join(folder, archivo)
                df = pd.read_csv(path_archivo, index_col=0)
                df["time"] = pd.to_datetime(df["time"])
                df['hora'] = df['time'].dt.hour
                df["hour"] = df['time'].dt.strftime('%H:%M')
                df['city'] = localidades[archivo.split(".")[0]] # columna con nombre de la ciudad
                print(df.head())
                dataframes.append(df)
    df_final = pd.concat(dataframes)
    st.dataframe(df_final, use_container_width=True, height=500)
    print(dataframes)
    return df_final

def main_forecast(localidades):
    hoy = date.today().isoformat()

    # Definir base de proyecto sin depender del working dir
    base_path = os.path.dirname(os.path.abspath(__file__))  # app/
    project_root = os.path.abspath(os.path.join(base_path, '..', '..'))  # galizia_weather/
    folder = os.path.join(project_root, 'data', 'processed', 'forecast', 'final')
    os.makedirs(folder, exist_ok=True)
    
    file_path = os.path.join(folder, f"forecast_{hoy}.csv")    
    
    # Si ya existe, lo carga
    if os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=['time'])  # Ajusta si es otra columna

    getForecastInfo()
    cleanForecastInfo()
    df = df_forecast(localidades)
    print(df)
    # Guarda el dataframe
    df.to_csv(file_path, index=False)
    return df

localidades = {
    "santiago": "Santiago de Compostela",
    "coruna": "Coruña",
    "lugo": "Lugo",
    "ourense": "Ourense",
    "pontevedra": "Pontevedra",
    "vigo": "Vigo"}

main_forecast(localidades)