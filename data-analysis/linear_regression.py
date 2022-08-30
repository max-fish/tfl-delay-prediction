from inspect import BoundArguments
import math
import numpy as np
import pandas as pd
from scipy import rand
from sklearn import gaussian_process
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, DotProduct
import scipy.stats as stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import KFold, train_test_split
from sklearn.tree import DecisionTreeRegressor
from data_analysis import getError, getErrorsForGaussian
import random
import itertools

def getTFLPerformance():
    data = pd.read_csv('arrivals_208_outbound_annotated.csv')

    df = pd.DataFrame(data)

    mean_absolute_error = df['error'].abs().mean()

    mean_squared_absolute_error = (df['error']**2).mean()

    print(str(mean_absolute_error))

    print(str(mean_squared_absolute_error))

# getTFLPerformance()


def generateBaselineConfidence():

    errors = getErrorsForGaussian()

    kf = KFold(n_splits=5, shuffle=True, random_state=1234)

    gaussian_means = []

    gaussian_variances = []

    gaussian_lower_intervals = []

    gaussian_upper_intervals = []

    gaussian_accuracies = []

    mean_absolute_prediciton_errors = []

    root_mean_squared_absolute_prediction_errors = []

    for train_indices, test_indices in kf.split(errors):

        train_errors = errors.iloc[train_indices]

        test_errors = errors.iloc[test_indices]['error']

        # mean_train = train_errors['error'].mean()

        mean_train = np.average(train_errors['error'], weights=train_errors['recency'])

        # variance_train = train_errors['error'].var()

        variance_train = np.average((train_errors['error'] - mean_train)**2, weights=train_errors['recency'])

        sigma_train = math.sqrt(variance_train)

        interval2Deviation = (mean_train - 2*sigma_train, mean_train + 2*sigma_train)

        successes2Deviation = 0

        mean_absolute_prediction_errors_per_fold = []

        mean_squared_absolute_prediction_errors_per_fold = []

        tries = len(test_errors)

        for error in test_errors:
            mean_absolute_prediction_errors_per_fold.append(abs(error - mean_train))
            mean_squared_absolute_prediction_errors_per_fold.append((error-mean_train)**2)
            if interval2Deviation[0] <= error <= interval2Deviation[1]:
                successes2Deviation +=1

        gaussian_means.append(mean_train)
        gaussian_variances.append(variance_train)
        gaussian_lower_intervals.append(interval2Deviation[0])
        gaussian_upper_intervals.append(interval2Deviation[1])
        gaussian_accuracies.append(successes2Deviation / tries)
        mean_absolute_prediciton_errors.append(np.mean(mean_absolute_prediction_errors_per_fold))
        root_mean_squared_absolute_prediction_errors.append(np.sqrt(np.mean(mean_squared_absolute_prediction_errors_per_fold)))

    # print('mean of gaussians means: ' + str(np.mean(gaussian_means)))
    # print('mean of gaussian variances: ' + str(np.mean(gaussian_variances)))
    # print('mean lower bound: ' + str(np.mean(gaussian_lower_intervals)))
    # print('mean upper bound: ' + str(np.mean(gaussian_upper_intervals)))
    # print('bound size: ' + str(np.mean(gaussian_upper_intervals) - np.mean(gaussian_lower_intervals)))
    # print('mean accuracy: ' + str(np.mean(gaussian_accuracies)))
    # print('prediction error: ' + str(np.mean(prediciton_errors)))

    return (np.mean(gaussian_accuracies), np.mean(gaussian_upper_intervals) - np.mean(gaussian_lower_intervals), np.mean(mean_absolute_prediciton_errors), np.mean(root_mean_squared_absolute_prediction_errors))

# print(generateBaselineConfidence())

def confidenceWithFeatures(errors, features, deviation):

    kf = KFold(n_splits=5, shuffle=True, random_state=1234)

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


    for train_indices, test_indices in kf.split(errors):

        train_approaches = errors.iloc[train_indices]

        test_approaches = errors.iloc[test_indices]

        train_grouped = train_approaches.groupby(by=features)

        test_grouped = test_approaches.groupby(by=features)

        gaussian_means_per_fold = []
        gaussian_variances_per_fold = []
        gaussian_lower_intervals_per_fold = []
        gaussian_upper_intervals_per_fold = []
        gaussian_interval_size_per_fold = []
        gaussian_accuracies_per_fold = []
        gaussian_sample_sizes_per_fold = []

        gaussian_miss_counter = 0

        for group_name, group_data in train_grouped:

            # train_errors, test_errors = train_test_split(group_data['error'], test_size=0.2, random_state=1234)

            train_errors = group_data['error']

            try:
                test_errors = test_grouped.get_group(group_name)['error']

            except KeyError:
                gaussian_miss_counter += 1
                continue

            mean_train = train_errors.mean()

            # mean_train = np.average(group_data['error'], weights=group_data['recency'])

            if train_errors.shape[0] == 1:
                variance_train = 0
            else:
                variance_train = train_errors.var()
                # variance_train = np.average((group_data['error'] - mean_train)**2, weights=group_data['recency'])

            sigma_train = math.sqrt(variance_train)

            confidence_95_interval = (mean_train - deviation*sigma_train, mean_train + deviation*sigma_train)

            tries = len(test_errors)

            mean_absolute_prediction_errors_per_fold = []

            mean_squared_absolute_prediction_errors_per_fold = []

            successes = 0

            for error in test_errors:
                mean_absolute_prediction_errors_per_fold.append(abs(error - mean_train))
                mean_squared_absolute_prediction_errors_per_fold.append((error - mean_train)**2)
                if confidence_95_interval[0] <= error <= confidence_95_interval[1]:
                    successes += 1

            gaussian_means_per_fold.append(mean_train)
            gaussian_variances_per_fold.append(variance_train)
            gaussian_lower_intervals_per_fold.append(confidence_95_interval[0])
            gaussian_upper_intervals_per_fold.append(confidence_95_interval[1])
            gaussian_interval_size_per_fold.append(confidence_95_interval[1] - confidence_95_interval[0])
            gaussian_accuracies_per_fold.append(successes / tries)
            gaussian_sample_sizes_per_fold.append(len(train_errors))

        gaussian_means.append(np.mean(gaussian_means_per_fold))
        gaussian_variances.append(np.mean(gaussian_variances_per_fold))
        gaussian_lower_intervals.append(np.mean(gaussian_lower_intervals_per_fold))
        gaussian_upper_intervals.append(np.mean(gaussian_upper_intervals_per_fold))
        gaussian_interval_size.append(np.mean(gaussian_interval_size_per_fold))
        gaussian_accuracies.append(np.mean(gaussian_accuracies_per_fold))
        gaussian_sample_sizes.append(np.mean(gaussian_sample_sizes_per_fold))
        gaussian_misses.append(gaussian_miss_counter)
        mean_absolute_prediction_errors.append(np.mean(mean_absolute_prediction_errors_per_fold))
        root_mean_squared_absolute_prediction_errors.append(np.sqrt(np.mean(mean_squared_absolute_prediction_errors_per_fold)))

    # print('mean of gaussians means: ' + str(np.mean(gaussian_means)))
    # print('mean of gaussian variances: ' + str(np.mean(gaussian_variances)))
    # print('mean lower bound: ' + str(np.mean(gaussian_lower_intervals)))
    # print('mean upper bound: ' + str(np.mean(gaussian_upper_intervals)))
    # print('bound size: ' + str(np.mean(gaussian_upper_intervals) - np.mean(gaussian_lower_intervals)))
    # print('mean accuracy: ' + str(np.mean(gaussian_accuracies)))
    # print('Sample size: ' + str(np.mean(gaussian_sample_sizes)))
    # print('Misses: ' + str(np.mean(gaussian_misses)))
    # print('interval size:' + str(np.mean(gaussian_interval_size)))

    return (np.mean(gaussian_accuracies), np.mean(gaussian_upper_intervals) - np.mean(gaussian_lower_intervals), np.mean(gaussian_sample_sizes), np.mean(gaussian_misses), np.mean(mean_absolute_prediction_errors), np.mean(root_mean_squared_absolute_prediction_errors))

# print(confidenceWithFeatures(getErrorsForGaussian(), ['isWeekend'], 2))

def graphDifferentConfidences():
    array = np.arange(0.5, 3, 0.1)
    errors = getErrorsForGaussian()
    for deviation in array:
        accuracy, bound_size = confidenceWithFeatures(errors,['timeToStationSection'], deviation)
        print((accuracy, bound_size))

# graphDifferentConfidences()

def getBestGaussian():

    data = []

    features = ['dayOfWeek', 'isWeekend', 'partOfDay', 'stationName']

    combinations1 = itertools.combinations(features, 1)

    combinations2 = itertools.combinations(features, 2)

    combinations3 = itertools.combinations(features, 3)

    combinations4 = itertools.combinations(features, 4)

    # combinations5 = itertools.combinations(features, 5)

    allCombinations = list(combinations1) + list(combinations2) + list(combinations3) + list(combinations4)

    errors = getErrorsForGaussian()

    for combination in allCombinations:
        accuracy, bound_size, sample_size, misses, mean_absolute_error, mean_absolute_squared_error = confidenceWithFeatures(errors, list(combination), 2)
        data.append([list(combination), accuracy, bound_size, sample_size, misses, mean_absolute_error, mean_absolute_squared_error])

    gaussians_df = pd.DataFrame(data, columns=['features', 'accuracy', 'intervalSize', 'sampleSize', 'misses', 'meanAbsoluteError', 'meanAbsoluteSquaredError'])

    gaussians_df.to_csv('arrivals_208_outbound_gaussians.csv', index=False)

# getBestGaussian()

def generateTTSRangePerformance():

    data = []

    errors = getErrorsForGaussian()

    for i in range(5, 1800, 5):

        errors['timeToStationSection'] = errors['timeToStation'].apply(lambda x: x // i)

        intervalAccuracy, intervalRange, sampleSize, misses, meanAbsoluteError, rootMeanSquaredError = confidenceWithFeatures(errors, ['timeToStationSection'], 2)

        data.append([i, intervalAccuracy, intervalRange, meanAbsoluteError, rootMeanSquaredError])

    df_tts_range = pd.DataFrame(data, columns=['ttsSectionSize', 'intervalAccuracy', 'intervalRange', 'meanAbsoluteError', 'rootMeanSquaredError'])

    df_tts_range.to_csv('arrivals_208_outbound_tts_analysis.csv', index=False)

# generateTTSRangePerformance()

def lookupBestGaussian():

    pd.set_option('display.max_columns', None)

    data = pd.read_csv('arrivals_208_outbound_gaussians.csv')

    df_gaussians = pd.DataFrame(data)

    df_gaussians_only_better = df_gaussians.loc[df_gaussians['meanAbsoluteError'] < 1.8711392945798047]

    # df_gaussians_only_better.sort_values(by=['gaussianAccuracy'], ascending=False, inplace=True)

    print(df_gaussians_only_better)

lookupBestGaussian()

# showTTSRangesPerformance()

def getBestTTS():
    data = pd.read_csv('arrivals_208_outbound_tts_analysis.csv')

    df = pd.DataFrame(data)

    print(df.loc[df['meanAbsoluteError'].idxmin()])

    print(df.loc[df['rootMeanSquaredError'].idxmin()])

# getBestTTS()

def linearRegression():

    train, test = train_test_split(approaches_df, test_size=0.2)

    model = LinearRegression()

    X_train = train[['firstPredictionTime', 'lastPredictionTime', 'firstExpectedArrival', 'lastExpectedArrival', 'dayOfWeek', 'isWeekend', 'partOfDay']]

    y_train = train[['error']]

    model.fit(X_train, y_train)

    X_test = test[['firstPredictionTime', 'lastPredictionTime', 'firstExpectedArrival', 'lastExpectedArrival', 'dayOfWeek', 'isWeekend', 'partOfDay']]

    y_test = test[['error']]

    y_pred = model.predict(X_test)

    print(mean_squared_error(y_test, y_pred))

    print(mean_absolute_error(y_test, y_pred))

    # plt.scatter(X_test, y_test, color ='b')
    # plt.plot(X_test, y_pred, color ='k')
 
    # plt.show()

    # print(model.score(X_test, y_test))

    # importance = model.coef_

    # print(importance)

    # for i,v in enumerate(importance[0]):
	#     # print('Feature: %0d, Score: %.5f' % (i,v))
    #     plt.bar(i, v)
    
    # plt.bar([x for x in range(len(importance))], importance[0])

    # plt.show()

# linearRegression()

def decisionTree():
    model = DecisionTreeRegressor()

    train, test = train_test_split(approaches_df, test_size=0.2)

    X_train = train[['dayOfWeek', 'isWeekend', 'partOfDay']]

    y_train = train[['error']]

    model.fit(X_train, y_train)

    X_test = test[['dayOfWeek', 'isWeekend', 'partOfDay']]

    y_test = test[['error']]

    y_pred = model.predict(X_test)

    print(mean_squared_error(y_test, y_pred))

    print(mean_absolute_error(y_test, y_pred))

# decisionTree()