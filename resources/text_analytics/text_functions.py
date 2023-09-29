import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Configura las credenciales
key = os.getenv('TEXT_ANALY_KEY')  # Reemplaza con tu clave de API
endpoint = "https://text-analytics-ww.cognitiveservices.azure.com/"  # Reemplaza con tu punto de enlace

# Inicializa el cliente de Text Analytics
credential = AzureKeyCredential(str(key))
text_analytics_client = TextAnalyticsClient(endpoint, credential)


def readFelings(text):
    print(text)
    resultado = text_analytics_client.analyze_sentiment([text])
    for documento in resultado:
        print("Texto analizado:", documento)
        print("Sentimiento:", documento.sentiment)
        print("Puntuación del sentimiento positivo:", documento.confidence_scores.positive)
        print("Puntuación del sentimiento neutral:", documento.confidence_scores.neutral)
        print("Puntuación del sentimiento negativo:", documento.confidence_scores.negative)
        return documento