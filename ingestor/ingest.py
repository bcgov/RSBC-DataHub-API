from config import Config
import logging
from rabbitmq import RabbitMQ
from flask import request, jsonify, Response, json
from flask_api import FlaskAPI


application = FlaskAPI(__name__)
logging.warning('*** ingestor initialized ***')
rabbitmq = RabbitMQ( Config() )

# Create a queue for the messages Flask receives (if it doesn't already exist)
rabbitmq.verifyOrCreate(Config.RABBITMQ_QUEUE)


@application.route('/v1/publish/event', methods=["POST"])
def create():

    if(rabbitmq.publish( Config.RABBITMQ_QUEUE , json.dumps(request.json) )):

        return jsonify(request.json), 200
        
    else: 

        return Response( error , 500, mimetype='application/json')
    


if __name__ == "__main__":
    application.run(host='0.0.0.0')
    

