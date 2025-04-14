import requests
import pandas as pd
from datetime import datetime
import json

# Tu API Key
def cargar_api_key(ruta="api_key.txt"):
    with open(ruta, "r") as f:
        return f.read().strip()

API_KEY = cargar_api_key()


# URL de la API de MeteoSIX (ajústala según el endpoint exacto)
url = "http://servizos.meteogalicia.es/apiv4/findPlaces"

for i in ['santiago', 'coru', 'lugo', 'pontevedra', 'ourense', 'vigo']:
    params = {
        "API_KEY": API_KEY,
        "location": i,
        "lang" : "es"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Guardar el JSON si quieres inspeccionarlo
        with open(f"data/raw/findPlace/findPlace_{i}.json", "w") as f:
            json.dump(data, f, indent=4)

        print("✅ Datos descargados correctamente")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)