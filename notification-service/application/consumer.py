from kafka import KafkaConsumer
import json
import os

def get_kafka_consumer():
    return KafkaConsumer(
        'post-events',
        bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='notification-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
