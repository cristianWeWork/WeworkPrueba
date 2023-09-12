from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel
from resources import translatorApp


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    user: str
    name: str | None = None

class itemTranslated(BaseModel):
    text: str
    
    
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
    

if __name__ == '__main__':
    uvicorn.run('myapp:app', host='0.0.0.0', port=8000)

