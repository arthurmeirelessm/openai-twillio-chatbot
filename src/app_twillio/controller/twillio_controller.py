from flask import Blueprint
from ..services.twillio_service import TwillioService


class TwilioController:
    def __init__(self):
        self.twillio_blueprint= Blueprint("twilio_controller", __name__)
        self.twillio_service = TwillioService()
        self._register_routes()

    def _register_routes(self):
        """
        Registra as rotas no blueprint.
        """
        self.twillio_blueprint.add_url_rule(
            "/", view_func=self.twillio_service.get_users, methods=["GET"]
        )
        self.twillio_blueprint.add_url_rule(
            "/message", view_func=self.twillio_service.send_message, methods=["POST"]
        )
        self.twillio_blueprint.add_url_rule(
            "/train", view_func=self.twillio_service.train_chroma, methods=["POST"]
        )
        self.twillio_blueprint.add_url_rule(
            "/agent", view_func=self.twillio_service.call_OpenAI_Agent, methods=["POST"]
        )
