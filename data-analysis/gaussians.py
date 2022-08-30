import itertools
import json
import math
import numpy as np
from data_analysis import getData, getDataWithRecency, getDataWithTimeToStationSection, getDataWithTimeToStationAndRecency, getDataWithTimestamps
import pandas as pd
from preprocessing import toTimestamp

def getTFLPerformance():
    df = getDataWithTimestamps()

    size = df.shape[0]

    train_cut_off_index = round(size * 0.8)

    train_data = df.loc[:train_cut_off_index]

    test_data = df.loc[train_cut_off_index:]

    predictedError = train_data['error'].mean()

    expectedArrivals = test_data['expectedArrival']

    predictedArrivals = expectedArrivals + pd.Timedelta(0, minutes=predictedError)

    actualArrivals = test_data['actualArrival']

    print(np.mean(((actualArrivals - predictedArrivals).dt.total_seconds() / 60).abs().tolist()))
    print(np.sqrt(np.mean((((actualArrivals - predictedArrivals).dt.total_seconds() / 60) ** 2).tolist())))

# getTFLPerformance()  

def generateBaselineConfidence(data):

    # data = getErrorsForGaussian()

    size = data.shape[0]

    train_cut_off_index = round(size * 0.8)

    train_data = data.loc[:train_cut_off_index]

    test_data = data.loc[train_cut_off_index:]

    mean_train_error = train_data['error'].mean()

    # mean_train_error = np.average(train_data['error'], weights=train_data['recencySection'])

    variance_train_error = test_data['error'].var()

    # variance_train_error = np.average((train_data['error'] - mean_train_error)**2, weights=train_data['recencySection'])

    sigma_train = math.sqrt(variance_train_error)

    interval2Deviation = (mean_train_error - 2*sigma_train, mean_train_error + 2*sigma_train)

    successes = 0

    absolute_prediction_errors = []

    squared_absolute_prediction_errors = []

    tries = test_data.shape[0]

    for error in test_data['error']:
        absolute_prediction_errors.append(abs(error - mean_train_error))
        squared_absolute_prediction_errors.append((error-mean_train_error)**2)
        if interval2Deviation[0] <= error <= interval2Deviation[1]:
                successes +=1

    accuracy = successes / tries

    interval_size = interval2Deviation[1] - interval2Deviation[0]

    mean_absolute_prediction_error = np.mean(absolute_prediction_errors)

    root_mean_squared_absolute_prediction_error = np.sqrt(np.mean(squared_absolute_prediction_errors))

    return (accuracy, interval_size, mean_absolute_prediction_error, root_mean_squared_absolute_prediction_error)

# print(generateBaselineConfidence())

def tryDifferentRecencySections():

    data = pd.read_csv('arrivals_208_outbound/annotated_data.csv')

    df = pd.DataFrame(data)

    toTimestamp(df)

    least_recent_timestamp = df['timeOfPrediction'].min()

    df['recencyInMinutes'] = df['timeOfPrediction'].apply(lambda x: (x - least_recent_timestamp).total_seconds() / 60)

    recency_section_data = []

    for i in range(5, 120, 5):

        df['recencySection'] = df['recencyInMinutes'].apply(lambda x: (x // i) + 1)

        accuracy, interval_size, mean_absolute_prediction_error, root_mean_squared_absolute_prediction_error = generateBaselineConfidence(df)

        recency_section_data.append([i, accuracy, interval_size, mean_absolute_prediction_error, root_mean_squared_absolute_prediction_error])

    df_recency_sections = pd.DataFrame(recency_section_data, columns=['recencySection', 'accuracy', 'intervalSize', 'meanAbsoluteError', 'rootMeanSquaredError'])

    df_recency_sections.to_csv('arrivals_208_outbound/recency_analysis.csv', index=False)

# tryDifferentRecencySections()

def findBestRecencySectionInDataFrame():
    data = pd.read_csv('arrivals_208_outbound_recency_sections_new.csv')

    df = pd.DataFrame(data)

    df.sort_values(by=['meanAbsoluteError'], inplace=True)

    print(df)

# findBestRecencySectionInDataFrame()


def confidenceWithFeatures(data, features, deviation, with_recency):

    size = data.shape[0]

    train_cut_off_index = round(size * 0.8)

    train_data = data.loc[:train_cut_off_index]

    test_data = data.loc[train_cut_off_index:]

    gaussian_means = []
    gaussian_variances = []
    gaussian_lower_intervals = []
    gaussian_upper_intervals = []
    gaussian_interval_size = []
    gaussian_accuracies = []
    gaussian_sample_sizes = []
    gaussian_misses = []
    mean_absolute_prediction_errors = []
    root_mean_squared_absolute_prediction_errors = []

    train_grouped = train_data.groupby(by=features)

    test_grouped = test_data.groupby(by=features)

    gaussian_miss_counter = 0

    for group_name, group_data in train_grouped:

        # train_errors, test_errors = train_test_split(group_data['error'], test_size=0.2, random_state=1234)

        train_errors = group_data['error']

        try:
            test_errors = test_grouped.get_group(group_name)['error']

        except KeyError:
            gaussian_miss_counter += 1
            continue

        if with_recency:
            mean_train_error = np.average(group_data['error'], weights=group_data['recencySection'])
        else:
            mean_train_error = train_errors.mean()


        if train_errors.shape[0] == 1:
            variance_train_error = 0
        else:
            if with_recency:
                variance_train_error = np.average((group_data['error'] - mean_train_error)**2, weights=group_data['recencySection'])
            else:
                variance_train_error = train_errors.var()

        sigma_train = math.sqrt(variance_train_error)

        confidence_95_interval = (mean_train_error - deviation*sigma_train, mean_train_error + deviation*sigma_train)

        tries = len(test_errors)

        absolute_prediction_errors = []

        squared_absolute_prediction_errors = []

        successes = 0

        for error in test_errors:
            absolute_prediction_errors.append(abs(error - mean_train_error))
            squared_absolute_prediction_errors.append((error - mean_train_error)**2)
            if confidence_95_interval[0] <= error <= confidence_95_interval[1]:
                successes += 1

        accuracy = successes / tries

        gaussian_means.append(mean_train_error)
        gaussian_variances.append(variance_train_error)
        gaussian_lower_intervals.append(confidence_95_interval[0])
        gaussian_upper_intervals.append(confidence_95_interval[1])
        # gaussian_interval_size.append(confidence_95_interval[1] - confidence_95_interval[0])
        gaussian_accuracies.append(accuracy)
        gaussian_sample_sizes.append(len(train_errors))
        gaussian_misses.append(gaussian_miss_counter)
        mean_absolute_prediction_errors.append(np.mean(absolute_prediction_errors))
        root_mean_squared_absolute_prediction_errors.append(np.sqrt(np.mean(squared_absolute_prediction_errors)))

    return (np.mean(gaussian_accuracies), np.mean(gaussian_upper_intervals) - np.mean(gaussian_lower_intervals), np.mean(gaussian_sample_sizes), np.mean(gaussian_misses), np.mean(mean_absolute_prediction_errors), np.mean(root_mean_squared_absolute_prediction_errors))

# print(confidenceWithFeatures(getDataWithRecency(22), ['dayOfWeek', 'partOfDay', 'stationName'], 2))

def generateTTSRangePerformance(with_recency):

    data = []

    errors = getDataWithRecency(115)

    for i in range(5, 1800, 5):

        errors['timeToStationSection'] = errors['timeToStation'].apply(lambda x: x // i)

        intervalAccuracy, intervalRange, sampleSize, misses, meanAbsoluteError, rootMeanSquaredError = confidenceWithFeatures(errors, ['timeToStationSection'], 2, with_recency)

        data.append([i, intervalAccuracy, intervalRange, meanAbsoluteError, rootMeanSquaredError])

    df_tts_range = pd.DataFrame(data, columns=['ttsSectionSize', 'intervalAccuracy', 'intervalRange', 'meanAbsoluteError', 'rootMeanSquaredError'])

    df_tts_range.to_csv('arrivals_208_outbound/tts_analysis.csv', index=False)

# generateTTSRangePerformance(False)

def findBestTTSPerformanceInDataFrame():
    data = pd.read_csv('arrivals_208_outbound/tts_recency.csv')

    df = pd.DataFrame(data)

    print(df.loc[df['meanAbsoluteError'].idxmin()])

    print(df.loc[df['rootMeanSquaredError'].idxmin()])

# findBestTTSPerformanceInDataFrame()

def getBestFeatureCombination(with_recency):

    data = []

    features = ['dayOfWeek', 'isWeekend', 'partOfDay', 'stationName', 'timeToStationSection']

    combinations1 = itertools.combinations(features, 1)

    combinations2 = itertools.combinations(features, 2)

    combinations3 = itertools.combinations(features, 3)

    combinations4 = itertools.combinations(features, 4)

    combinations5 = itertools.combinations(features, 5)

    allCombinations = list(combinations1) + list(combinations2) + list(combinations3) + list(combinations4) + list(combinations5)

    if with_recency:
        errors = getDataWithTimeToStationAndRecency(1790, 115)
    else:
        errors = getDataWithTimeToStationSection(1790)

    for combination in allCombinations:
        accuracy, bound_size, sample_size, misses, mean_absolute_error, mean_absolute_squared_error = confidenceWithFeatures(errors, list(combination), 2, with_recency)
        data.append([list(combination), accuracy, bound_size, sample_size, misses, mean_absolute_error, mean_absolute_squared_error])

    gaussians_df = pd.DataFrame(data, columns=['features', 'accuracy', 'intervalSize', 'sampleSize', 'misses', 'meanAbsoluteError', 'meanAbsoluteSquaredError'])

    gaussians_df.to_csv('features_tts_recency.csv', index=False)

# getBestFeatureCombination(True)

def findBestFeatureCombinationInDataFrame():
    data = pd.read_csv('arrivals_208_outbound/features_tts_recency.csv')

    df = pd.DataFrame(data)

    print(df.loc[df['meanAbsoluteError'].idxmin()])
    print(df.loc[df['meanAbsoluteSquaredError'].idxmin()])

# findBestFeatureCombinationInDataFrame()

def testModel():
    df = getDataWithTimeToStationAndRecency(1790, 115)

    size = df.shape[0]

    train_cut_off_index = round(size * 0.8)

    train_data = df.loc[:train_cut_off_index]

    test_data = df.loc[train_cut_off_index:]

    train_data_grouped = train_data.groupby(by=['isWeekend', 'timeToStationSection'])

    test_data_grouped = test_data.groupby(by=['isWeekend', 'timeToStationSection'])

    errors = []

    squaredErrors = []

    predictedError = np.average(train_data['error'], weights=train_data['recencySection'])

    expectedArrivals = test_data['expectedArrival']

    predictedArrivals = expectedArrivals + pd.Timedelta(0, minutes=predictedError)

    actualArrivals = test_data['actualArrival']

    errors.extend(((actualArrivals - predictedArrivals).dt.total_seconds() / 60).abs().tolist())

    squaredErrors.extend((((actualArrivals - predictedArrivals).dt.total_seconds() / 60) ** 2).tolist())

    # for test_group_name, test_group_data in test_data_grouped:

    #     isWeekend, timeToStationSection = test_group_name

    #     relevant_train_data = train_data_grouped.get_group((isWeekend, timeToStationSection))

    #     predictedError = np.average(relevant_train_data['error'], weights=relevant_train_data['recencySection'])

    #     expectedArrivals = test_group_data['expectedArrival']

    #     predictedArrivals = expectedArrivals + pd.Timedelta(0, minutes=predictedError)

    #     actualArrivals = test_group_data['actualArrival']

    #     errors.extend(((actualArrivals - predictedArrivals).dt.total_seconds() / 60).abs().tolist())

    #     squaredErrors.extend((((actualArrivals - predictedArrivals).dt.total_seconds() / 60)**2).tolist())

    # for group_name, group_data in df_grouped:

        # predictedError = np.average(group_data['error'], weights=group_data['recencySection'])

        # expectedArrivals = group_data['expectedArrival']

        # predictedArrivals = expectedArrivals + pd.Timedelta(0, minutes=predictedError)

        # actualArrivals = group_data['actualArrival']

        # errors.extend(((actualArrivals - predictedArrivals).dt.total_seconds() / 60).abs().tolist())

        # squaredErrors.extend((((actualArrivals - predictedArrivals).dt.total_seconds() / 60)**2).tolist())

    # for index, row in df.iterrows():
    #     isWeekend = row['isWeekend']
    #     timeToStationSection = row['timeToStationSection']

    #     group = df_grouped.get_group((isWeekend, timeToStationSection))

    #     predictedError = np.average(group['error'], weights=group['recencySection'])

    #     expectedArrival = row['expectedArrival']

    #     predictedArrival = expectedArrival + pd.Timedelta(0, minutes=predictedError)

    #     actualArrivalTime = row['actualArrival']

    #     errors.append(abs((actualArrivalTime - predictedArrival).total_seconds() / 60))

    #     squaredErrors.append(((actualArrivalTime - predictedArrival).total_seconds() / 60) ** 2)

    print(np.mean(errors))

    print(np.sqrt(np.mean(squaredErrors)))

# testModel()

    # confidenceWithFeatures(df, ['isWeekend', 'timeToStationSection'], 2, True)

def squeeze():
    data = pd.read_csv('arrivals_208_outbound/arrivals_208_outbound_optimized.csv')

    df_optimized = pd.DataFrame(data)
    
    deviations = np.arange(0.5, 3, 0.5)

    for i in deviations:
        print(confidenceWithFeatures(df_optimized, ['isWeekend', 'timeToStationSection'], i, True))

# squeeze()

def generateModel():
    data = pd.read_csv('arrivals_208_outbound/arrivals_208_outbound_optimized.csv')

    df_optimized = pd.DataFrame(data)

    df_grouped = df_optimized.groupby(by=['isWeekend', 'timeToStationSection'])

    modelData = {}

    for group_name, group_data in df_grouped:

        isWeekend, timeToStationSection = group_name

        weighted_average = np.average(group_data['error'], weights=group_data['recencySection'])

        weighted_variance = np.average((group_data['error'] - weighted_average)**2, weights=group_data['recencySection'])

        standard_deviation = np.sqrt(weighted_variance)

        low_end = weighted_average - 1.5 * standard_deviation

        high_end = weighted_average + 1.5 * standard_deviation

        modelData[str(isWeekend) + '_' + str(timeToStationSection)] = {'error': weighted_average,  'low_end': low_end, 'high_end': high_end}

    json_string = json.dumps(modelData)

    with open('model_data.json', 'w') as outfile:
        outfile.write(json_string)

# generateModel()