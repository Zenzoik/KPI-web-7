from pathlib import Path

from flask import Flask
from flask_migrate import Migrate

from app.config import DevelopmentConfig
from app.database import db
from app.extensions import login_manager
from app.routes import register_routes
from app.seed import seed_database

migrate = Migrate()


def create_app(config_class=DevelopmentConfig):
    base_dir = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static"),
    )
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    register_routes(app)

    with app.app_context():
        db.create_all()
        seed_database()

    return app
