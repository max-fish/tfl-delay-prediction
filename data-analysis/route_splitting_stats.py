from matplotlib import pyplot as plt
import numpy
import pandas as pd
import datetime as dt
from route_splitting import splitRoutes, clusterRoutesTest, perBusPerStationSplitting, clusterRoutes, dbscanSplitting, hdbscanSplitting
from sklearn.cluster import DBSCAN
import time
import hdbscan
from sklearn.neighbors import NearestNeighbors

plt.rcParams['savefig.dpi'] = 600

pd.options.mode.chained_assignment = None  # default='warn'

data = pd.read_csv(r'./arrivals453inbound_12_July_2022.csv')

# pd.set_option('display.max_columns', None)

df = pd.DataFrame(data)

df['timeOfPrediction'] = df['timeOfPrediction'].apply(lambda x: dt.datetime.strptime(x.split(".")[0],'%Y-%m-%dT%H:%M:%S'))

df['expectedArrival'] = df['expectedArrival'].apply(lambda x: dt.datetime.strptime(x.split(".")[0], '%Y-%m-%dT%H:%M:%SZ'))

df.sort_values(by=['timeOfPrediction'], inplace=True)

df = df.reset_index(drop=True)

def stationApproachStats():

    splitRoutes(df)

    # clusterRoutesTest(df)

    X = []

    y = []

    # df_one_station = df.loc[df['naptanId'] == "490000011D"]

    df_group_by_approach = df.groupby(by=['approach_id'])

    for name, group in df_group_by_approach:
        # print(gxroup)
        first = group.iloc[0]

        last = group.iloc[-1]

        timeOfPredictionDiff = (last['timeOfPrediction'] - first['timeOfPrediction']).total_seconds() / 60

        # expectedArrivalDiff = (last['expectedArrival'] - first['expectedArrival']).total_seconds() / 60

        X.append([len(group), timeOfPredictionDiff])

        # y.append(len(group))

    # lof = LocalOutlierFactor(contamination=0.003)
    # yhat = lof.fit_predict(X)

    # plt.scatter(y, X)

    clusterer = hdbscan.HDBSCAN(min_cluster_size=50).fit(X)

    outlier_scores = clusterer.outlier_scores_

    non_outliers = []

    outliers = []

    for data_point, outlier_score in zip(X, outlier_scores):

        if outlier_score >= 0.6:
            outliers.append(data_point)
            # plt.scatter(data_point[0], data_point[1], c='#ff0000')
        else:
            non_outliers.append(data_point)
            # plt.scatter(data_point[0], data_point[1], c='#0000FF')

    outliers_x = map(lambda x: x[0], outliers)

    outliers_y = map(lambda x: x[1], outliers)

    non_outliers_x = map(lambda x: x[0], non_outliers)

    non_outliers_y = map(lambda x: x[1], non_outliers)

    plt.scatter(list(outliers_x), list(outliers_y), c='#ff0000')

    plt.scatter(list(non_outliers_x), list(non_outliers_y), c='#0000FF')

    plt.xlabel(xlabel='Amount of Data Points')

    plt.ylabel(ylabel='Duration (min)')

    plt.title('Station Approach Data Point Amounts and Durations')

    plt.show()

# stationApproachStats()

def graphGroupedBusRoute():
    splitRoutes(df)

    df_one_bus = df.loc[df['vehicleId'] == "LTZ1295"]

    df_group_by_route = df_one_bus.groupby(by=lambda x: df_one_bus.loc[x]['route_id'].split('_')[2])

    for name, group in df_group_by_route:
        plt.scatter(group['timeOfPrediction'], group['timeToStation'])

    plt.xlabel(xlabel='Time of Prediction (date & time)')

    plt.ylabel(ylabel='Time until Arrival (sec)')

    plt.title('Destination-Based Route Splitting')

    plt.show()

# graphGroupedBusRoute()

def avgApproachCount():
    splitRoutes(df)

    df_group_by_approach = df.groupby(by=['route_id'])

    groupLengths = []

    for name, group in df_group_by_approach:
        groupLengths.append(group.shape[0])

    print(numpy.mean(groupLengths))

# avgApproachCount()


def avgApproachDuration():
    splitRoutes(df)

    df_group_by_approach = df.groupby(by=['route_id'])

    groupDurations = []

    for name, group in df_group_by_approach:
        first = group.iloc[0]

        last = group.iloc[-1]

        timeOfPredictionDiff = (last['timeOfPrediction'] - first['timeOfPrediction']).total_seconds() / 60

        groupDurations.append(timeOfPredictionDiff)

    print(numpy.mean(groupDurations))

# avgApproachDuration()

def dbscanStats():
    df_one_bus = df.loc[df['vehicleId'] == 'LTZ1295']

    # training_data = df_one_bus.loc[:, ['timeOfPrediction', 'timeToStation']].values

    first_timestamp = df_one_bus.iloc[0]['timeOfPrediction']

    training_data = df_one_bus.apply(lambda x: [(x['timeOfPrediction'] - first_timestamp).total_seconds() / 60, x['timeToStation']], axis=1, result_type='expand')

    # training_data = df_one_bus.apply(lambda x: (x['timeOfPrediction'] - first_timestamp).total_seconds() / 60, axis=1).values.reshape(-1, 1)

#     # print(training_data)

    # neighb = NearestNeighbors(n_neighbors=4) # creating an object of the NearestNeighbors class
    # nbrs=neighb.fit(training_data) # fitting the data to the object
    # distances,indices=nbrs.kneighbors(training_data)

    # distances = numpy.sort(distances, axis = 0) # sorting the distances
    # distances = distances[:, 1] # taking the second column of the sorted distances
    # plt.rcParams['figure.figsize'] = (5,3) # setting the figure size
    # plt.plot(distances) # plotting the distances
    # plt.show()

# 1 dim: eps=1.52, min_samples=2
# 2 dim: eps=14.97, min_samples=4

    hdbscan_model = DBSCAN(eps=14.97, min_samples=4)
    result = hdbscan_model.fit_predict(training_data)

    clusters = numpy.unique(result)

    for cluster in clusters:

        indices = numpy.where(result == cluster)

        points = df_one_bus.iloc[indices]

    # approach_id = bus_id + '_' + station_name + '_' +  str(approach_id_counter)

        # df.loc[points.index, 'approach_id'] = approach_id

    # approach_id_counter += 1

        plt.scatter(points['timeOfPrediction'], points['timeToStation'])

    plt.xlabel(xlabel='Time Of Prection (date & time)')

    plt.ylabel(ylabel='Time until Arrival (sec)')

    plt.title('DBSCAN Route Clustering')

    plt.show()

# dbscanStats()

def hdbscanStats():
    df_one_bus = df.loc[df['vehicleId'] == 'LTZ1275']

    first_timestamp = df_one_bus.iloc[0]['timeOfPrediction']

    training_data = df_one_bus.apply(lambda x: [(x['timeOfPrediction'] - first_timestamp).total_seconds() / 60, x['timeToStation']], axis=1, result_type='expand')

    model = hdbscan.HDBSCAN(min_cluster_size=20)

    model_labels = model.fit_predict(training_data)

    clusters = numpy.unique(model_labels)

    for cluster in clusters:
        indices = numpy.where(model_labels == cluster)

        points = df_one_bus.iloc[indices]

        plt.scatter(points['timeOfPrediction'], points['timeToStation'])

        plt.xlabel(xlabel='Time Of Prection (date & time)')

        plt.ylabel(ylabel='Time until Arrival (sec)')

        plt.title('HDBSCAN Route Clustering')

    plt.show()

# hdbscanStats()

def splitAverages():
    hdbscanSplitting(df)

    df_grouped = df.groupby(by=['approach_id'])

    durations = []

    lengths = []

    for _, group_data in df_grouped:

        first = group_data.iloc[0]

        last = group_data.iloc[-1]

        timeOfPredictionDiff = (last['timeOfPrediction'] - first['timeOfPrediction']).total_seconds() / 60

        durations.append(timeOfPredictionDiff)

        lengths.append(len(group_data))

    print(numpy.mean(durations))

    print(numpy.var(durations))

    print(numpy.mean(lengths))

    print(numpy.var(lengths))

# splitAverages()

def graphAverages():

    duration_means = [29.40485902082437, 27.309683034078418, 889.1020659266334, 987.4922873694932]

    duration_variances = [1475.43431060373, 55.726799806566795, 1689788.2872151195, 1900938.7229666272]

    length_means = [32.68050863075128, 32.68050863075128, 31.828479350680354, 101.85599694423223]

    length_variances = [114.01765006379615, 108.08176959337068, 4416.168718647282, 15316.215321179516]

    trip_splitting_names = ['Destination-based', 'Per Station Based', 'DBSCAN Clustering', 'HDBSCAN Clustering']

    for duration_mean, length_mean, trip_splitting_name in zip(duration_means, length_means, trip_splitting_names):
        plt.scatter(duration_mean, length_mean, label=trip_splitting_name)

    plt.legend()

    # plt.scatter(length_means, numpy.sqrt(length_variances))

    # plt.errorbar(length_means, length_variances)

    plt.show()

graphAverages()