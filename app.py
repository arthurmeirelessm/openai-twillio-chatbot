from flask import Flask
from src.app_twillio.routes.twillio_routes import TwillioRoutes


def create_app():
    app = Flask(__name__)
    twillio_routes = TwillioRoutes()
    app.register_blueprint(twillio_routes.twillio_blueprint)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
