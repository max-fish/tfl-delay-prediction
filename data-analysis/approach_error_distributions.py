import pandas as pd
from data_analysis import getErrorFromTTS
from preprocessing import toTimestamp
from sklearn.model_selection import train_test_split 
import numpy as np

def baseline():
    data = pd.read_csv('arrivals_208_outbound/annotated_data.csv')

    df = pd.DataFrame(data)

    # toTimestamp(df)

    station_data = df.loc[df['stationName'] == 'Morley Road']

    df_grouped_by_approaches = station_data.groupby(by=['approach_id'])

    approaches = list(df_grouped_by_approaches.groups)

    train_approach_groups, test_approach_groups = train_test_split(approaches, test_size=0.2, random_state=1234)

    train_errors = []

    for train_approach_group in train_approach_groups:
        train_approach_data = df_grouped_by_approaches.get_group(train_approach_group)

        onlyRangeTrain = train_approach_data.loc[(train_approach_data['timeToStation'] > 100) & (train_approach_data['timeToStation'] < 200)]

        train_errors.extend(onlyRangeTrain['error'])

    predictedError = np.mean(train_errors)

    modelErrors = []

    for test_approach_group in test_approach_groups:
        test_approach_data = df_grouped_by_approaches.get_group(test_approach_group)

        onlyRangeTest = test_approach_data.loc[(test_approach_data['timeToStation'] > 0) & (test_approach_data['timeToStation'] < 100)]

        for index, row in onlyRangeTest.iterrows():
            modelError = abs(row['error'] - predictedError)
            modelErrors.append(modelError)

    print(np.mean(modelErrors))

    print(np.var(modelErrors))

        

        
    
baseline()