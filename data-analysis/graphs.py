import pandas as pd
from preprocessing import toTimestamp
import matplotlib.pyplot as plt

plt.rcParams['savefig.dpi'] = 600

def featureUniqueness():
    data = pd.read_csv('arrivals_208_outbound/annotated_data.csv')

    df = pd.DataFrame(data)

    toTimestamp(df)

    hourValues = df['hour'].nunique()

    partOfDayValues = df['partOfDay'].nunique()

    dayOfWeekValues = df['dayOfWeek'].nunique()

    isWeekendValues = df['isWeekend'].nunique()

    stationNameValues = df['stationName'].nunique()

    timeToStationValues = df['timeToStation'].nunique()

    timeOfPredictionValues = df['timeOfPrediction'].nunique()

    # print(timeOfPredictionValues.mean())

    x = ['Hour', 'Part of Day', 'Day of Week', 'Is Weekend', 'Station Name', 'Time to Station', 'Time of Prediction']

    # y = [hourValues.mean(), partOfDayValues.mean(), dayOfWeekValues.mean(), isWeekendValues.mean(), stationNameValues.mean(), timeToStationValues.mean(), timeOfPredictionValues.mean()]

    y = [hourValues, partOfDayValues, dayOfWeekValues, isWeekendValues, stationNameValues, timeToStationValues, timeOfPredictionValues]

    bar_container = plt.bar(x, y)

    plt.bar_label(bar_container)

    plt.xlabel(xlabel='Feature')

    plt.ylabel(ylabel='Number of Unique Values')

    plt.title('Feature Uniqueness')

    plt.show()

featureUniqueness()