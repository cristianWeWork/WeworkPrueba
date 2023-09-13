# import requests, uuid, json
# import os
# from dotenv import load_dotenv


# translatorEndpoint = "https://api.cognitive.microsofttranslator.com"
# translatorLocation = "westeurope"

# load_dotenv()
# translatorKey = os.getenv('TRANSLATORKEY')


# path = '/translate'
# constructed_url = translatorEndpoint + path

# params = {
#     'api-version': '3.0',
#     'to': ['fr', 'en']
# }

# headers = {
#     'Ocp-Apim-Subscription-Key': translatorKey,
#     # location required if you're using a multi-service or regional (not global) resource.
#     'Ocp-Apim-Subscription-Region': translatorLocation,
#     'Content-type': 'application/json',
#     'X-ClientTraceId': str(uuid.uuid4())
# }

# def funcionTraduccion(texto: str) :    
#     body = [{
#         'text': texto
#     }]
#     request = requests.post(constructed_url, params=params, headers=headers, json=body)
#     response = request.json()
#     return response
    