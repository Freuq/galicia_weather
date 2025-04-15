import requests
import pandas as pd
from datetime import datetime
import json

# Tu API Key
def cargar_api_key(ruta="api_key.txt"):
    with open(ruta, "r") as f:
        return f.read().strip()

API_KEY = cargar_api_key()

# Estación meteorológica de Santiago (puede requerir ajuste según la documentación)
station = "1429"  # Ejemplo: estación de Santiago - cambiar si es necesario
lat, lon = 42.8782, -8.5448

# Variables deseadas
variables = {
    "temperatura": "temperature",
    "humedad": "relative_humidity",
    "precipitacion": "precipitation_amount"
}

# Rango de fechas
start_date = "2023-01-01T00:00:00"
end_date = "2025-01-01T00:00:00"

# URL de la API de MeteoSIX (ajústala según el endpoint exacto)
url = "http://servizos.meteogalicia.es/apiv2/getWeatherInfo"

params = {
    "API_KEY": API_KEY,
    #"locationIds": "71938",
    "coord" : "-8.5434,42.88187",
    "variables": "temperature, precipitation_amount, relative_humidity",
    #"lang" : "es",
    "startTime": start_date,
    "endTime": end_date,
    #"format": "json"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    # Guardar el JSON si quieres inspeccionarlo
    with open("data/raw/meteodata.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Datos descargados correctamente")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)