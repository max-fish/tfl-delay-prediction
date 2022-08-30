import pandas as pd
from sklearn.cluster import DBSCAN
from numpy import unique, where
import numpy as np
import matplotlib.pyplot as plt
import hdbscan

def splitRoutes(df):

    df_grouped_by_bus = df.groupby(by=['vehicleId'])

    for name, group in df_grouped_by_bus:

        one_bus = group

        bus_id = name

        one_bus_only_terminals = one_bus.loc[one_bus['stationName'] == one_bus['destinationName']]
        one_bus_only_terminals['nextTimeOfPrediction'] = one_bus_only_terminals['timeOfPrediction'].shift(-1)
        one_bus_only_terminals['timeDiff'] = (one_bus_only_terminals['nextTimeOfPrediction'] - one_bus_only_terminals['timeOfPrediction']).dt.total_seconds() / 60

        routeEndTimes = one_bus_only_terminals.loc[(one_bus_only_terminals['timeDiff'] > 35) | (one_bus_only_terminals['timeDiff'].isnull())]['timeOfPrediction'].tolist()

        for index, routeEnd in enumerate(routeEndTimes):
            if index == 0:
                one_route = one_bus.loc[one_bus['timeOfPrediction'] <= routeEnd]
                one_route_indexes = one_route.index.tolist()
                
                for row_index in one_route_indexes:
                    df.loc[row_index, 'route_id'] = bus_id + '_' + df.loc[row_index, 'stationName'] + '_' + str(index)
            
            else:
                one_route = one_bus.loc[(one_bus['timeOfPrediction'] > routeEndTimes[index - 1]) & (one_bus['timeOfPrediction'] <= routeEnd)]
                one_route_indexes = one_route.index.tolist()

                for row_index in one_route_indexes:
                    df.loc[row_index, 'route_id'] = bus_id + '_' + df.loc[row_index, 'stationName'] +  '_' + str(index)

                if index == len(routeEndTimes) - 1:
                    after_route = one_bus.loc[one_bus['timeOfPrediction'] > routeEndTimes[index]]
                    after_route_indexes = after_route.index.tolist()

                    for row_index in after_route_indexes:
                       df.loc[row_index, 'route_id'] = bus_id + '_' + df.loc[row_index, 'stationName'] +  '_' + str(index + 1) 

def clusterRoutes(df):

    df_grouped_by_bus = df.groupby(by=['vehicleId'])

    for group_name, group_data in df_grouped_by_bus:

        bus_id = group_name

        one_bus = group_data

        # for index, row in one_bus_one_station.iterrows():
        #     one_bus_one_station.loc[index, 'timeOfPrediction'] = row['timeOfPrediction'].timestamp()
        #Hello <3 -- Emir
        training_data = one_bus.loc[:, ['timeOfPrediction']].values

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

        # if station_name == "Horse Guards Parade":

        #     for i in range(0, one_bus_one_station.shape[0] - 1):
        #         firstPrediction = one_bus_one_station.iloc[i]

        #         # print(firstPrediction)

        #         secondPrediction = one_bus_one_station.iloc[i + 1]

        #         timeDiff = (secondPrediction['timeOfPrediction'] - firstPrediction['timeOfPrediction']).total_seconds() / 60

        #         # plt.scatter(xaxis, timeDiff)

        #         # xaxis += 1

        #         # approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)

        #         if timeDiff <= 35:
        #             approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)
        #             df.loc[[df.index.values[i], df.index.values[i + 1]], 'approach_id'] = approach_id
        #         else:
        #             approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)
        #             df.loc[df.index.values[i], 'approach_id'] = approach_id

        #             approach_id_counter += 1
        #             approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)
        #             df.loc[df.index.values[i + 1], 'approach_id'] = approach_id

        # print(df)

        # plt.show()

        hdbscan_model = DBSCAN(eps=90, min_samples=4)
        result = hdbscan_model.fit_predict(training_data)

        clusters = unique(result)

        approach_id_counter = 0

        for cluster in clusters:

            indices = where(result == cluster)

            points = one_bus.iloc[indices]

            # approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)

            # df.loc[points.index, 'approach_id'] = approach_id

            # approach_id_counter += 1

            plt.scatter(points['timeOfPrediction'], points['timeToStation'])

    plt.show()

    # print(df)

def clusterRoutesTest(df):

    df_grouped = df.groupby(by=['vehicleId', 'stationName'])

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
                approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)
                df.loc[group_data.index.values[i], 'approach_id'] = approach_id
                

            if timeDiff <= 35:
                approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)

                df.loc[group_data.index.values[i + 1], 'approach_id'] = approach_id
            else:

                approach_id_counter += 1

                approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)
                df.loc[group_data.index.values[i + 1], 'approach_id'] = approach_id

        # break

    # plt.show()

def perBusPerStationSplitting(df):

    # start_time = time.time()

    df_grouped = df.groupby(by=['vehicleId', 'stationName'])

    for group_name, group_data in df_grouped:

        bus_id, station_name = group_name

        group_data['nextTimeOfPrediction'] = group_data['timeOfPrediction'].shift(-1)

        group_data['timeDiff'] = (group_data['nextTimeOfPrediction'] - group_data['timeOfPrediction']).dt.total_seconds() / 60

        approach_split_times = group_data.loc[(group_data['timeDiff'] > 35) | (group_data['timeDiff'].isnull())]['timeOfPrediction'].tolist()

        for index, approach_split_time in enumerate(approach_split_times):
            if index == 0:
                one_approach = group_data.loc[group_data['timeOfPrediction'] <= approach_split_time]

                one_approach_indices = one_approach.index.tolist()
                
                df.loc[one_approach_indices, 'approach_id'] = bus_id + '_' + station_name + '_' + str(index)

            else:
                one_approach = group_data.loc[(group_data['timeOfPrediction'] > approach_split_times[index - 1]) & (group_data['timeOfPrediction'] <= approach_split_time)]

                one_approach_indices = one_approach.index.tolist()

                df.loc[one_approach_indices, 'approach_id'] = bus_id + '_' + station_name +  '_' + str(index)
    # end_time = time.time()

    # print(end_time - start_time)

def splitTrips(df):
    df_grouped = df.groupby(by=['vehicleId'])

    for bus_id, bus_data in df_grouped:

        df_group_by_approach = df_grouped.groupby(by=['approach_id'])

        approach_ends_df = pd.DataFrame()
        for approach_id, approach_data in df_group_by_approach:
            new_df = pd.DataFrame({'approachEndTime': approach_data.iloc[-1]['timeOfPrediction']})
            approach_ends_df = pd.concat([approach_ends_df, new_df])

        approach_ends_df['nextApproachEnd'] = approach_ends_df['approachEndTime'].shift(-1)

        approach_ends_df['timeDiff'] = (approach_ends_df['nextApproachEnd'] - approach_ends_df['approachEndTime']).dt.total_seconds() / 60

def dbscanSplitting(df):
    df_grouped_by = df.groupby(by=['vehicleId'])

    for bus_id, one_bus_data in df_grouped_by:
        first_timestamp = one_bus_data.iloc[0]['timeOfPrediction']

        training_data = one_bus_data.apply(lambda x: [(x['timeOfPrediction'] - first_timestamp).total_seconds() / 60, x['timeToStation']], axis=1, result_type='expand')

        hdbscan_model = DBSCAN(eps=14.97, min_samples=4)

        result = hdbscan_model.fit_predict(training_data)

        clusters = np.unique(result)

        for cluster in clusters:

            indices = np.where(result == cluster)

            points = one_bus_data.iloc[indices]

            points_grouped_by_station = points.groupby(by=['stationName'])

            approach_id_counter = 0

            for station_name, points_for_station in points_grouped_by_station:

                approach_id = bus_id + '_' + station_name + '_' + str(approach_id_counter)

                df.loc[points_for_station.index, 'approach_id'] = approach_id

                approach_id_counter += 1

def hdbscanSplitting(df):

    df_grouped_by = df.groupby(by=['vehicleId'])

    for bus_id, one_bus_data in df_grouped_by:

        first_timestamp = one_bus_data.iloc[0]['timeOfPrediction']

        training_data = one_bus_data.apply(lambda x: [(x['timeOfPrediction'] - first_timestamp).total_seconds() / 60, x['timeToStation']], axis=1, result_type='expand')

        model = hdbscan.HDBSCAN(min_cluster_size=20)

        model_labels = model.fit_predict(training_data)

        clusters = np.unique(model_labels)

        for cluster in clusters:
            indices = np.where(model_labels == cluster)

            points = one_bus_data.iloc[indices]

            points_grouped_by_station = points.groupby(by=['stationName'])

            approach_id_counter = 0

            for station_name, points_for_station in points_grouped_by_station:

                approach_id = bus_id + '_' + station_name + '_' + str(approach_id_counter)

                df.loc[points_for_station.index, 'approach_id'] = approach_id

                approach_id_counter += 1