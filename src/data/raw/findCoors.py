import os
import json

place_coors_dict = {}

for place in ['santiago', 'a coru', 'lugo', 'pontevedra', 'ourense', 'vigo']:
    print(place.upper())

    # Ruta ajustada para el caso especial de A Coruña
    filename = 'coru' if place == 'a coru' else place
    path = f'data/raw/findPlace/findPlace_{filename}.json'

    with open(path, "r") as f:
        data = json.load(f)

    # Buscar ciudad válida dentro del JSON
    for feature in data['features']:
        name = feature['properties']['name'].lower()
        municipality = feature['properties']['municipality'].lower()
        province = feature['properties']['province'].lower()

        if name == municipality or name == province:
            coors = feature['geometry']['coordinates']
            id_ = feature['properties']['id']
            city = feature['properties']['name'].lower().split(' ')[0]
            
            if city == 'a':
                city = 'coruna'
            # Guardar en dict
            place_coors_dict[city] = {"id": id_, "coors": coors}
            break  # salimos después de encontrar la coincidencia

# (Opcional) Guardar como JSON
with open("data/processed/place_coords.json", "w") as f:
    json.dump(place_coors_dict, f, indent=4)

print("✅ Diccionario generado y guardado")

