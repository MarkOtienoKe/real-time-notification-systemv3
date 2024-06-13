from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_login import LoginManager
from prometheus_flask_exporter import PrometheusMetrics

from dotenv import load_dotenv
import os
import json 

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    print(os.getenv('APP_SECRET_KEY'))
    app.secret_key = os.getenv('APP_SECRET_KEY')
    metrics = PrometheusMetrics(app)

    # Config from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from .user_api import user_api_blueprint
    app.register_blueprint(user_api_blueprint, url_prefix='/api/v1')

    # Swagger UI setup
    SWAGGER_URL = '/api/docs'
    API_URL = '/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "User Service"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    @app.route('/swagger.json')
    def swagger_json():
        with open('swagger.json') as f:
            return jsonify(json.load(f))

    return app
