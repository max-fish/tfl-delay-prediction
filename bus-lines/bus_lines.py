# import json

# fileObject = open('bus_lines.json')

# busLines = json.load(fileObject)

# busLineArray = []

# for busLine in busLines:
#     busLineArray.append({"LineId": busLine['name']})

# with open('bus_line_rooms.json', 'w') as f:
#     json.dump(busLineArray, f)

import os

print(os.path.getsize('../django/TflDelayPredictionsApi/data_0.csv') / 1000000)