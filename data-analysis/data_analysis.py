import numpy
import pandas as pd
import matplotlib.pyplot as plt
import hdbscan
from sklearn import cluster
from sklearn import preprocessing

from sklearn.cluster import DBSCAN, AffinityPropagation, MeanShift, dbscan
from sklearn.neighbors import NearestNeighbors

from route_splitting import perBusPerStationSplitting, splitRoutes
from preprocessing import toTimestamp, toTimestampAndSort, splitByApprachAndAddErrors, addActualArrivalTime

import time

pd.options.mode.chained_assignment = None  # default='warn'
plt.rcParams['savefig.dpi'] = 600

# data = pd.read_csv(r'arrivals_208_outbound/annotated.csv')

# df = pd.DataFrame(data)

def compressData():

    df_approaches = pd.DataFrame()

    perBusPerStationSplitting(df)

    df_grouped_by_approach = df.groupby(by=['approach_id'])

    for approach_name, approach_data in df_grouped_by_approach:
        print(approach_data[['RowKey', 'timeOfPrediction', 'timeToStation', 'expectedArrival']])
        break

def saveDataToCSV():
    
    addActualArrivalTime(df)

    df.drop(columns=[column for column in df.columns.to_list() if "@type" in column], inplace=True)
    df.to_csv('arrivals_208_outbound/annotated.csv', index=False)

# saveDataToCSV()

# compressData()

# for index, row in df.iterrows():
#     df.loc[index, 'isTerminal'] = (row['stationName'] == row['destinationName'])

def plotSingleBusJourney():

    toTimestamp(df)

    df_one_bus = df.loc[df['vehicleId'] == 'LTZ1295']

    # df_grouped = df_one_bus.groupby(by=["stationName"]).apply(lambda x: [x['timeOfPrediction'], x['timeToStation']]).reset_index(name="TimeOfPrediction_TimeToStation")

    # xylist = df_grouped['TimeOfPrediction_TimeToStation'].tolist()

    df_grouped = df_one_bus.groupby(by=['stationName'])

    for _, group_data in df_grouped:
        isTerminal = group_data.iloc[0]['stationName'] == group_data.iloc[0]['destinationName']
        plt.scatter(group_data['timeOfPrediction'], group_data['timeToStation'], marker= "^" if isTerminal else '.')

    plt.xlabel(xlabel='Time of Prediction (date & time)')

    plt.ylabel(ylabel='Time until Arrival (sec)')

    plt.title('453 Inbound Bus Route Arrival Predictions (1 Trip)')

    # for dataForStation in xylist:
    #     plt.scatter(dataForStation[0], dataForStation[1], marker= "^" if dataForStation[2].iloc[0] else ".")

    plt.show()

# plotSingleBusJourney()

def getSingleBusJourney():
    df_one_bus = df.loc[df['vehicleId'] == 'LTZ1275']

    df_grouped = df_one_bus.groupby(by=["stationName"]).apply(lambda x: [x['timeOfPrediction'], x['timeToStation'], x['isTerminal']]).reset_index(name="TimeOfPrediction_TimeToStation")

    xylist = df_grouped['TimeOfPrediction_TimeToStation'].tolist()

    return xylist


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

def showSingleApproachPredictions():

    df_one_bus = df.loc[df['vehicleId'] == 'LTZ1275']
    df_only_terminals = df_one_bus.loc[df['stationName'] == df['destinationName']]

    plt.scatter(df_only_terminals['timeOfPrediction'], [1 for i in range(0, df_only_terminals.shape[0])], marker='^', c='#FF69B4')

    plt.xlabel(xlabel='Time of Prediction (date & time)')

    plt.yticks([])

    plt.title('The Distribution of Terminal Stations based on Prediction Time')

    plt.show()

# showSingleApproachPredictions()

def viewStationApproaches():

    toTimestampAndSort(df)

    splitRoutes(df)

    # clusterRoutesTest()

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    # print(df_one_station)

    df_group_by_approach = df_one_station.groupby(by=['route_id'])

    # df_group_by_route = df_one_station.groupby(by=['approach_id'])

    for name, group in df_group_by_approach:
        plt.plot(group['timeOfPrediction'], group['expectedArrival'])

    plt.xlabel(xlabel='Time of Prediction (date & time)')

    plt.ylabel(ylabel='Expected Arrival Time (date & time)')

    plt.title('Station Approaches after Destination-Based Route Splitting')

    plt.show()

# viewStationApproaches()

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
    perBusPerStationSplitting(df)

    df_one_station = df.loc[df['naptanId'] == "490000011D"]

    df_group_by_route = df_one_station.groupby(by=['approach_id'])

    for name, group in df_group_by_route:
        firstExpectedArrival = group.iloc[0]['expectedArrival']
        lastTimeOfPrediction = group.iloc[-1]['timeOfPrediction']
        group['timeOffset'] = (lastTimeOfPrediction - group['timeOfPrediction']).apply(lambda x: x.total_seconds() / 60)
        group['error'] = (group['expectedArrival'] - firstExpectedArrival).apply(lambda x: x.total_seconds() / 60)

        plt.plot(group['timeOfPrediction'], group['timeToStation'])

    # plt.xlabel('Time until Arrival (min)')

    # plt.ylabel('Time diff from initial prediction (min)')

    # plt.gca().invert_xaxis()
    
    plt.show()

def getError():

    df_errors = pd.DataFrame()

    perBusPerStationSplitting(df)

    df_one_station = df.loc[df['naptanId'] == "490G00011703"]

    df_group_by_route = df_one_station.groupby(by=['approach_id'])

    for name, group in df_group_by_route:
        first = group.iloc[0]['expectedArrival']
        last = group.iloc[-1]['expectedArrival']

        error = (last - first).total_seconds() / 60

        isWeekend = last.day_of_week >= 5

        lastHour = last.hour

        lastMinute = last.minute

        partOfDay = getPartOfDay(lastHour)

        new_df = pd.DataFrame({'error': error, 'dayOfWeek': last.day_of_week, 'isWeekend': isWeekend, 'partOfDay': partOfDay }, index=[0])

        df_errors = pd.concat([df_errors, new_df])
        
    return df_errors

def getPartOfDay(hour):
    if 5 <= hour < 9:
        return 0
    elif 9 <= hour < 12:
        return 1
    elif 12 <= hour < 16:
        return 2
    elif 16 <= hour < 17:
        return 3
    elif 17 <= hour < 19:
        return 4
    elif 19 <= hour < 21:
        return 5
    elif (21 <= hour <= 24) or (0 <= hour < 5):
        return 6


def getData():

    # toTimestamp(df)

    # df['hour'] = df['expectedArrival'].apply(lambda x: x.hour)
    # df['partOfDay'] = df['hour'].apply(lambda x: getPartOfDay(x))
    # df['dayOfWeek'] = df['expectedArrival'].apply(lambda x: x.day_of_week)
    # df['isWeekend'] = df['dayOfWeek'].apply(lambda x: x >= 5)
    # df['weekOfMonth'] = df['expectedArrival'].apply(lambda x: (x.day-1) // 7 + 1)

    # df['timeToStationSection'] = df['timeToStation'].apply(lambda x: x // 70)

    # least_recent_timestamp = df['timeOfPrediction'].min()

    # df['recencySection'] = df['timeOfPrediction'].apply(lambda x: ((x - least_recent_timestamp).total_seconds() / 60) // 30)
    return df

def getDataWithTimestamps():
    toTimestampAndSort(df)

    return df

# getErrorsForGaussian()

def getDataWithRecency(recencySection):
    toTimestamp(df)

    least_recent_timestamp = df['timeOfPrediction'].min()

    df['recencySection'] = df['timeOfPrediction'].apply(lambda x: ((x - least_recent_timestamp).total_seconds() / 60) // recencySection)

    return df

def getDataWithTimeToStationSection(tts_section):

    df['timeToStationSection'] = df['timeToStation'].apply(lambda x: x // tts_section)

    return df

def getDataWithTimeToStationAndRecency(tts_section, recencySection):

    toTimestampAndSort(df)

    least_recent_timestamp = df['timeOfPrediction'].min()

    df['recencySection'] = df['timeOfPrediction'].apply(lambda x: (((x - least_recent_timestamp).total_seconds() / 60) // recencySection) + 1)

    df['timeToStationSection'] = df['timeToStation'].apply(lambda x: (x // tts_section) + 1)

    return df



def getErrorFromTTS(approach_data, tts):

    # df_errors = pd.DataFrame()

    lastExpectedArrival = approach_data.iloc[-1]['expectedArrival']

    error = None

    tts_predictions = approach_data[approach_data['timeToStation'] == tts]

    if tts_predictions.shape[0] > 0:
        if tts_predictions.shape[0] == 1:
                expectedArrivalForTTS = tts_predictions.iloc[0]['expectedArrival']
                error = (lastExpectedArrival - expectedArrivalForTTS).total_seconds() / 60
        elif tts_predictions.shape[0] > 1:
                averageExpectedArrvialForTTS = pd.Timestamp(numpy.mean(tts_predictions['expectedArrival'].apply(lambda x: x.value)))
                error = (lastExpectedArrival.tz_localize(None) - averageExpectedArrvialForTTS).total_seconds() / 60
    else:
        lower = approach_data[approach_data['timeToStation'] < tts]
        higher = approach_data[approach_data['timeToStation'] > tts]

        closestPredictions = []

        if lower.shape[0] > 0:
            lowerIdx = lower['timeToStation'].idxmax()
            closestPredictions.append(approach_data.loc[lowerIdx])
        if higher.shape[0] > 0:
            higherIdx = higher['timeToStation'].idxmin()
            closestPredictions.append(approach_data.loc[higherIdx])

        if len(closestPredictions) == 1:
            closestPrediction = closestPredictions[0]
            error = (lastExpectedArrival - closestPrediction['expectedArrival']).total_seconds() / 60
        elif len(closestPredictions) == 2:
            firstClosestPrediction = closestPredictions[0]
            secondClosestPrediction = closestPredictions[1]

            firstTTSDiff = abs(tts - firstClosestPrediction['timeToStation'])
            secondTTSDiff = abs(tts - secondClosestPrediction['timeToStation'])

            if firstTTSDiff > secondTTSDiff:
                error = (lastExpectedArrival - secondClosestPrediction['expectedArrival']).total_seconds() / 60
            elif firstTTSDiff < secondTTSDiff:
                error = (lastExpectedArrival - firstClosestPrediction['expectedArrival']).total_seconds() / 60
            else:
                averageExpectedArrival = pd.Timestamp(numpy.mean([firstClosestPrediction['expectedArrival'].value, secondClosestPrediction['expectedArrival'].value]))

                error = (lastExpectedArrival.tz_localize(None) - averageExpectedArrival).total_seconds() / 60

    return error

# getErrorFromTTS(500)

def fromTtsSanityCheck():
    x = []
    error_averages = []
    error_variances = []
    for tts in range(60, 1800):
        data = getErrorFromTTS(tts)
        errors = data['error']

        x.append(tts)
        error_averages.append(numpy.mean(errors))
        error_variances.append(numpy.var(errors))

    plt.scatter(x, error_averages, c='#0000FF', label='average')
    plt.scatter(x, error_variances, c='#ff0000', label='variance')

    # plt.legend()

    plt.xlabel(xlabel='Time to station (sec)')

    plt.ylabel(ylabel='Error (min)')

    plt.title('Mean and Variance of Prediction Error vs Time to Station')

    plt.gca().invert_xaxis()

    plt.show()

# fromTtsSanityCheck()

def ttsErrors():

    df_grouped_by_tts = df.groupby(by=['timeToStation'])

    error_means = []

    error_vars = []

    num_errors = []

    x = []

    for tts, tts_data in df_grouped_by_tts:
        x.append(tts)
        error_means.append(numpy.mean(tts_data['error']))
        error_vars.append(numpy.var(tts_data['error']))
        num_errors.append(tts_data.shape[0])

    plt.scatter(x, error_means, label='mean')

    plt.scatter(x, error_vars, label='variance')

    plt.scatter(x, num_errors, label='amount')

    plt.legend()

    plt.show()

# ttsErrors()

def ttsAnalysis():
    data = pd.read_csv('arrivals_208_outbound/arrivals_208_outbound_tts_analysis_new.csv')

    df = pd.DataFrame(data, columns=['ttsSectionSize', 'intervalAccuracy', 'intervalRange', 'meanAbsoluteError', 'rootMeanSquaredError'])

    plt.xlabel(xlabel='TTS Section Size (sec)')

    plt.ylabel(ylabel='Error (min)')

    plt.title('TTS Section Performance')
    
    plt.plot(df['ttsSectionSize'], df['meanAbsoluteError'], label='Mean Absolute Error')

    plt.plot(df['ttsSectionSize'], df['rootMeanSquaredError'], label='Root Mean Squared Error')

    plt.legend()

    plt.show()

# ttsAnalysis()


def averageTimestamp():
    time1 = '2022-07-10T04:44:05.3660733Z'
    time2 = '2022-07-10T04:44:35.4640716Z'

    timestamp1 = pd.to_datetime(time1)
    timestamp2 = pd.to_datetime(time2)

    mean_timestamp = timestamp1 + ((timestamp2 - timestamp1) / 2)

    print(pd.Timestamp(numpy.mean([timestamp1.value, timestamp2.value])))

# averageTimestamp()
    
# plotApproachErrorsTimeSeries()


# calculateError()

# calculateError('Great Central Street')

# plotSingleBusJourney()

# viewStationApproaches()

# showError()

def saveBestFeatures():
    df = getDataWithTimeToStationAndRecency(1790, 115)

    df.to_csv('arrivals_208_outbound/arrivals_208_outbound_optimized.csv', index=False)

# saveBestFeatures()

def showAnnotatedErrors():
    data = pd.read_csv('arrivals_208_outbound/annotated_data.csv')

    df = pd.DataFrame(data)

    toTimestamp(df)    

    df_group_by = df.loc[df['stationName'] == "Old Bromley Road"].groupby(by=['approach_id'])

    print(df_group_by)

    amount = 0
    for _, group_data in df_group_by:
      last = group_data.iloc[-1]['timeOfPrediction']
      plt.plot(group_data['timeOfPrediction'], group_data['error'] * 60)
      plt.plot(group_data['timeOfPrediction'], group_data['timeToStation'])
      plt.show()
      amount += 1
      if amount > 3:
        break

# showAnnotatedErrors()

def approachSplitSnippet():
    data = pd.read_csv('arrivals453inbound_12_July_2022.csv')

    df = pd.DataFrame(data)

    pd.set_option('display.max_columns', None)

    toTimestampAndSort(df)

    perBusPerStationSplitting(df)

    df_one_station = df.loc[df['stationName'] == "Trafalgar Avenue"]

    df_grouped = df_one_station.groupby(by=['approach_id'])

    groups_names = list(df_grouped.groups)

    first_group = groups_names[1]

    second_group = groups_names[2]

    first_approach_data = df_grouped.get_group(first_group)

    second_approach_data = df_grouped.get_group(second_group)

    first_preview = first_approach_data.tail(3).apply(lambda x: [x['RowKey'].split('_')[0], x['stationName'], x['timeOfPrediction'], x['timeToStation'], x['expectedArrival']], axis=1, result_type='expand')

    second_preview = second_approach_data.head(3).apply(lambda x: [x['RowKey'].split('_')[0], x['stationName'], x['timeOfPrediction'], x['timeToStation'], x['expectedArrival']], axis=1, result_type='expand')

    print(first_preview)

    print(second_preview)

# approachSplitSnippet()