from re import M
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 

# import boto3
import json
import pandas as pd
import os
# dynamo_db = boto3.resource('dynamodb')

COUNTER = 0

@csrf_exempt
def index(request):
    # table = dynamo_db.Table('test_arrival_predictions')
    
    # print(request.body)

    arrivalPredictions = request.body

    arrivalPredictionsDataFrame = pd.read_json(str(arrivalPredictions, 'UTF-8'))

    arrivalPredictionsDataFrame.drop(columns=['Timing'], inplace=True)

    # print(arrivalPredictionsDataFrame)

    outputPath = 'data_' + str(COUNTER) + '.csv'

    arrivalPredictionsDataFrame.to_csv(outputPath, mode='a', index=False, header=not os.path.exists(outputPath))

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
