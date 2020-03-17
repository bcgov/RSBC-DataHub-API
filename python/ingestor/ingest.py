from config import Config
import logging
from common.rabbitmq import RabbitMQ
from flask import request, jsonify, Response, json
from flask_api import FlaskAPI


application = FlaskAPI(__name__)
logging.basicConfig(level=Config.LOG_LEVEL)
logging.warning('*** ingestor initialized ***')

rabbit_mq = RabbitMQ(
    Config.INGEST_USER,
    Config.INGEST_PASS,
    Config.RABBITMQ_URL,
    Config.LOG_LEVEL,
    Config.MAX_CONNECTION_RETRIES)

# Create a queue for the messages Flask receives (if it doesn't already exist)
rabbit_mq.verifyOrCreate(Config.WRITE_QUEUE)


@application.route('/v1/publish/event', methods=["POST"])
def create():
    if rabbit_mq.publish(Config.WRITE_QUEUE , json.dumps(request.json)):
        return jsonify(request.json), 200
    else:
        return Response( error , 500, mimetype='application/json')


if __name__ == "__main__":
    application.run(host='0.0.0.0')
