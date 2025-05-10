import pandas as pd
from datetime import date, timedelta, datetime
import json

with open("data/raw/getForecast/forecast_santiago.json", "r") as f:
    forecast_data = json.load(f)

# 0 sky_state, 1 temperature, 2 precipitation_amount, 3 humidity_relative
#print(forecast_data["features"][0]['properties']["days"][0]['variables'][1])
sky_state = forecast_data["features"][0]['properties']["days"][0]['variables'][0]["values"]
temperature = forecast_data["features"][0]['properties']["days"][0]['variables'][1]["values"]
precipitation = forecast_data["features"][0]['properties']["days"][0]['variables'][2]["values"]
humidity = forecast_data["features"][0]['properties']["days"][0]['variables'][3]["values"]
print(sky_state)
for i in sky_state:
    time = i["timeInstant"]
    type_sky = i["value"]
    print(time, type_sky)

for i in temperature:
    time = i["timeInstant"]
    temperature_c = i["value"]
    print(time, temperature_c)
    
for i in precipitation:
    time = i["timeInstant"]
    lluvia = i["value"]
    print(time, lluvia)
    
for i in humidity:
    time = i["timeInstant"]
    humedad_rel = i["value"]
    print(time, humedad_rel)

dict_ = {}
time_path = forecast_data["features"][0]['properties']["days"][0]['variables'][0]["values"]
list_time = [date["timeInstant"] for date in time_path]
dict_["time"] = list_time
for idx, param in enumerate(["sky_state", "temperature", "precipitation", "humidity"]):
    print(idx, param)

    values = forecast_data["features"][0]['properties']["days"][0]['variables'][idx]["values"]
    list_ = []
    for v in values:
        list_.append(v["value"])
    dict_[param] = list_

print(dict_)
    