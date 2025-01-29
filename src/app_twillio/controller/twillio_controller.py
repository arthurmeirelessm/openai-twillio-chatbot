from flask import Blueprint, request, jsonify
from ..services.twillio_service import TwillioService


class TwillioController:
    def __init__(self):
        self.twillio_service = TwillioService()

    def call_OpenAI_chat_controller(self):
        body = request.form['Body'] 
        WaId = request.form['WaId']
        if body and WaId: 
            response = self.twillio_service.call_OpenAI_chat_service(WaId, body)
            return jsonify({"response": response}), 200
        else:
            return jsonify({"error": "Prompt field is missing"}), 400
