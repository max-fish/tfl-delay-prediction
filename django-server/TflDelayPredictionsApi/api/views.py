from re import M

# import boto3
import json
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os

from api.blob_storage import uploadCsvFileToAzure
# dynamo_db = boto3.resource('dynamodb')

counter = 0

locked = False

requestCounter = 0

@csrf_exempt
def index(request):

    global requestCounter

    # table = dynamo_db.Table('test_arrival_predictions')
    
    # print(request.body)

    arrivalPredictions = request.body

    arrivalPredictionsDataFrame = pd.read_json(str(arrivalPredictions, 'UTF-8'))

    arrivalPredictionsDataFrame.drop(columns=['Timing'], inplace=True)

    # print(arrivalPredictionsDataFrame)

    global locked

    global counter

    while locked:
        time.sleep(1)

    locked = True

    print('Request Serviced: ' + str(requestCounter))

    requestCounter += 1

    outputPath = 'data_' + str(counter) + '.csv'

    if os.path.exists(outputPath):

        if os.path.getsize(outputPath) / 1000000 > 10:
            uploadCsvFileToAzure(outputPath)
            counter += 1
            outputPath = 'data_' + str(counter) + '.csv'
        

    arrivalPredictionsDataFrame.to_csv(outputPath, mode='a', index=False, header=not os.path.exists(outputPath))

    locked = False

    

    # fileObject = open('data_' + str(COUNTER) + '.csv', 'w')

    # if not fileObject.writable():
    #     fileObject.close()
    #     COUNTER += 1
    #     fileObject = open('data_' + str(COUNTER) + '.csv', 'w')

    # csvWriter = csv.writer(fileObject)


    # if not fileObject.readline():
    #     header = arrivalPredictionsJson[0].keys()
    #     csvWriter.writerow()

    #     fileObject.write(json.dumps(arrivalPredictionsJson))

    # fileObject.close()

    # with table.batch_writer() as batch:
    #     for prediction in arrivalPredictionsJson:
    #         batch.put_item(
    #             Item={
    #                 'prediction_id': prediction['Id'],
    #                 'timestamp': prediction['Timestamp'],
    #                 'operationType': prediction['OperationType'],
    #                 'vechicleId': prediction['VehicleId'],
    #                 'naptanId': prediction['NaptanId'],
    #                 'stationName': prediction['StationName'],
    #                 'lineId': prediction['LineId'],
    #                 'lineName': prediction['LineName'],
    #                 'platformName': prediction['PlatformName'],
    #                 'direction': prediction['Direction'],
    #                 'bearing': prediction['Bearing'],
    #                 'destinationNaptanId': prediction['DestinationNaptanId'],
    #                 'destinationName': prediction['DestinationName'],
    #                 'timeToStation': prediction['TimeToStation'],
    #                 'towards': prediction['Towards'],
    #                 'expectedArrival': prediction['ExpectedArrival'],
    #                 'timeToLive': prediction['TimeToLive'],
    #                 'modeName': prediction['ModeName']
    #             }
    #         )
#     table.put_item(
#    Item={
#         'prediction_id': '1202650361',
#         'timestamp': '2022-05-14T20:50:29.5044999Z',
#         'first_name': 'Jane',
#         'last_name': 'Doe',
#         'age': 25,
#         'account_type': 'standard_user',
#     }
# )
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")
# Create your views here.
