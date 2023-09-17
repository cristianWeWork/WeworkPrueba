import os
import azure.cognitiveservices.speech as speechsdk

subscription_key = "a5701bbef60a46858ac7b4a270cf3507"
region = "e58fb2cda455475082827385d55192b3"
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
audio_config = speechsdk.audio.AudioOutputConfig(filename="../download/file.wav")
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

texto_a_convertir = "Hola, esto es una prueba de conversión de texto a voz en Azure."

audio_data = synthesizer.speak_text(texto_a_convertir)

