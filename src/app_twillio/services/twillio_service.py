import os
import uuid
from twilio.rest import Client
from flask import request, jsonify
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.chat_message_histories.dynamodb import (
    DynamoDBChatMessageHistory,
)
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from dotenv import load_dotenv

load_dotenv()


class TwillioService:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.account_sid = os.getenv("ACCOUNT_SID_TWILLIO")
        self.auth_token_twillio = os.getenv("AUTH_TOKEN_TWILLIO")

        self.twillio_client = Client(self.account_sid, self.auth_token_twillio)
        self.llm = ChatOpenAI(
            model_name="gpt-4", 
            temperature=0.7, 
            max_tokens=500, 
            api_key=self.openai_key
        )
        self.dynamodb = boto3.resource('dynamodb').Table('ConversationalSessionTwillio')

    def get_or_create_session(self, recipient_number):
        # Verificar ou criar session_id no DynamoDB
        response = self.dynamodb.get_item(Key={'UserId': recipient_number})
        if 'Item' in response:
            return response['Item']['SessionId']
        else:
            new_session_id = str(uuid.uuid4())
            self.dynamodb.put_item(Item={'UserId': recipient_number, 'SessionId': new_session_id})
            return new_session_id

    def call_OpenAI_chat_service(self, recipient_number: str, body: str) -> str:
        session_id = self.get_or_create_session(recipient_number)
        
        # Carregar o histórico de chat
        chat_history = self.load_chat_history(session_id)
        
        # Chamada à LangChain com o histórico
        response = self.llm({"question": body, "chat_history": chat_history})
        
        # Atualizar o histórico no DynamoDB
        self.save_chat_history(session_id, chat_history)

        # Enviar resposta ao Twilio
        back_message_to_twillio = self.twillio_client.messages.create(
            from_="whatsapp:+14155238886", body=response['answer'], to=f'whatsapp:+{recipient_number}'
        )
        return str(back_message_to_twillio)
    
    def load_chat_history(self, session_id):
        # Carregar o histórico do DynamoDB
        response = self.dynamodb.get_item(Key={'SessionId': session_id})
        if 'Item' in response:
            return response['Item']['ChatHistory']
        return []

    def save_chat_history(self, session_id, chat_history):
        # Salvar o histórico de volta no DynamoDB
        self.dynamodb.put_item(Item={'SessionId': session_id, 'ChatHistory': chat_history})
