from cProfile import label
import math
from posixpath import split
from turtle import color
from unicodedata import name
from numpy import unique, where
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import datetime as dt
import hdbscan
from sklearn import cluster

from sklearn.cluster import DBSCAN, AffinityPropagation, MeanShift, dbscan
from sklearn.neighbors import NearestNeighbors

pd.options.mode.chained_assignment = None  # default='warn'

data = pd.read_csv(r'./arrivals453inbound_12_July_2022.csv')

# pd.set_option('display.max_columns', None)

df = pd.DataFrame(data)

df['timeOfPrediction'] = df['timeOfPrediction'].apply(lambda x: dt.datetime.strptime(x.split(".")[0],'%Y-%m-%dT%H:%M:%S'))

df['expectedArrival'] = df['expectedArrival'].apply(lambda x: dt.datetime.strptime(x.split(".")[0], '%Y-%m-%dT%H:%M:%SZ'))

df.sort_values(by=['timeOfPrediction'], inplace=True)

df = df.reset_index(drop=True)

for index, row in df.iterrows():
    df.loc[index, 'isTerminal'] = (row['stationName'] == row['destinationName'])

def plotSingleBusJourney():

    df_one_bus = df.loc[df['vehicleId'] == 'LTZ1295']

    df_grouped = df_one_bus.groupby(by=["stationName"]).apply(lambda x: [x['timeOfPrediction'], x['timeToStation'], x['isTerminal']]).reset_index(name="TimeOfPrediction_TimeToStation")

    xylist = df_grouped['TimeOfPrediction_TimeToStation'].tolist()

    for dataForStation in xylist:
        plt.scatter(dataForStation[0], dataForStation[1], marker= "^" if dataForStation[2].iloc[0] else ".")

    plt.show()

# plotSingleBusJourney()

def getSingleBusJourney():
    df_one_bus = df.loc[df['vehicleId'] == 'LTZ1275']

    df_grouped = df_one_bus.groupby(by=["stationName"]).apply(lambda x: [x['timeOfPrediction'], x['timeToStation'], x['isTerminal']]).reset_index(name="TimeOfPrediction_TimeToStation")

    xylist = df_grouped['TimeOfPrediction_TimeToStation'].tolist()

    return xylist

def splitRoutes():
    df_grouped_by_bus = df.groupby(by=['vehicleId'])

    for name, group in df_grouped_by_bus:

        one_bus = group

        bus_id = name

        one_bus_only_terminals = one_bus.loc[one_bus['stationName'] == one_bus['destinationName']]
        one_bus_only_terminals['nextTimeOfPrediction'] = one_bus_only_terminals['timeOfPrediction'].shift(-1)
        one_bus_only_terminals['timeDiff'] = (one_bus_only_terminals['nextTimeOfPrediction'] - one_bus_only_terminals['timeOfPrediction']).dt.total_seconds() / 60

        # print(one_bus_only_terminals['timeDiff'])

        routeEndTimes = one_bus_only_terminals.loc[(one_bus_only_terminals['timeDiff'] > 10) | (one_bus_only_terminals['timeDiff'].isnull())]['timeOfPrediction'].tolist()

        for index, routeEnd in enumerate(routeEndTimes):
            if index == 0:
                one_route = one_bus.loc[one_bus['timeOfPrediction'] <= routeEnd]
                one_route_indexes = one_route.index.tolist()
                
                for row_index in one_route_indexes:
                    df.loc[row_index, 'route_id'] = bus_id + '_' + str(index)
            
            else:
                one_route = one_bus.loc[(one_bus['timeOfPrediction'] > routeEndTimes[index - 1]) & (one_bus['timeOfPrediction'] <= routeEnd)]
                one_route_indexes = one_route.index.tolist()

                for row_index in one_route_indexes:
                    df.loc[row_index, 'route_id'] = bus_id + '_' + str(index)

def clusterRoutes():

    df_grouped_by_bus = df.groupby(by=['vehicleId', 'stationName'])

    for group_name, group_data in df_grouped_by_bus:

        bus_id, station_name = group_name

        one_bus_one_station = group_data

        # for index, row in one_bus_one_station.iterrows():
        #     one_bus_one_station.loc[index, 'timeOfPrediction'] = row['timeOfPrediction'].timestamp()

        training_data = one_bus_one_station.loc[:, ['timeOfPrediction']].values

        # neighb = NearestNeighbors(n_neighbors=2) # creating an object of the NearestNeighbors class
        # nbrs=neighb.fit(training_data) # fitting the data to the object
        # distances,indices=nbrs.kneighbors(training_data)

        # distances = numpy.sort(distances, axis = 0) # sorting the distances
        # distances = distances[:, 1] # taking the second column of the sorted distances
        # plt.rcParams['figure.figsize'] = (5,3) # setting the figure size
        # plt.plot(distances) # plotting the distances
        # plt.show()

        xaxis = 0

        # plt.scatter(one_bus_one_station['timeOfPrediction'], numpy.ones(one_bus_one_station.shape[0]))

        approach_id_counter = 0

        if station_name == "Horse Guards Parade":

            for i in range(0, one_bus_one_station.shape[0] - 1):
                firstPrediction = one_bus_one_station.iloc[i]

                # print(firstPrediction)

                secondPrediction = one_bus_one_station.iloc[i + 1]

                timeDiff = (secondPrediction['timeOfPrediction'] - firstPrediction['timeOfPrediction']).total_seconds() / 60

                # plt.scatter(xaxis, timeDiff)

                # xaxis += 1

                # approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)

                if timeDiff <= 35:
                    approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)
                    df.loc[[df.index.values[i], df.index.values[i + 1]], 'approach_id'] = approach_id
                else:
                    approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)
                    df.loc[df.index.values[i], 'approach_id'] = approach_id

                    approach_id_counter += 1
                    approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)
                    df.loc[df.index.values[i + 1], 'approach_id'] = approach_id

        # print(df)

        # plt.show()

        # hdbscan_model = DBSCAN(eps=90, min_samples=4)
        # result = hdbscan_model.fit_predict(training_data)

        # clusters = unique(result)

        # approach_id_counter = 0

        # for cluster in clusters:

        #     indices = where(result == cluster)

        #     points = one_bus_one_station.iloc[indices]

        #     # approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)

        #     # df.loc[points.index, 'approach_id'] = approach_id

        #     # approach_id_counter += 1

        #     plt.scatter(points['timeOfPrediction'], numpy.ones(len(points['timeOfPrediction'])))

    # plt.show()

    # print(df)

# clusterRoutes()


def getStationApproaches():

    splitRoutes()

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    df_group_by_route = df_one_station.groupby(by=['route_id'])

    approaches_df = pd.DataFrame()

    for name, group in df_group_by_route:
        new_df = group[['timeOfPrediction', 'timeToStation']]
        approaches_df = pd.concat([approaches_df, new_df])

    return approaches_df

# getStationApproaches()

def clusterRoutesTest():

    df_grouped = df.groupby(by=['vehicleId', 'stationName'])

    xaxis = 0

    for group_name, group_data in df_grouped:

        bus_id, station_name = group_name

        approach_id_counter = 0

        for i in range(0, group_data.shape[0] - 1):
            first = group_data.iloc[i]['timeOfPrediction']
            second = group_data.iloc[i + 1]['timeOfPrediction']

            timeDiff = (second - first).total_seconds() / 60

            # print(timeDiff)

            # plt.scatter(xaxis, timeDiff)

            # xaxis += 1

            if i == 0:
                approach_id = bus_id + '_' + str(approach_id_counter)
                df.loc[group_data.index.values[i], 'approach_id'] = approach_id
                

            if timeDiff <= 35:
                approach_id = bus_id + '_' + str(approach_id_counter)

                df.loc[group_data.index.values[i + 1], 'approach_id'] = approach_id
            else:

                approach_id_counter += 1

                approach_id = bus_id + '_' + str(approach_id_counter)
                df.loc[group_data.index.values[i + 1], 'approach_id'] = approach_id

        # break

    # plt.show()

# clusterRoutesTest()

def showSingleApproachPredictions():
    df_grouped = df.groupby(by=['vehicleId', 'stationName'])

    pd.set_option('display.max_columns', None)

    for group_name, group_data in df_grouped:
        print(group_data)
        break

# showSingleApproachPredictions()

def viewStationApproaches():
    splitRoutes()

    # clusterRoutesTest()

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    # print(df_one_station)

    df_group_by_approach = df_one_station.groupby(by=['route_id'])

    # df_group_by_route = df_one_station.groupby(by=['approach_id'])

    for name, group in df_group_by_approach:
        plt.plot(group['timeOfPrediction'], group['expectedArrival'])

    plt.show()

viewStationApproaches()

def stationApproachStats():

    splitRoutes()

    # clusterRoutesTest()

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    df_group_by_approach = df_one_station.groupby(by=['route_id'])

    for name, group in df_group_by_approach:
        # print(gxroup)
        first = group.iloc[0]

        last = group.iloc[-1]

        timeOfPredictionDiff = (last['timeOfPrediction'] - first['timeOfPrediction']).total_seconds() / 60

        expectedArrivalDiff = (last['expectedArrival'] - first['expectedArrival']).total_seconds() / 60

        plt.scatter(timeOfPredictionDiff, expectedArrivalDiff)

    plt.show()

# stationApproachStats()

def time_sections():

    splitRoutes()

    df_group_by_route = df.groupby(by=['vehicleId', 'route_id'])

    # print(df_group_by_route.size())

    for name, group in df_group_by_route:
        vehicleId = name[0]

        routeId = name[1]

        plt.scatter(group.iloc[0]['timeOfPrediction'], 1)

        # print(group.iloc[-1]['timeOfPrediction'])


        # plt.scatter([vehicleId, vehicleId], [first_time, last_time])

    plt.show()

    # for name, group in df_group_by_route:
    #     first_time = group.iloc[0]['timeOfPrediction']

    #     last_time = group.iloc[-1]['timeOfPrediction']

    #     plt.scatter(name, first_time)
    #     plt.scatter(name, last_time)

    # plt.show()


# time_sections()

def plotBusRoute():

    naptan_ids_453 = [
                "490007400M",
                "490015040W",
                "490000011D",
                "490007807E",
                "490000191A",
                "490000091E",
                "490010198W",
                "490000173RF",
                "490004810RJ",
                "490000179F",
                "490007960P",
                "490013767A",
                "490019475P",
                "490008376S",
                "490000266G",
                "490005646E",
                "490009420E",
                "490000132C",
                "490012693D",
                "490009281E",
                "490000073J",
                "490011632BA",
                "490003658BB",
                "490004315BK",
                "490006379BL",
                "490006266EC",
                "490013761EE",
                "490009531E",
                "490010880EN",
                "490005526EP",
                "490008461ER",
                "490003246Z",
                "490010204G",
                "490000156R",
                "490009689S",
                "490000155V",
                "490006051E",
                "490002029S"
            ]

    splitRoutes()

    current_timestamp = None

    xValues = []
    yValues = []

    # df_grouped = df.groupby(by=['naptanId'])

    df_one_route = df.loc[df['route_id'] == df['route_id'].iloc[0]]

    # print(df_one_route)

    df_grouped = df_one_route.groupby(by=['naptanId'])

    for naptanId in naptan_ids_453:
        try:
            group = df_grouped.get_group(naptanId)
        except:
            continue

        # if current_timestamp == None:
        #     first_entry = group.iloc[0]
        # else:
        #     futures = group.loc[group['timeOfPrediction'] >= current_timestamp]
            
        #     if futures.shape[0] == 0:
        #         continue

        #     first_entry = futures.iloc[0]
                
        # xValues.append(first_entry['timeOfPrediction'])
        # yValues.append(first_entry['timeToStation'])

        last_entry = group.iloc[-1]
        xValues.append(last_entry['timeOfPrediction'])
        yValues.append(last_entry['expectedArrival'])

        plt.scatter(last_entry['timeOfPrediction'], last_entry['expectedArrival'])

        current_timestamp = last_entry['timeOfPrediction']

    plt.plot(xValues, yValues)

    plt.show()

# plotBusRoute()

def plotSingleJourney():

    splitRoutes()

    df_one_route = df.loc[df['route_id'] == "LTZ1273_0"]

    df_grouped = df_one_route.groupby(by=["stationName"]).apply(lambda x: [x['timeOfPrediction'], x['timeToStation'], x['isTerminal'], x['stationName']]).reset_index(name="TimeOfPrediction_TimeToStation")

    xylist = df_grouped['TimeOfPrediction_TimeToStation'].tolist()

    print(xylist)

    for dataForStation in xylist:
        plt.scatter(dataForStation[0], dataForStation[1], marker= "^" if dataForStation[2].iloc[0] else ".")

    plt.show()

# plotSingleJourney()

def getLatestArrivalTime(naptanId, group):
    df_only_naptanId = group.loc[group['naptanId'] == naptanId]

    return (df_only_naptanId.iloc[-1]['expectedArrival'], df_only_naptanId.iloc[-1]['timeOfPrediction'])

def showError():
    # values = []
    # ptr = -1
    # previousPredictionId = None
    # df_one_station = df.loc[df['stationName'] == stationName]

    # df_one_station['timeOfPrediction'] = df_one_station['timeOfPrediction'].apply(lambda x: dt.datetime.strptime(x.split(".")[0],'%Y-%m-%dT%H:%M:%S'))

    # df_one_station['expectedArrival'] = df_one_station['expectedArrival'].apply(lambda x: dt.datetime.strptime(x.split(".")[0], '%Y-%m-%dT%H:%M:%SZ'))

    # df_one_station.sort_values(by=['timeOfPrediction'], inplace=True)

    # for index, row in df_one_station.iterrows():
    #     currentPredictionId = row['RowKey'].split('_')[0]
    #     if currentPredictionId != previousPredictionId:
    #         previousPredictionId = currentPredictionId
    #         ptr += 1
    #         values.append([[], []])
    #     values[ptr][0].append(row['timeOfPrediction'])
    #     values[ptr][1].append(row['expectedArrival'])
        
    # # print(len(values))
    # firstGraph = values[0]
    # plt.scatter(firstGraph[0], firstGraph[1])
    # plt.show()
    splitRoutes()

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    df_group_by_route = df_one_station.groupby(by=['route_id'])

    for name, group in df_group_by_route:
        error = 0
        firstExpectedArrival = group.iloc[0]['expectedArrival']
        lastTimeOfPrediction = group.iloc[-1]['timeOfPrediction']
        group['timeOffset'] = (lastTimeOfPrediction - group['timeOfPrediction']).apply(lambda x: x.total_seconds() / 60)
        group['error'] = (group['expectedArrival'] - firstExpectedArrival).apply(lambda x: x.total_seconds() / 60)

        plt.plot(group['timeOffset'], group['error'])

    plt.xlabel('Time until Arrival (min)')

    plt.ylabel('Time diff from initial prediction (min)')

    plt.gca().invert_xaxis()
    
    plt.show()

def calculateErrorFromMin(min):

    clusterRoutesTest()

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    df_group_by_route = df_one_station.groupby(by=['route_id'])

    df_errors = pd.DataFrame()

    for name, group in df_group_by_route:

        lastTimeOfPrediction = group.iloc[-1]['timeOfPrediction']

        group['timeOffset'] = (lastTimeOfPrediction - group['timeOfPrediction']).apply(lambda x: x.total_seconds() / 60)

        firstExpectedArrivalAfterMin = group.loc[group['timeOffset'] <= min].iloc[0]['expectedArrival']

        lastPrediction = group.iloc[-1]['expectedArrival']

        # group['error'] = (group['expectedArrival'] - firstExpectedArrivalAfterMin).apply(lambda x: x.total_seconds() / 60)

        error = (lastPrediction - firstExpectedArrivalAfterMin).total_seconds() / 60

        new_df = pd.DataFrame({ 'error': error }, index=[0])

        df_errors = pd.concat([df_errors, new_df])

    return df_errors

def calculateErrorFromTTS():

    clusterRoutesTest()

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    df_group_by_route = df_one_station.groupby(by=['approach_id'])

    df_errors = pd.DataFrame()

    for name, group in df_group_by_route:
        lastTimeOfPrediction = group.iloc[-1]['timeOfPrediction']



def getError():

    df_errors = pd.DataFrame()

    clusterRoutesTest()

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    df_group_by_route = df_one_station.groupby(by=['approach_id'])

    for name, group in df_group_by_route:
        first = group.iloc[0]['expectedArrival']
        last = group.iloc[-1]['expectedArrival']

        error = (last - first).total_seconds() / 60
        
        new_df = pd.DataFrame({ 'route': name, 'error': error }, index=[0])

        df_errors = pd.concat([df_errors, new_df])
        
    return df_errors

def plotApproachErrorsTimeSeries():
    df_errors = pd.DataFrame()

    clusterRoutesTest()

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    df_group_by_approach = df_one_station.groupby(by=['approach_id'])

    for name, group in df_group_by_approach:
        first = group.iloc[0]['expectedArrival']
        last = group.iloc[-1]['expectedArrival']

        error = (last - first).total_seconds() / 60

        plt.scatter(group.iloc[-1]['timeOfPrediction'], error)

    plt.show()

# plotApproachErrorsTimeSeries()


# calculateError()

# calculateError('Great Central Street')

# plotSingleBusJourney()

# viewStationApproaches()

# showError()