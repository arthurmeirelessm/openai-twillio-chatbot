from flask import Flask
from src.app_twillio.controller.twillio_controller import TwilioController


def create_app():
    app = Flask(__name__)
    twillio_controller = TwilioController()
    app.register_blueprint(twillio_controller.twillio_blueprint)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
