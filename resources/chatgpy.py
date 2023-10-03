from fastapi import FastAPI
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
import os
import openai
from fastapi.responses import StreamingResponse
import PyPDF2
from io import BytesIO

from pydantic import BaseModel

openai.api_key = os.getenv('OPENAPI_KEY')

def get_streamed_ai_response(response):
    for chunk in response: 
        yield chunk['choices'][0]['delta'].get("content", "")

class Message(BaseModel):
    role: str
    content: str

    
def extract_text_from_pdf(pdf_content):
    pdf = pdf_content.file.read()
    
    # Crear un objeto BytesIO y escribir los bytes del PDF en él
    pdf_stream = BytesIO(pdf)
    
    # Crear un objeto PdfReader de PyPDF2 usando el objeto BytesIO
    pdf_reader = PyPDF2.PdfReader(pdf_stream)
    
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    return text

async def chatingWithchatGpt(pdfFile, whoAmI):
    pdf_Text = extract_text_from_pdf(pdfFile)

    initial_context = f"El contenido del PDF es: {pdf_Text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
         messages=[
            {"role": "system", "content": whoAmI},
            {"role": "user", "content": "Por favor, proporciona información sobre el tema."},
            {"role": "assistant", "content": initial_context},
        ],
        # max_tokens=50,
    )
    

    return {"response": response}


async def chatingContWithAi(messages : List[Message]):
    response  = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

    chat_response = response

    return chat_response