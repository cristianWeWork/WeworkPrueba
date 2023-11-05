
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
import PyPDF2
from io import BytesIO
import os
import resources.blob_storage.blob_functions as blobf

import names
openai_api_key = os.getenv('OPENAPI_KEY')

def extract_text_from_pdf(pdf_content):
    pdf = pdf_content.file.read()
    
    # Crear un objeto BytesIO y escribir los bytes del PDF en él
    pdf_stream = BytesIO(pdf)
    
    # Crear un objeto PdfReader de PyPDF2 usando el objeto BytesIO
    pdf_reader = PyPDF2.PdfReader(pdf_stream)
    
    texts = []
    for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                texts.append(text)
    return texts

def vectorEmbeddingResponse(vectordb, query):
    
    qa = VectorDBQA.from_chain_type(llm=OpenAI(openai_api_key=openai_api_key), chain_type="stuff", vectorstore=vectordb)
    response = qa.run(query)
    
    return response


async def chatingWithLLM(pdfFile):
    pdf_Text = extract_text_from_pdf(pdfFile)
    name = names.get_full_name()
    persist_directory = name

    embeddings = OpenAIEmbeddings(openai_api_key =openai_api_key)
    vectordb = Chroma.from_texts(pdf_Text, embeddings, persist_directory=persist_directory)
    blobf.
    query = "Hazme un resumen del texto."
    response = vectorEmbeddingResponse(vectordb, query)
    vectordb.persist()
    vectordb = None
    return {"response": response, "name" : name}

async def stillChatingWithLLM(query, name):
    
    embeddings = OpenAIEmbeddings(openai_api_key =openai_api_key)
    vectordb = Chroma(persist_directory=name, embedding_function=embeddings)
    response = vectorEmbeddingResponse(vectordb, query)
    

    return {"response": response}