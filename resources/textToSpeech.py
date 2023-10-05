import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig, AudioOutputStream
from dotenv import load_dotenv
import requests
import datetime
import resources.database_dir.database_connections as bbdd
import resources.blob_storage.blob_functions as blobf
import resources.text_analytics.text_functions as txtf
load_dotenv()
speechKey = os.getenv('SPEECHKEY')

date = datetime.datetime.now()


def getVisemes(visemes: str):
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
        resultados = [
            objeto for objeto in response_data if objeto["LocaleName"] == nationality]
        return resultados
    else:
        print("La solicitud no fue exitosa. Código de estado:", request.status_code)
        return []


async def getAudioText(text: str, voice: str, language: str):
    aos = AudioOutputStream(None)
    speech_config = speechsdk.SpeechConfig(
        subscription=speechKey, region="westeurope")
    file_name = "outputaudio.wav"
    file_config = speechsdk.audio.AudioOutputConfig(
        filename=file_name)  # type: ignore
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=file_config)
    speech_config.speech_synthesis_voice_name = voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=file_config)
    ssml = ssmlCreator(text, voice)
    blendShapes = []
    visemes = []
    feelings = txtf.readFelings(text)
    def viseme_cb(evt):
        # print("Viseme event received: audio offset: {}ms, viseme id: {}.".format(
        #     evt.audio_offset / 10000, evt.viseme_id))
        nonlocal blendShapes, visemes
        visemes.append({"audio_offsett": evt.audio_offset /
                       10000, "viseme_id": evt.viseme_id})
        blendShapes.append(evt.animation)

    speech_synthesizer.viseme_received.connect(viseme_cb)
    result = speech_synthesizer.speak_ssml_async(ssml).get()
    data = {
        "voz": voice,
        "text": text,
        "idioma": language,
        "format": "text",
        "url_audio": "",
        "sentiments": { "sentiment":feelings.sentiment, "sentiment_score": {"positive":feelings.confidence_scores.positive,"negative":feelings.confidence_scores.negative,"neutral":feelings.confidence_scores.neutral} }, # type: ignore
        "blendShapes": blendShapes,
        "visemes": visemes,
        "created_at": date
    }
    
    id = bbdd.insert_document(data)
    
    url_audio =  blobf.upload_File("outputaudio.wav", "{}.wav".format(id))
    
    bbdd.update_url_audio({"_id" : id}, {"url_audio": url_audio})
    
    return url_audio,  str(id)

# Utility


def ssmlCreator(text: str, voiceL: str):
    return """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="es-ES">
            <voice name="{}">
               <mstts:viseme type="FacialExpression"/>
               {}
            </voice>
                </speak>""".format(voiceL, text)
