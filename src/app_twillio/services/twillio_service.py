from flask import jsonify, request
from twilio.twiml.messaging_response import MessagingResponse
from ..repository.chroma_db import ChromaRepository
from ..helper.conversation import ConversationHelper


class TwillioService:
    def __init__(self):
        self.chroma_repository = ChromaRepository()
        self.qa = ConversationHelper()

    def get_users(self) -> str:
        """
        Retorna u status básico.
        """
        return jsonify({"Status": 200})

    def send_message(self) -> str:
        """
        Endpoint para receber mensagens do Twilio e responder.
        """
        incoming_msg = request.form.get("Body")
        from_number = request.form.get("From")

        try:
            res = self.qa.create_conversation(
                {"question": incoming_msg, "chat_history": {}}
            )
            response = MessagingResponse()
            response.message(res)
            return str(response)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def train_chroma(self):
        file = request.data
        if not file:
            return jsonify({"error": "Nenhum arquivo enviado."}), 400

        try:
            self.chroma_repository.embeddings_content(file)
            return jsonify({"message": "Documents added successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    
    def call_OpenAI_Agent(self, prompt: str) -> str: 
        try:
             
        except Exception as e: 
            