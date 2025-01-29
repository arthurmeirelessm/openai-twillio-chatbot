import os
import uuid
from flask import request, jsonify
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.chat_message_histories.dynamodb import DynamoDBChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from dotenv import load_dotenv

load_dotenv()


class TwillioService:
    def __init__(self):
        # Inicializando a chave API do OpenAI
        self.openai_key = os.getenv("OPENAI_API_KEY")

        # Configurando o modelo LLM
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",  # Certifique-se de que o nome do modelo está correto
            temperature=0.7,
            max_tokens=500,
            api_key=self.openai_key,
        )

 
        self.session_id = str(uuid.uuid4()) 
        
        print(type(self.session_id))

        self.chat_history = DynamoDBChatMessageHistory(
            table_name="ConversationalSessionTwillio", 
            session_id=self.session_id,
        )

        # Configuração de memória com o histórico do DynamoDB
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            chat_memory=self.chat_history,
            return_messages=True
        )

        # Inicializando embeddings
        self.embeddings = OpenAIEmbeddings(api_key=self.openai_key)

        # Inicializando o banco de dados vetorial
        self.vector_db = Chroma(
            embedding_function=self.embeddings,
            collection_name="my_collection",
            persist_directory="./my_chroma_db",
        )

        # Inicializando o retriever com compressão contextual
        self.retriever = ContextualCompressionRetriever(
            base_compressor=LLMChainExtractor.from_llm(self.llm),
            base_retriever=self.vector_db.as_retriever(),
        )

        # Criando o template do prompt
        self.prompt_template = ChatPromptTemplate.from_template(
            """
            Context: {context}
            Chat History: {chat_history}
            Human: {question}
            AI: Please provide a relevant answer based on the context and chat history.
        """
        )

        # Criando o ConversationalRetrievalChain
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": self.prompt_template},
        )

    def call_OpenAI_chat_service(self, prompt: str) -> str:
        print(f"\n👤 Usuário: {prompt}")
        
        # Processa a resposta do modelo
        response = self.conversation_chain({"question": prompt})["answer"]
        return response