import json

file = open('bus_line_Stations_combined.txt')

data = json.load(file)

similarities = []

for i in range(0, len(data) - 1):
    for j in range(i + 1, len(data)):
        base_stations = data[i]['stations']
        comparator_stations = data[j]['stations']

        common_stations = [station for station in base_stations if station in comparator_stations]

        base_indexes = [base_stations.index(station) for station in common_stations]

        comparator_indexes = [comparator_stations.index(station) for station in common_stations]

        base_indexes.sort()

        comparator_indexes.sort()

        base_segments = []

        comparator_segments = []

        for z in range(0, len(base_indexes) - 1):
            if base_indexes[z + 1] == base_indexes[z] + 1:
                base_segments.append((base_stations[base_indexes[z]], base_stations[base_indexes[z + 1]]))

        for z in range(0, len(comparator_indexes) - 1):
            if comparator_indexes[z + 1] == comparator_indexes[z] + 1:
                comparator_segments.append((comparator_stations[comparator_indexes[z]], comparator_stations[comparator_indexes[z + 1]]))

        common_segments = [segment for segment in base_segments if segment in comparator_segments]

        similarities.append((data[i]['busLine'], data[j]['busLine'], len(common_segments), abs(len(data[i]['stations']) - len(data[j]['stations']))))

# similarities.sort(reverse=True, key=lambda similarity: similarity[2] + similarity[3] if similarity[2] + 10 > similarity[3] else similarity[2])

similarities.sort(reverse=True, key=lambda similarity: similarity[2] + similarity[3])

print(similarities[0:20])

# bus_lines = set()

# for similarity in similarities[0:11]:
#     bus_lines.add(similarity[0])
#     bus_lines.add(similarity[1])

# print('uniqueness: ' + str(len(bus_lines)))