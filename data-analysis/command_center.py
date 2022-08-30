import pandas as pd
from preprocessing import toTimestampAndSort, splitByApprachAndAddErrors
import time

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

start_time = time.time()

data = pd.read_csv('arrivals_208_outbound/data.csv')

df = pd.DataFrame(data)

toTimestampAndSort(df)

df['hour'] = df['timeOfPrediction'].apply(lambda x: x.hour)

df['partOfDay'] = df['timeOfPrediction'].apply(lambda x: getPartOfDay(x.hour))

df['dayOfWeek'] = df['timeOfPrediction'].apply(lambda x: x.day_of_week)

df['isWeekend'] = df['timeOfPrediction'].apply(lambda x: x.day_of_week >= 5)

splitByApprachAndAddErrors(df)

df.to_csv('arrivals_208_outbound/annotated_data.csv', index=False)

end_time = time.time()

print(end_time - start_time)