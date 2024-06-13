from flask import Blueprint
from . import socketio, redis_client

notification_api_blueprint = Blueprint('notification_api', __name__)

def process_event(event):
    if event['type'] == 'post_created':
        notify_message = f"New post created by user {event['user_id']}: {event['content']}"
        redis_client.lpush('notifications', notify_message)
        socketio.emit('new_notification', {'message': notify_message}, room='')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
