from bson import ObjectId
from fastapi import Body, Cookie, FastAPI, Form, HTTPException, Query, Request, status, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse,StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Any, Dict, List, Annotated, Optional
import uvicorn
from pydantic import BaseModel, Field
from resources.azureSTTS import translatorApp
from resources.azureSTTS.textToSpeech import getVoicesList, getVoiceOptions, getAudioText
# from resources.azureSTTS.speechToText import speechToText
from fastapi.middleware.cors import CORSMiddleware
import resources.database_dir.database_connections as bbdd
import resources.chatWithMe.chatgpy as chatai
import resources.chatWithMe.embbedingChat as chatEm
from resources.scriptService.scriptService import borradoDeAudio, readRhubard



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
    name: str 
class itemTranslated(BaseModel):
    text: str

class chattingWithEmb(BaseModel):
    name: str
    query:str
class chattingGPTNew(BaseModel):
    assistant_id: str
    thread_id:str
    text: str

class itemToSpeech(BaseModel):
    text:str
    voice: str
    language:str
    format: Optional[str] = "wav"
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "voice": "es-CU-BelkysNeural",
                    "text":"Muy buenas, Bienvenidos a los juegos del hambre",
                    "language": "Spanish (Cuba)",
                    "format": "ogg"
                }
            ]
        }
    }
class AIobject(BaseModel):
    voz:str
    text: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    idioma:str| None = Field(
        default=None, title="The description of the item", max_length=300
    )
    format: str| None = Field(
        default=None, title="The description of the item", max_length=300
    )
    url_audio: str| None = Field(
        default=None, title="The description of the item", max_length=300
    )
    feelings: str| None = Field(
        default=None, title="The description of the item", max_length=300
    )
    blendShapes: str| None = Field(
        default=None, title="The description of the item", max_length=300
    )
    visemes: str| None  = Field(
        default=None, title="The description of the item", max_length=300
    )

class AIqueryobject(BaseModel):
    id:str

   
    
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
    
@app.post("/textToSpeech/")
async def getTextToSpeech(item :itemToSpeech) :
    
    query = {
        "voz": item.voice,
        "text": item.text,
        "format": item.format
    }
    result = bbdd.find_document(query)
    print(result)
    
    if result == None:
        url_audio, id = await getAudioText(item.text, item.voice, item.language, item.format) # type: ignore
        response = {
            "url_audio" : url_audio,
            "id" : id
        }
        return response
    else:
        
        response = {
            "url_audio" : result['url_audio'],
            "id" : result['_id'],
        }
        return response
         

@app.get("/getDBName")
async def getDBName():
    return bbdd.showDBlist()
    
@app.post("/insert/")
async def insertIntoDB(object: AIobject):
    return bbdd.insert_document(object)

@app.post("/query/")
async def getFromDB(request_data : AIqueryobject = Body(...)):
    _id = request_data.id
    
    if not _id:
        raise HTTPException(status_code=400, detail="Los campos 'voz' son obligatorios")

    result = bbdd.find_document({"_id": ObjectId(_id)})
    
    return result


@app.post("/update/")
async def updateIntoDB(query, object: AIobject):
    return bbdd.update_document(query, object)

@app.post("/delete/")
async def deleteFromDB(query):
    return bbdd.delete_document(query)

@app.post("/message")
async def chatingWithAi():
    
    response =  await chatai.chatingContWithAi()

    return response

@app.post("/ContinueMessage")
async def chatingContWithAi(request: Request):
    data = await request.json()
    print(data)
    # response = await chatai.chatingContWithAi(data)

    # return response

@app.post("/messageEmb")
async def chatingWithLLM(pdf_file:  UploadFile):
    
    response = await chatEm.chatingWithLLM(pdf_file)

    return response

@app.post("/ContinueMessageEmb")
async def ContinueMessageEmb(request: chattingWithEmb):
   
    print(request)
    response = await chatEm.stillChatingWithLLM(request.query, request.name)

    return response

# @app.post("/speechToText/")
# async def speechText(audio: Annotated[UploadFile, File()]):    
#     audio_data = await audio.read()
    
#     response = await speechToText(audio_data)

@app.post("/rhubardTranslate/")
async def rhubard(audio: UploadFile): 
    try:
        audio_data = await audio.read()
        response = await readRhubard(audio_data, audio)
        borradoDeAudio(audio)
        return JSONResponse(response)
    except ConnectionError as e:
        with open('./uploads/error.json') as fp:
                data = fp.write(str(e))
                print(data)
            
    
@app.get("/getSessionThread")
async def getSessionThread(request_id: str = Cookie(None)):
    print(request_id)
    return chatai.createSessionThread()    
    
@app.post("/chatNewGPT")
async def getMessages(request: chattingGPTNew):
    
    return chatai.messagesFromGPT(request.assistant_id,request.thread_id, request.text)
    
    
    
    
    
    
if __name__ == '__main__':
    uvicorn.run('myapp:app', host='0.0.0.0', port=8000)

