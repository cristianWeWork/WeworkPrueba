import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import requests

load_dotenv()
speechKey = os.getenv('SPEECHKEY')

# subscription_key = "a5701bbef60a46858ac7b4a270cf3507"
# fad*region = "e58fb2cda455475082827385d55192b3"
# speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
# audio_config = speechsdk.audio.AudioOutputConfig(filename="../download/file.wav")
# synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# texto_a_convertir = "Hola, esto es una prueba de conversión de texto a voz en Azure."

# audio_data = synthesizer.speak_text(texto_a_convertir)

def getVoicesList():
    requestUrl = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/voices/list"
    headers = {
        'Ocp-Apim-Subscription-Key': speechKey,
        'Content-type': 'application/json',
    
    }
    request: object = requests.get(requestUrl,  headers=headers)
    seen = set() 

    # never use list as a variable name
    if request.status_code == 200:
        # Obtener el contenido JSON de la respuesta
        response_data = request.json()

        # Asumiendo que response_data es una lista de diccionarios similar a tu ejemplo anterior
        # Usar una comprensión de lista para obtener los valores de 'LocaleName'
        locale_names = [item["LocaleName"] for item in response_data]

        # Imprimir el array resultante
        list_set = set(locale_names)
        result_list = list(list_set)
        result = sorted(result_list)
        return result
    else:
        print("La solicitud no fue exitosa. Código de estado:", request.status_code)
    
  