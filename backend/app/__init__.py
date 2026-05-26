from flask import Flask
from .database import init_db
from .middleware.auth import register_auth_middleware
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    init_db(app)
    register_auth_middleware(app)
    register_routes(app)

    return app
