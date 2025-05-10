import pandas as pd
import json

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
    print(df_forecast.head())
    df_forecast.to_csv(f"data/processed/forecast/forecast_{i}.csv")