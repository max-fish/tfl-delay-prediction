import json
import requests
import numpy as np

# file = open('bus-lines.txt', 'r')

# bus_lines_string = file.read()

# bus_lines = bus_lines_string.split(',')

# bus_lines_first_half = bus_lines[:len(bus_lines)//2]

# bus_lines_second_half = bus_lines[len(bus_lines)//2:]

# bus_line_station_data = []


# for bus_line in bus_lines_first_half:
#         try:
#             response = requests.get('https://api.tfl.gov.uk/line/' + bus_line + '/route/sequence/outbound?app_key=6c2701fece254c448b25dd58bc3c0a3f')
#             responseContent = response.json()

#             stations = responseContent['orderedLineRoutes'][0]['naptanIds']

#             bus_line_station_data.append({ 'busLine': bus_line, 'stations': stations })
#         except Exception as e:
#             print(bus_line)
#             print(response)


# jsonString = json.dumps(bus_line_station_data)

# with open('bus_line_stations.txt', 'w') as outfile:
#     outfile.write(jsonString)

# file = open('bus_line_stations.txt')

# data_first_half = json.load(file)

# file2 = open('bus_line_stations_2.txt')

# data_second_half = json.load(file2)

# print(len(data_first_half))

# print(len(data_second_half))

# combined_data = np.concatenate((data_first_half, data_second_half))

# print(len(combined_data))

# jsonString = json.dumps(combined_data.tolist())

# with open('bus_line_stations_combined.txt', 'w') as outfile:
#     outfile.write(jsonString)

file = open('bus_line_stations_combined.txt')

data = json.load(file)

lengths = []

for bus_info in data:
    if bus_info['busLine'] == "53":
        lengths.append(len(bus_info['stations']))
    if bus_info['busLine'] == "N53":
        lengths.append(len(bus_info['stations']))
    if len(lengths) == 2:
        break

print(abs(lengths[0] - lengths[1]))