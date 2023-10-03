from logging.config import dictConfigClass
from fastapi import FastAPI, Form, Request, status, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Any, Dict, List, Annotated
import uvicorn
from pydantic import BaseModel
from resources import translatorApp
from resources.textToSpeech import getVoicesList, getVoiceOptions, getAudioText
import os
from fastapi.middleware.cors import CORSMiddleware
import resources.database_dir.database_connections as bbdd
import resources.chatgpy as chatai

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

def get_streamed_ai_response(response):
    for chunk in response: 
        yield chunk['choices'][0]['delta'].get("content", "")


class Item(BaseModel):
    user: str
    name: str | None = None

class itemTranslated(BaseModel):
    text: str

class itemToSpeech(BaseModel):
    text:str
    voice: str
    language:str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "voz": "es-CU-BelkysNeural",
                    "text":"Muy buenas, Bienvenidos a los juegos del hambre",
                    "idioma": "Spanish (Cuba)",
                }
            ]
        }
    }
class AIobject(BaseModel):
    voz:str
    text: str
    idioma:str
    format: str
    url_audio: str
    feelings: str
    blendShapes: str
    visemes: str
class Message(BaseModel):
    role: str
    content: str

    
@app.get("/")
async def  welcomeToNightCity():
    return {"text": "Hola NightCity"}
    
@app.post("/translateMe/")
async def translateFunction(itemTranslated: itemTranslated):
    text = itemTranslated.text
    return translatorApp.funcionTraduccion(text)

@app.get("/getVoicesList/")
async def textToSpeech():
    print("Hola")
    return getVoicesList()
    
@app.get("/getVoiceFindDetails/")
async def getVoiceDetail(nationality: str) -> list:
    return getVoiceOptions(nationality)
    
@app.post("/SpeechToText/")
async def getTextToSpeech(item :itemToSpeech) :
    query = {
        "voz": item.voice,
        "text": item.text
    }
    result = bbdd.find_document(query)
    if result == None:
        url_audio = await getAudioText(item.text, item.voice, item.language)
        response = {
            "url_audio" : url_audio
        }
        return response
    else:
        
        response = {
            "url_audio" : result['url_audio'],
            
        }
        
        return response
         

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

@app.post("/message")
async def chatingWithAi(pdf_file:  Annotated[UploadFile, File()], whoAmI: Annotated[str, "Quien soy?"] = Form(...)):
    
    response = await chatai.chatingWithchatGpt(pdf_file, whoAmI)

    return response

@app.post("/ContinueMessage")
async def chatingContWithAi(request: Request):
    data = await request.json()
    print(data)
    response = await chatai.chatingContWithAi(data)

    return response

if __name__ == '__main__':
    uvicorn.run('myapp:app', host='0.0.0.0', port=8000)

