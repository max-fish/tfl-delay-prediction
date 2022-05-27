import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

def uploadCsvFileToAzure(file_name):
    try:
        print("Azure upload")

        blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=delaycsvstorage;AccountKey=prPXa/eMkACLn8RTMi9KgLQZSSVfXaQyP8bBTKZdrfIFKlSl2LmdmEXUjJDS71y7rI2aegJyq+It+AStwHg7pw==;EndpointSuffix=core.windows.net")
    
        blob_client = blob_service_client.get_blob_client(container="csv-files", blob=file_name)

        with open(file_name, "rb") as data:
            blob_client.upload_blob(data)

        os.remove(file_name)

    except Exception as ex:
        print('Exception:')
        print(ex)