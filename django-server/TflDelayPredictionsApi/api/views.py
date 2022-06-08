from re import M
from datetime import datetime
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os

from api.blob_storage import uploadCsvFileToAzure
# dynamo_db = boto3.resource('dynamodb')

locked = False

date_time_obj = datetime.now()

timestamp_string = date_time_obj.strftime("%d-%b-%Y (%H:%M:%S)")

@csrf_exempt
def index(request):

    # table = dynamo_db.Table('test_arrival_predictions')
    
    # print(request.body)

    arrivalPredictions = request.body

    arrivalPredictionsDataFrame = pd.read_json(str(arrivalPredictions, 'UTF-8'))

    arrivalPredictionsDataFrame.drop(columns=['Timing'], inplace=True)

    global locked

    while locked:
        time.sleep(1)

    locked = True

    global timestamp_string
    
    outputPath = 'data_' + timestamp_string + '.csv'

    if os.path.exists(outputPath):

        if os.path.getsize(outputPath) / 1000000 > 193:
            uploadCsvFileToAzure(outputPath)
            date_time_obj = datetime.now()
            timestamp_string = date_time_obj.strftime("%d-%b-%Y_%H:%M:%S")
            outputPath = 'data_' + timestamp_string + '.csv'
        

    arrivalPredictionsDataFrame.to_csv(outputPath, mode='a', index=False, header=not os.path.exists(outputPath))

    locked = False
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")

