from flask import Flask
from arjun_foodie_app.config import Config
from arjun_foodie_app.database_ext import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from arjun_foodie_app.foodie_routes import api_bp

    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True,port=5001)