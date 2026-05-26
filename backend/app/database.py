from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()

def init_db(app):
    """Initialize the DB engine and create tables if they don't exist."""
    db.init_app(app)
    with app.app_context():
        try:
            from . import models  # Ensure models are imported so metadata is registered
            db.create_all()
        except SQLAlchemyError as exc:
            app.logger.error(f"Database init failed: {exc}")
            raise
