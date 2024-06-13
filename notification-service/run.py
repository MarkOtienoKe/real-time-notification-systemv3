from application import create_app, socketio
from application.consumer import get_kafka_consumer
from application.notification_api import process_event

app = create_app()

def start_kafka_consumer():
    consumer = get_kafka_consumer()
    for message in consumer:
        process_event(message.value)

if __name__ == '__main__':
    import threading
    threading.Thread(target=start_kafka_consumer).start()
    socketio.run(app, host='0.0.0.0', port=9113)
