from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("<h1>Hello and welcome to my first <u>Django App</u> project!</h1>")
# Create your views here.
import pymongo
from django.conf import settings

connection_string = "mongodb+srv://gmnapster:Av2moULIATlLrfXb@cluster0.ibipj.mongodb.net/?retryWrites=true&w=majority"

my_client = pymongo.MongoClient(connection_string, ssl_cert_reqs=ssl.CERT_NONE)

# First define the database name
dbname = my_client['sample_medicines']

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection)
collection_name = dbname["medicinedetails"]

#let's create two documents
medicine_1 = {
    "medicine_id": "RR000123456",
    "common_name" : "Paracetamol",
    "scientific_name" : "",
    "available" : "Y",
    "category": "fever"
}
medicine_2 = {
    "medicine_id": "RR000342522",
    "common_name" : "Metformin",
    "scientific_name" : "",
    "available" : "Y",
    "category" : "type 2 diabetes"
}

collection_name.insert_many([medicine_1,medicine_2])

med_details = collection_name.find({})

for r in med_details:
	print(r["common_name"])

update_data = collection_name.update_one({'medicine_id':'RR000123456'}, {'$set':{'common_name':'Paracetamol 500'}})

count = collection_name.count()
print(count)

delete_data = collection_name.delete_one({'medicine_id':'RR000123456'})