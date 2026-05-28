from flask import Flask
from .database import init_db
from .middleware.auth import register_auth_middleware
from .routes import register_routes
from .config import Config

def create_app():
    from flask_cors import CORS

    app = Flask(__name__)
    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(Config)  # load directly, no string import needed

    init_db(app)
    register_auth_middleware(app)
    register_routes(app)

    return app
