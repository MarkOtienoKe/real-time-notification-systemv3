from flask import Flask
from dotenv import load_dotenv
from flask_socketio import SocketIO
import redis
import os

# Load environment variables from .env file
load_dotenv()

socketio = SocketIO(async_mode='eventlet', cors_allowed_origins="*")
redis_client = redis.StrictRedis(
    host=os.getenv('REDIS_HOST'), 
    port=os.getenv('REDIS_PORT'), 
    db=os.getenv('REDIS_DB')
)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    socketio.init_app(app)

    from .notification_api import notification_api_blueprint
    app.register_blueprint(notification_api_blueprint, url_prefix='/api/v1')

    return app
