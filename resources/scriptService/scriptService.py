import os
import subprocess
from pydub import AudioSegment
import json
import shutil
import tempfile

import platform
from pathlib import Path
import fastapi
import librosa

#Sistema Operativo en el que estamos
sistema = platform.system()

async def readRhubard(audio_data, audio):
        # Ruta de la carpeta que deseas crear
        ruta_carpeta = "./uploads"

        # Verifica si la carpeta no existe y, en ese caso, créala
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
        
        save_path = f"./uploads/"
        
        with open(os.path.join(save_path, audio.filename), 'wb') as disk_file:
            disk_file.write(audio_data)

            print(f"Received file named {audio.filename} containing {len(audio_data)} bytes. ")
        if sistema == "Windows": 
            # comando Windows
            comando =  'resources\\scriptService\\rhubard\\windows\\rhubarb.exe -f json  uploads\\{} -o uploads\\{}.json'.format(audio.filename,audio.filename)
            # comando Linux
        else :
            comando = './resources/scriptService/rhubard/Linux/rhubarb.exe -f json  ./uploads/{} -o ./uploads/{}.json'.format(audio.filename,audio.filename)
        checkpoint = True 
        try:
            if (len(audio_data) > 0):
                resultado = subprocess.run(comando, shell=True, check=True, text=True)
                checkpoint = False
                print("La ejecución fue exitosa. Código de salida:", resultado.returncode)
        except subprocess.CalledProcessError as e:
            print("La ejecución falló. Código de salida:", e.returncode)
            
            
        with open('./uploads/{}.json'.format(audio.filename)) as fp:
            data = json.load(fp)
            print(data)
            
        return data
    
def borradoDeAudio(audio):
    os.remove('./uploads/{}.json'.format(audio.filename))
    os.remove('./uploads/{}'.format(audio.filename))
        
        