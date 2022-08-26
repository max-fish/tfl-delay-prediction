import json

file = open('208_stations_outbound.txt')

data = json.load(file)

new_data = []

for station in data[0]['stopPoint']:
    print(station)
    new_data.append({
        'id': station['id'],
        'name': station['name'],
        'lat': station['lat'],
        'lon': station['lon']
    })

json_string = json.dumps(new_data)

with open('stations_208.txt', 'w') as outfile:
    outfile.write(json_string)