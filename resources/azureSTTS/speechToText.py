import os
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechRecognizer, ResultReason,AudioConfig
import io
from azure.cognitiveservices.speech.audio import AudioOutputConfig, AudioOutputStream
from dotenv import load_dotenv
import requests
import datetime
import tempfile
import resources.database_dir.database_connections as bbdd
import resources.blob_storage.blob_functions as blobf
import resources.text_analytics.text_functions as txtf
load_dotenv()
speechKey = os.getenv('SPEECHSTTKEY')
speech_config = SpeechConfig(subscription=speechKey, region="westeurope")
speech_recognizer = SpeechRecognizer(speech_config=speech_config)

async def speechToText(audio):    
        with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio_file:
                temp_audio_file.write(audio)
                audio_path = temp_audio_file.name
    
       
        if os.path.exists(audio_path):
                with open(audio_path, "rb") as temp_file:
                        file_content = temp_file.read()

                if file_content:
                        # Add a check to make sure the file content is not empty
                        if len(file_content) > 0:
                                print(f"El archivo {audio_path} se creó correctamente y contiene contenido.")

                                audio_config = AudioConfig(filename=audio_path)
                                recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

                                # Recognize the speech
                                result = recognizer.recognize_once()

                        else:
                                print(f"El archivo {audio_path} se creó correctamente, pero está vacío.")

                else:
                        print(f"El archivo {audio_path} se creó correctamente, pero está vacío.")

        else:
                print(f"El archivo {audio_path} no se creó correctamente.")

        # Clean up the temporary audio file
        os.remove(audio_path)

        # return result



