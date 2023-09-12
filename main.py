from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    user: str
    name: str | None = None


@app.get("/")
async def prueba():
    return {"message": "Hello World"}

@app.post("/user/")
async def create_item(item: Item):
    frase = "Muy buenas, " + str(item.name) + ", tu nombre de usuario es: " + str(item.user)
    return {"message": frase}
    
@app.get("/superhero/{superHero}")
async def superheroCall(superHero:str):
    frase = "Muy buenas, " + str(superHero).capitalize()
    
    return {"message" : str(frase)}

if __name__ == '__main__':
    uvicorn.run('myapp:app', host='0.0.0.0', port=8000)

