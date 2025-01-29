from flask import Blueprint, request, jsonify
from ..controller.twillio_controller import TwillioController


class TwillioRoutes:
    def __init__(self):
        self.twillio_blueprint = Blueprint("twillio_routes", __name__)
        self.twillio_controller = TwillioController()
        self._register_routes()

    def _register_routes(self):
        self.twillio_blueprint.add_url_rule(
            "/chat",
            view_func=self.twillio_controller.call_OpenAI_chat_controller,
            methods=["POST"],
        )
