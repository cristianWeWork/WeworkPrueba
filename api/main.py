from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def prueba():
    return {"message": "Hello World"}


@app.get("/superhero/{superHero}")
async def superheroCall(superHero:str):
    frase = "Muy buenas, " + str(superHero).capitalize()
    
    return {"message" : str(frase)}