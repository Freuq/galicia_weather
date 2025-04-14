import os
import json

# project directory
current_directory = os.getcwd()
folder = current_directory.split("\\")[-1]
if folder != 'galizia_weather':
    os.chdir('..')
    print(os.getcwd()) 
else:
    print(os.getcwd())

place_coors = []

for place in ['santiago', 'a coru', 'lugo', 'pontevedra', 'ourense', 'vigo']:
    print(place.upper())
    if place == 'a coru':
        path = f'data/raw/findPlace/findPlace_coru.json'
        with open(path, "r") as f:
            data = json.load(f)

            
    else:
        path = f'data/raw/findPlace/findPlace_{place}.json'
        with open(path, "r") as f:
            data = json.load(f)

    # Mostrar el contenido del JSON
    #print(json.dumps(data, indent=4))
    
    for i in range(len(data['features'])):
        name = data['features'][i]['properties']['name'].lower()
        municipality = data['features'][i]['properties']['municipality'].lower()
        province = data['features'][i]['properties']['province'].lower()
        if  name == municipality or name == province:
            coors = data['features'][i]['geometry']['coordinates']
            id = data['features'][i]['properties']['id']
            city = data['features'][i]['properties']['name']
            
    list_city = (city,id,coors)
    print(list_city)
    place_coors.append(list_city)    

# Guardar las coordenadas de las ciudades en un archivo JSON
with open("data/raw/city_coordinates.json", "w") as f:
    json.dump(place_coors, f, indent=4)

