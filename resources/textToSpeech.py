import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from dotenv import load_dotenv
import requests
from fastapi.responses import FileResponse
import xml.etree.ElementTree as ET
load_dotenv()
speechKey = os.getenv('SPEECHKEY')
global infovisemes 
def getVisemes(visemes:str):
    infovisemes = visemes
    return visemes

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
        
        
def getAudioText(text: str, voice: str):

    speech_config = speechsdk.SpeechConfig(subscription=speechKey, region="westeurope")
    file_name = "outputaudio.wav"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    speech_config.speech_synthesis_voice_name = voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config = file_config)
    ssml = ssmlCreator(text,voice)
    visemes = []
    def viseme_cb(evt):
        # print("Viseme event received: audio offset: {}ms, viseme id: {}.".format(
        #     evt.audio_offset / 10000, evt.viseme_id))
        nonlocal visemes 
        visemes.append(evt.animation)
        
      
    
    
    speech_synthesizer.viseme_received.connect(viseme_cb)
    result = speech_synthesizer.speak_ssml_async(ssml).get()

    return "outputaudio.wav",visemes
    
## Utility
def ssmlCreator(text:str, voiceL:str):    
    return """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="es-ES">
            <voice name="{}">
               <mstts:viseme type="FacialExpression"/>
               {}
            </voice>
                </speak>""".format(voiceL, text)
   
   