import certifi
import google.generativeai as genai

from flask import Flask, current_app, jsonify
from flask_cors import CORS
from mongoengine import connect, disconnect, get_connection
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
from werkzeug.exceptions import RequestEntityTooLarge
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from dotenv import load_dotenv

flask_bcrypt = Bcrypt()
jwt = JWTManager()
load_dotenv()


def create_app(config_object="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    with app.app_context():
        socketio = SocketIO(
            cors_allowed_origins=current_app.config["FRONTEND_URL"],
            async_mode="threading",
        )
        CORS(
            app,
            resources={
                r"/*": {
                    "origins": [
                        current_app.config["FRONTEND_URL"],
                        "http://localhost:5173",
                    ]
                }
            },
        )

        try:
            connect(
                db=current_app.config["MONGO_DB"],
                host=current_app.config["MONGO_HOST"],
                port=current_app.config["MONGO_PORT"],
                serverSelectionTimeoutMS=5000,
                tls=True,
                tlsCAFile=certifi.where(),
            )
            client = get_connection()
            client.admin.command("ping")
            app.logger.info("✅ MongoDB connection established")
        except (ServerSelectionTimeoutError, ConfigurationError) as exc:
            app.logger.critical("❌ MongoDB connection failed: %s", exc)
            disconnect()
            raise

        try:
            genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
            app.logger.info("✅ Gemini (Generative AI) initialized successfully")
            app.gemini = genai
        except Exception as e:
            app.logger.critical("❌ Gemini initialization failed: %s", e)
            raise

    from .routes.auth import auth
    from .routes.groups import groups
    from .routes.memberships import memberships
    from .routes.channels import channels
    from .routes.messages import messages

    app.register_blueprint(auth, urlprefix="/")
    app.register_blueprint(groups, urlprefix="/")
    app.register_blueprint(memberships, urlprefix="/")
    app.register_blueprint(channels, urlprefix="/")
    app.register_blueprint(messages, urlprefix="/")

    flask_bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        return jsonify({"err": "Payload too large"}), 413

    from .services.message_handler import on_join, on_leave

    return app
