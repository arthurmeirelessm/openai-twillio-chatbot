import os
from flask import jsonify
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from PyPDF2 import PdfReader
import io

load_dotenv()


class ChromaRepository:
    def __init__(self):
        self.chroma_persistence_dir = os.getenv("CHROMA_PERSISTENCE_DIR")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.chroma_persistence_dir or not self.openai_api_key:
            raise ValueError(
                "CHROMA_PERSISTENCE_DIR ou OPENAI_API_KEY não configurados no .env"
            )

        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.chroma = Chroma(
            persist_directory=self.chroma_persistence_dir,
            embedding_function=self.embeddings,
        )

    def embeddings_content(self, file):
        try:
            pdf_reader = PdfReader(io.BytesIO(file))
            documents = []
            for page in pdf_reader.pages:
                documents.append(page.extract_text())
            text_splitter = CharacterTextSplitter(
                separator="\n", chunk_size=1024, chunk_overlap=128
            )
            texts = text_splitter.split_documents(documents)
            print(texts)
            persist_directory = "chroma_storage/"

            vectordb = self.chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                persist_directory=persist_directory,
            )

            vectordb.persist()

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def create_chain(self):
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        chain = ConversationChain(memory=memory, llm=self.embeddings)
        return chain
