from flask import Blueprint, request, jsonify
from ..services.twillio_service import TwillioService


class TwillioController:
    def __init__(self):
        self.twillio_service = TwillioService()

    def call_OpenAI_chat_controller(self):
        data = request.get_json()  
        prompt = data.get("prompt") 
        print(prompt)
        if prompt: 
            response = self.twillio_service.call_OpenAI_chat_service(prompt)
            return jsonify({"response": response}), 200
        else:
            return jsonify({"error": "Prompt field is missing"}), 400
