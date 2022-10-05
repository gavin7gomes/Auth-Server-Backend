import json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from config import ApplicationConfig
from db import db

from security import authenticate, identity
from resources.user import UserList, UserRegister

from kafka import KafkaProducer

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

@app.route('/kafka', methods=['GET'])
def helloworld():
    SAMPLE_KAFKA_TOPIC = "sample_topic"

    producer = KafkaProducer(bootstrap_servers="192.168.2.8:29092")
    data = {
        "message": "Hello, Kafka!"
    }
    producer.send(SAMPLE_KAFKA_TOPIC, json.dumps(data).encode("utf-8"))

api.add_resource(UserRegister, "/register")
api.add_resource(UserList, "/users")

if __name__ == '__main__':
    db.init_app(app)
    app.run(host='127.0.0.1', port=5001, debug=False, threaded=True)