from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_restful import Api


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    api = Api(app)

    # Import and register routes
    from app.routes import main_routes, api_routes
    app.register_blueprint(main_routes.main_bp)
    api_routes.register_api_routes(api)  # Register API routes here

    # Debug: Print registered routes
    print("\nRegistered Routes:")
    print(app.url_map)

    return app
