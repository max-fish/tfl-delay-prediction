import pandas as pd
from route_splitting import perBusPerStationSplitting

def toTimestamp(df):
    df['timeOfPrediction'] = df['timeOfPrediction'].apply(lambda x: pd.to_datetime(x.split(".")[0]))

    df['expectedArrival'] = df['expectedArrival'].apply(lambda x: pd.to_datetime(x.split(".")[0]))

    # df['actualArrival'] = df['actualArrival'].apply(lambda x: pd.to_datetime(x.split(".")[0]))

def toTimestampAndSort(df):
    df['timeOfPrediction'] = df['timeOfPrediction'].apply(lambda x: pd.to_datetime(x.split(".")[0]))

    df['expectedArrival'] = df['expectedArrival'].apply(lambda x: pd.to_datetime(x.split(".")[0]))

    # df['actualArrival'] = df['actualArrival'].apply(lambda x: pd.to_datetime(x.split(".")[0]))

    df.sort_values(by=['timeOfPrediction'], inplace=True)

    df = df.reset_index(drop=True)

def sortByTimeOfPrediction(df):
    df['timeOfPrediction'] = df['timeOfPrediction'].apply(lambda x: pd.to_datetime(x.split(".")[0]))

    df.sort_values(by=['timeOfPrediction'], inplace=True)

    df = df.reset_index(drop=True)

def splitByApproach(df):
    perBusPerStationSplitting(df)

def splitByApprachAndAddErrors(df):

    perBusPerStationSplitting(df)

    df_group_by_approach = df.groupby(by=['approach_id'])

    for name, group in df_group_by_approach:
        lastExpectedArrival = group.iloc[-1]['expectedArrival']
        for i in range(0, group.shape[0]):
            currentPrediction = group.iloc[i]
            currentExpectedArrival = currentPrediction['expectedArrival']
            currentIndex = currentPrediction.name

            error = (lastExpectedArrival - currentExpectedArrival).total_seconds() / 60

            df.loc[currentIndex, 'error'] = error

            df.loc[currentIndex, 'actualArrival'] = lastExpectedArrival

# def addRecencyInMinutes(df):

def addActualArrivalTime(df):

    sortByTimeOfPrediction(df)

    df_group_by_approach = df.groupby(by=['approach_id'])

    for name, group in df_group_by_approach:
        lastExpectedArrival = group.iloc[-1]['expectedArrival']

        for i in range(0, group.shape[0]):
            currentPrediction = group.iloc[i]
            currentIndex = currentPrediction.name

            df.loc[currentIndex, 'actualArrival'] = lastExpectedArrival