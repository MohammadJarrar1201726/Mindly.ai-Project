import os

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from azure.ai.textanalytics import TextAnalyticsClient

def connect_document_intelligence_service() -> DocumentAnalysisClient:
    """
    Connect to document intelligence service.

    This function handles importing environment variables and create a connection with
    DocumentAnalysisClient service, and returs the resultant clinet object.

    Returns:
    - DocumentAnalysisClient object
    """
    endpoint = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
    key = os.getenv("DOC_INTELLIGENCE_KEY")

    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    return document_analysis_client


def connect_open_ai_service() -> AzureOpenAI:
    """
    Connect to OpenAi service.

    This function handles importing environment variables and create a connection with
    OpenAi service, and returs the resultant clinet object.

    Returns:
    - AzureOpenAI object
    """
    return AzureOpenAI(
        api_version=os.getenv("OPEN_AI_API_VERSION"),
        azure_endpoint=os.getenv("OPEN_AI_AZURE_ENDPOINT"),
        api_key=os.getenv("OPEN_AI_API_KEY"),
    )


def connect_open_ai_chatbot() -> AzureOpenAI:
    """
    Connect to OpenAi Chatbot.

    This function handles importing environment variables and create a connection with
    OpenAi chatbot, and returs the resultant clinet object.

    Returns:
    - AzureOpenAI object
    """

    return AzureOpenAI(
        api_key=os.getenv("OPEN_AI_CHAT_BOT_API_KEY"),
        api_version=os.getenv("OPEN_AI_CHAT_BOT_API_VERSION"),
        azure_endpoint=os.getenv("OPEN_AI_CHAT_BOT_ENDPOINT"),
    )

def connect_language_services() -> TextAnalyticsClient:
    # Azure Form Recognizer endpoint and key
    endpoint = os.getenv("LANGUAGE_RESOURCE_ENDPOINT")
    key = os.getenv("LANGUAGE_RESOURCE_KEY")

    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    return text_analytics_client