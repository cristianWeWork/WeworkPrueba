import os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
conne_str = os.getenv('CONN_STRING_BLOB')
blob_service_client = BlobServiceClient.from_connection_string(str(conne_str))
container_name = "ia-tts-ww"
container_client = blob_service_client.get_container_client(container_name)

def upload_File(file, blob_name):
    blob_client = container_client.get_blob_client(blob_name)
     
    with open(file, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    return blob_client.url

