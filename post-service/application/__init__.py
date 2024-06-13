from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer
from flask_swagger_ui import get_swaggerui_blueprint
from prometheus_flask_exporter import PrometheusMetrics

from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def create_app():
    app = Flask(__name__)
    metrics = PrometheusMetrics(app)

    # Configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    from .post_api import post_api_blueprint
    app.register_blueprint(post_api_blueprint, url_prefix='/api/v1')

    # Swagger UI setup
    SWAGGER_URL = '/api/docs'

    API_URL = '/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Post Service"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    @app.route('/swagger.json')
    def swagger_json():
        with open('swagger.json') as f:
            return jsonify(json.load(f))

    return app
