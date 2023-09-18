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
   
    if request.status_code == 200:
        response_data = request.json()
        locale_names = [item["LocaleName"] for item in response_data]

        # Imprimir el array resultante
        list_set = set(locale_names)
        result_list = list(list_set)
        result = sorted(result_list)
        return result
    else:
        print("La solicitud no fue exitosa. Código de estado:", request.status_code)
    

def getVoiceOptions(nationality: str):
    requestUrl = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/voices/list"
    headers = {
        'Ocp-Apim-Subscription-Key': speechKey,
        'Content-type': 'application/json',
    
    }
    request: object = requests.get(requestUrl,  headers=headers)
    print("Hola")
    if request.status_code == 200:
        response_data = request.json()
        resultados = [objeto for objeto in response_data if objeto["LocaleName"] == nationality]
        return resultados
    else:
        print("La solicitud no fue exitosa. Código de estado:", request.status_code)