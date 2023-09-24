from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
from resources import translatorApp
from resources.textToSpeech import getVoicesList, getVoiceOptions, getAudioText
import os
from fastapi.middleware.cors import CORSMiddleware
import resources.database.database_connections as bbdd
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    user: str
    name: str | None = None

class itemTranslated(BaseModel):
    text: str

class itemToSpeech(BaseModel):
    text:str
    voice: str
    
class AIobject(BaseModel):
    voz:str
    text: str
    idioma:str
    format: str
    url_audio: str
    feelings: str
    blendShapes: str
    visemes: str
    
@app.get("/")
async def prueba():
    return {"message": "Hola NightCity"}

@app.post("/user/")
async def create_item(item: Item):
    frase = "Muy buenas, " + str(item.name) + ", tu nombre de usuario es: " + str(item.user)
    return {"message": frase}
    
@app.get("/superhero/{superHero}")
async def superheroCall(superHero:str):
    frase = "Muy buenas, " + str(superHero).capitalize()
    
    return {"message" : str(frase)}

@app.get("/user/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

@app.post("/translateMe/")
async def translateFunction(itemTranslated: itemTranslated):
    text = itemTranslated.text
    return translatorApp.funcionTraduccion(text)

@app.get("/getVoicesList/")
async def textToSpeech():
    print("Hola")
    return getVoicesList()
    
@app.get("/getVoiceFindDetails/")
async def getVoiceDetail(nationality: str):
    return getVoiceOptions(nationality)
    
@app.post("/SpeechToText/")
async def getTextToSpeech(item :itemToSpeech):
    archivo_audio, visemes = getAudioText(item.text, item.voice)
    response = FileResponse(archivo_audio)
    response.headers["data"] = str(visemes)
    print(visemes)
    return {"data":visemes}

@app.get("/getDBName")
async def getDBName():
    return bbdd.showDBlist()
    
@app.post("/insert/")
async def insertIntoDB(object: AIobject):
    return bbdd.insert_document(object)

@app.get("/query/")
async def getFromDB(object: AIobject):
    return bbdd.find_document(object)

@app.post("/update/")
async def updateIntoDB(query, object: AIobject):
    return bbdd.update_document(query, object)

@app.post("/delete/")
async def deleteFromDB(query):
    return bbdd.delete_document(query)



if __name__ == '__main__':
    uvicorn.run('myapp:app', host='0.0.0.0', port=8000)

