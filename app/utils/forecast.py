import requests
import pandas as pd
from datetime import date, timedelta, datetime
import time
import json
import os
import streamlit as st
import glob
from dotenv import load_dotenv

def cargar_api_key():
    load_dotenv()  
    try:
        # Intentar primero desde st.secrets (producción)
        return st.secrets["API_KEY"]
    except Exception:
        # Si falla (estás en local), leer desde archivo api_key.txt
        return os.getenv("API_KEY")

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

def delete_old_files(folder):
    archivos = os.listdir(folder)
    hoy = date.today()
    for archivo in archivos:
        # Verificar si el archivo sigue el patrón de "forecast_YYYY-MM-DD"
        if archivo.startswith("forecast_"):
            try:
                # Extraer la fecha del nombre del archivo
                archivo_limpio = archivo.split(".")[0]
                fecha_archivo_str = archivo_limpio[len("forecast_"):]
                fecha_archivo = date.fromisoformat(fecha_archivo_str)
                # Comparar la fecha del archivo con la fecha de hoy
                if fecha_archivo < hoy:
                    archivo_a_eliminar = os.path.join(folder, archivo)
                    os.remove(archivo_a_eliminar)  # Eliminar archivo
                    print(f"Archivo eliminado: {archivo_a_eliminar}")
            except Exception as e:
                print(f"Error al eliminar el archivo {archivo[len('forecast_'):]}: {e}")   

def file_path_():
    hoy = date.today().isoformat()
    # Definir base de proyecto sin depender del working dir
    base_path = os.path.dirname(os.path.abspath(__file__))  # app/
    project_root = os.path.abspath(os.path.join(base_path, '..', '..'))  # galizia_weather/
    folder = os.path.join(project_root, 'data', 'processed', 'forecast', 'final')
    
    # eliminar otros archivos 
    delete_old_files(folder)
    
    return os.path.join(folder, f"forecast_{hoy}.csv")    

@st.cache_data
def forecast_main(localidades):

    file_path = file_path_()
    
    # Si ya existe, lo carga
    if os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=['time'])  # Ajusta si es otra columna

    
    # Sino hace la petición a la API
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

    
    file_path = file_path_()
    df_forecast.to_csv(file_path, index=False)
    # Llamar esta función al inicio para eliminar archivos antiguos

    # Si ya existe, lo carga
    if os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=["time"])