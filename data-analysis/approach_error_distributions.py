import itertools
import pandas as pd
# from data_analysis import getErrorFromTTS
# from preprocessing import toTimestamp
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

def getTflError():
    data = pd.read_csv('arrivals_208_outbound/annotated_data.csv')

    df = pd.DataFrame(data)

    df_grouped_by_approaches = df.groupby(by=['approach_id'])

    errors = []

    for _, approach_data in df_grouped_by_approaches:
        errors.extend(onlyRange['error'])

    print(np.mean(errors))

# getTflError()

data = pd.read_csv('arrivals_208_outbound/annotated_data.csv')

df = pd.DataFrame(data)

def baseline():
    df_grouped_by_approaches = df.groupby(by=['approach_id'])

    approaches = list(df_grouped_by_approaches.groups)

    train_approach_groups, test_approach_groups = train_test_split(approaches, test_size=0.2, random_state=1234)

    values = []

    for train_approach_group in train_approach_groups:
        train_group_data = df_grouped_by_approaches.get_group(train_approach_group)

        values.extend(train_group_data['error'])

    predictedValue = np.mean(values)

    allAbsoluteErrors = []

    allSquaredErrors = []

    for test_approach_group in test_approach_groups:
        test_group_data = df_grouped_by_approaches.get_group(test_approach_group)

        absoluteErrors = []

        squaredErrors = []

        for _, row in test_group_data.iterrows():
            absolueError = abs(row['error'] - predictedValue)
            absoluteErrors.append(absolueError)
            squaredErrors.append(absolueError**2)

        allAbsoluteErrors.extend(absoluteErrors)

        allSquaredErrors.extend(squaredErrors)

    print((np.mean(allAbsoluteErrors), np.sqrt(np.mean(allSquaredErrors))))

# baseline()


def tts_feature_model(ttsSectionSize):

    # toTimestamp(df)

    # station_data = df.loc[df['stationName'] == 'Morley Road']

    df_grouped_by_approaches = df.groupby(by=['approach_id'])

    approaches = list(df_grouped_by_approaches.groups)

    train_approach_groups, test_approach_groups = train_test_split(approaches, test_size=0.2, random_state=1234)

    range_values = np.arange(0, 2000, ttsSectionSize)

    allErrors = []

    allSquaredErrors = []

    for i in range(0, len(range_values) - 1):

        train_errors = []

        for train_approach_group in train_approach_groups:
            train_approach_data = df_grouped_by_approaches.get_group(train_approach_group)

            onlyRangeTrain = train_approach_data.loc[(train_approach_data['timeToStation'] > range_values[i]) & (train_approach_data['timeToStation'] < range_values[i + 1])]

            train_errors.extend(onlyRangeTrain['error'])

        predictedError = np.mean(train_errors)

        onlyRangeModelErrors = []

        onlyRangeModelSquaredErrors = []

        for test_approach_group in test_approach_groups:
            test_approach_data = df_grouped_by_approaches.get_group(test_approach_group)

            onlyRangeTest = test_approach_data.loc[(test_approach_data['timeToStation'] > range_values[i]) & (test_approach_data['timeToStation'] < range_values[i + 1])]

            for index, row in onlyRangeTest.iterrows():
                modelError = abs(row['error'] - predictedError)
                onlyRangeModelErrors.append(modelError)
                onlyRangeModelSquaredErrors.append(modelError**2)

        allErrors.extend(onlyRangeModelErrors)

        allSquaredErrors.extend(onlyRangeModelSquaredErrors)

    return (np.nanmean(allErrors), np.sqrt(np.nanmean(allSquaredErrors)), np.nanvar(allErrors))

def features():
    features = ['dayOfWeek', 'isWeekend', 'partOfDay', 'stationName', 'timeToStationSection']

    combinations1 = itertools.combinations(features, 1)

    combinations2 = itertools.combinations(features, 2)

    combinations3 = itertools.combinations(features, 3)

    combinations4 = itertools.combinations(features, 4)

    combinations5 = itertools.combinations(features, 5)

    allCombinations = list(combinations1) + list(combinations2) + list(combinations3) + list(combinations4) + list(combinations5)

    df_grouped_by_approaches = df.groupby(by=['approach_id'])

    approaches = list(df_grouped_by_approaches.groups)

    train_approach_groups, test_approach_groups = train_test_split(approaches, test_size=0.2, random_state=1234)

    for train_approach_group in train_approach_groups:
        train_approach_data = df_grouped_by_approaches.get_group(train_approach_group)

def modelWithFeatures(features):
    df_grouped_by_approaches = df.groupby(by=['approach_id'])

    approaches = list(df_grouped_by_approaches.groups)

    train_approach_groups, test_approach_groups = train_test_split(approaches, test_size=0.2, random_state=1234)

    df_group_by_features

    for train_approach_group in train_approach_groups:
        train_approach_data = df_grouped_by_approaches.get_group(train_approach_group)

        df_group_by_features = train_approach_data.groupby(by=features)

        for feature_group, feature_data in df_group_by_features:
            

        
# ttsSections = []
# meanAbsoluteErrors = []
# rootMeanSquaredErrors = []
# approach_model_df = pd.DataFrame()
# for i in range(50, 2000, 50):
#     meanAbsoluteError, rootMeanSquaredError, variance = baseline(i)
#     new_df = pd.DataFrame({'ttsSection': i, 'meanAbsoluteError': meanAbsoluteError, 'rootMeanSquaredError': rootMeanSquaredError}, index=[0])
#     approach_model_df = pd.concat([approach_model_df, new_df])
#     # ttsSections.append(i)
#     # meanAbsoluteErrors.append(meanAbsoluteError)
#     # rootMeanSquaredErrors.append(rootMeanSquaredError)

# approach_model_df.to_csv('approach_model_tts_sections.csv', index=False)


def showTTSErrors():
    data = pd.read_csv('approach_model_tts_sections.csv')
    df = pd.DataFrame(data)

    ttsSections = df['ttsSection']

    meanAbsoluteErrors = df['meanAbsoluteError']

    rootMeanSquaredErrors = df['rootMeanSquaredError']

    plt.plot(ttsSections, meanAbsoluteErrors)

    plt.plot(ttsSections, rootMeanSquaredErrors)

    plt.xlabel(xlabel='TTS Section Size (sec)')

    plt.ylabel(ylabel='Error (min)')

    plt.title('TTS Section Performance')

    plt.show()

# showTTSErrors()

def generateModelData():
    data = pd.read_csv('arrivals_208_outbound/annotated_data.csv')

    df = pd.DataFrame(data)

    df_grouped_by_station = df.groupby(by=['stationName'])

    model_data = {}

    range_values = np.arange(0, 2000, 100)

    for station_name, station_data in df_grouped_by_station:

        df_grouped_by_approaches = station_data.groupby(by=['approach_id'])

        for i in range(0, len(range_values) - 1):

            predicted_error_values = []

            for _, approach_data in df_grouped_by_approaches:

                onlyRange = approach_data.loc[(approach_data['timeToStation'] > range_values[i]) & (approach_data['timeToStation'] < range_values[i + 1])]

                predicted_error_values.extend(onlyRange['error'])

            predicted_error = np.mean(predicted_error_values)

            sigma_error = np.sqrt(np.var(predicted_error_values))

            low = predicted_error - 2*sigma_error

            high = predicted_error + 2*sigma_error

            model_data[station_name + '_' + str(range_values[i]) + '-' + str(range_values[i + 1])] = {'predictedError': predicted_error, 'low': low, 'high': high}

    print(model_data)

# generateModelData()

def thresholdAnalysis():
    df_grouped_by_approach = df.groupby(by=['approach_id'])

    vars60 = []

    vars120 = []

    for _, approach_data in df_grouped_by_approach:
        vars60.append(approach_data.loc[0 < approach_data['timeToStation'] < 120]['error'].var())
        vars120.append(approach_data.loc[1690 < approach_data['timeToStation'] < 1750]['error'].var())

    print(np.nanmean(vars60))
    print(np.nanmean(vars120))


# thresholdAnalysis()