# Real-Time Notification System

## Overview
This project is a real-time notification system that integrates a user service, post service, and notification service. The system utilizes Kafka for message brokering, Redis for data storage, Flask-SocketIO for real-time communication, and Grafana for monitoring.

## Features
- **User Service**: Manages user profiles and authentication.
- **Post Service**: Handles posts, likes, and comments.
- **Notification Service**: Listens to post events and notifies clients via WebSocket.
- **Monitoring**: Integrated Grafana for monitoring system metrics.

## Architecture
- **Backend**: Flask
- **Real-time Communication**: Flask-SocketIO
- **Message Broker**: Kafka
- **Data Storage**: Redis
- **Monitoring**: Grafana

## Prerequisites
- Python 3.11
- Docker
- Docker Compose

## Setup Instructions

### 1. Clone the Repository
```sh
git clone git remote add origin git@github.com:MarkOtienoKe/real-time-notification-system.git
cd real-time-notification-system
docker-compose up --build

### Start Services
docker-compose up

### Stop Services
docker-compose down

###API Endpoint
- For User service access Swagger using
http://127.0.0.1:9111/api/docs/

- For Post Service  access swagger using
http://127.0.0.1:9112/api/docs/

- For notification service use
http://127.0.0.1:9113/api/v1

WebSocket Endpoint: ws://127.0.0.1:9113/api/v1/socket.io/


