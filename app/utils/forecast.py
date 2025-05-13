import requests
import pandas as pd
from datetime import date, timedelta, datetime
import json
import os
import streamlit as st

def cargar_api_key():
    try:
        # Intentar primero desde st.secrets (producción)
        return st.secrets["API_KEY"]
    except Exception:
        # Si falla (estás en local), leer desde archivo api_key.txt
        with open("api_key.txt") as f:
            return f.read().strip()

def json_to_df(forecast_data):
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
    return dict_

def forecast_main(localidades):
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

    API_KEY = cargar_api_key()

    place_coors_dict = {}

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    json_path = os.path.join(base_path, "data", "processed", "place_coords.json")

    with open(json_path, "r") as f:
        place_coors_dict = json.load(f)

    today = date.today()

    tomorrowDay = today + timedelta(days=1)
    inicio = datetime.combine(tomorrowDay, datetime.min.time())
    final = datetime.combine(tomorrowDay, datetime.max.time()).replace(microsecond=0)

    startDay = inicio.strftime("%Y-%m-%dT%H:%M:%S")
    endDay = final.strftime("%Y-%m-%dT%H:%M:%S")

    # URL de la API de MeteoSIX (ajústala según el endpoint exacto)
    url = "http://servizos.meteogalicia.es/apiv4/getNumericForecastInfo"
    df_forecast = pd.DataFrame()
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
            forecast_data = response.json()

        dict_ = json_to_df(forecast_data)
        df_temp = pd.DataFrame(dict_)
        df_temp["time"] = pd.to_datetime(df_temp["time"])
        df_temp["hour"] = df_temp['time'].dt.strftime('%H:%M')
        df_temp['city'] = localidades[i]
        
        df_forecast = pd.concat([df_forecast, df_temp])
    
    hoy = date.today().isoformat()
    
    base_path = os.path.dirname(os.path.abspath(__file__))  # app/
    project_root = os.path.abspath(os.path.join(base_path, '..', '..'))  # galizia_weather/
    folder = os.path.join(project_root, 'data', 'processed', 'forecast', 'final')
    file_path = os.path.join(folder, f"forecast_{hoy}.csv")    
    df_forecast.to_csv(file_path, index=False)
    # Si ya existe, lo carga
    if os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=["time"])