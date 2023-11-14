import json
import time
from typing import List, Dict
import os
import openai
import PyPDF2
from io import BytesIO
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()
# openai.api_key = os.getenv('OPENAPI_KEY')

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
    print(text)
    return text

# async def chatingWithchatGpt(pdfFile, whoAmI):
#     pdf_Text = extract_text_from_pdf(pdfFile)

#     initial_context = f"El contenido del PDF es: {pdf_Text}"

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#          messages=[
#             {"role": "system", "content": whoAmI},
#             {"role": "user", "content": "Por favor, proporciona información sobre el tema."},
#             {"role": "assistant", "content": initial_context},
#         ],
#         # max_tokens=50,
#     )
    

#     return {"response": response}


# async def chatingContWithAi(messages : List[Message]):
#     response  = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#         )
#     print(response)
#     chat_response = response
#     return chat_response


# async def speechToText(audio):
#     transcript = openai.Audio.transcribe("whisper-1", audio)
#     return transcript


async def chatingContWithAi():
    assistant = client.beta.assistants.create(
    
        name="Sophie",
        instructions="You are a biologist",
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"},],
        model="gpt-4-1106-preview"
    )
    
    
    thread = client.beta.threads.create()
    
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role="user",
        content= "Necesito saber quien es el presidente de usa"
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account."
        )
    run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
            )
    messages = client.beta.threads.messages.list(
            thread_id=thread.id
            )
    lastMessageForRun = messages.data
    return lastMessageForRun


def createSessionThread():
    thread = client.beta.threads.create()
    return thread.id

def messagesFromGPT(assistant_id : str, thread_id : str, text : str):
    message = client.beta.threads.messages.create(
        thread_id = thread_id,
        role="user",
        content= text
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
        )
    print(run)
    print('-------------------')
    while (run.status != 'completed'):
        run = client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                    )
        
        time.sleep(2)
        print(run.status)
        print('-------------------')
        
    messages = client.beta.threads.messages.list(
                thread_id=thread_id
                )
    lastMessageForRun = messages.data
    finalData = lastMessageForRun[0].content[0].text.value  # type: ignore
    if "```json" in finalData:
        finalData_parsed = finalData.strip("```").strip("json")
        returnData = json.loads(finalData_parsed)
        return returnData
    else:
        return finalData
