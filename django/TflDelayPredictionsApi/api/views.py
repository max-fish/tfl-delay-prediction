from django.http import HttpResponse
from django.shortcuts import render

import boto3

dynamo_db = boto3.resource('dynamodb')

def index(request):
    table = dynamo_db.Table('arrival_predictions')
    

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
