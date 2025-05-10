import requests
import pandas as pd
from datetime import date, timedelta, datetime
import json

# Tu API Key
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

        print("✅ Datos descargados correctamente")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)