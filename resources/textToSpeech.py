import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from dotenv import load_dotenv
import requests
from fastapi.responses import FileResponse
load_dotenv()
speechKey = os.getenv('SPEECHKEY')

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
    result = speech_synthesizer.speak_text_async(text).get()
    stream = speechsdk.AudioDataStream(result)
    file
    # return 


def speech_synthesis_to_wave_file():
    speech_config = speechsdk.SpeechConfig(subscription=speechKey, region="westeurope")
    file_name = "outputaudio.wav"
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Receives a text from console input and synthesizes it to wave file.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                
                
                
def speech_synthesis_to_mp3_file():

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # https://docs.microsoft.com/azure/cognitive-services/speech-service/rest-text-to-speech#audio-outputs
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    file_name = "outputaudio.mp3"
    file_config = speechsdk.audio.AudioOutputConfig()
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

    # Receives a text from console input and synthesizes it to mp3 file.
    while True:
        print("Enter some text that you want to synthesize, Ctrl-Z to exit")
        try:
            text = input()
        except EOFError:
            break
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))