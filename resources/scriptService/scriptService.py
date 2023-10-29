import os
import subprocess
from pydub import AudioSegment
import json
import shutil
import tempfile

from pathlib import Path
import fastapi
import librosa
async def readRhubard(audio):
        # Ruta de la carpeta que deseas crear
        ruta_carpeta = "./uploads"

        # Verifica si la carpeta no existe y, en ese caso, créala
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
        
        save_path = f"./uploads/"
        
        with open(os.path.join(save_path, audio.filename), 'wb') as disk_file:
            file_bytes = await audio.read()

            disk_file.write(file_bytes)

            print(f"Received file named {audio.filename} containing {len(file_bytes)} bytes. ")
        # Realiza alguna operación con el archivo de audio
        # comando =  'C:/Users/User/Desktop/"cosas cristian"/"prueba Python"/resources/scriptService/rhubard/windows/rhubarb.exe -f json C:/Users/User/Desktop/"cosas cristian"/"prueba Python"/resources/uploads/{} s-o C:/Users/User/Desktop/"cosas cristian"/"prueba Python"/resources/uploads/{}.json'.format(audio.filename,audio.filename)
        comando =  'resources\\scriptService\\rhubard\\windows\\rhubarb.exe -f json  resources\\uploads\\{} -o resources\\uploads\\{}.json'.format(audio.filename,audio.filename)

        try:
            resultado = subprocess.run(comando, shell=True, check=True, text=True)
            print("La ejecución fue exitosa. Código de salida:", resultado.returncode)
        except subprocess.CalledProcessError as e:
            print("La ejecución falló. Código de salida:", e.returncode)
            
            
        # with open('{}.json'.format(audio.filename)) as fp:
        #     data = json.load(fp)
        #     print(data)
            # os.remove('{}.json'.format(audio.filename))
            # os.remove(audio.filename)
        # return data
   