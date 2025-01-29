from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os

load_dotenv()


class ConversationHelper:
    def __init__(self):
        self.persist_directory = os.getenv("CHROMA_PERSISTENCE_DIR")
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.db = Chroma(
            persist_directory=self.persist_directory, embedding_function=self.embeddings
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=False
        )
        self.llm = ChatOpenAI()

        self.qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.db.as_retriever(),
            memory=self.memory,
            get_chat_history=lambda h: h,
            verbose=True,
        )

    def create_conversation(self) -> ConversationalRetrievalChain:
        return self.qa
