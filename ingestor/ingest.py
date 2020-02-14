from config import Config
import logging
from rabbitmq import RabbitMQ
from flask import request, jsonify, Response, json
from flask_api import FlaskAPI


application = FlaskAPI(__name__)
rabbitmq = RabbitMQ( Config() )
logging.warning('*** ingestor initialized ***')   

# Create the queues, if they don't already exist
authorizedQueues = Config.RABBITMQ_QUEUES.split(',')
for authorizedQueue in authorizedQueues:
    rabbitmq.verifyOrCreate(authorizedQueue)


@application.route('/api/v1/event/<queue>', methods=["POST"])
def create(queue):

    if(queue not in authorizedQueues):
        return Response( "Error_" + queue + "_not_valid" , 500, mimetype='application/json')


    if(rabbitmq.publish( queue , json.dumps(request.json) )):

        return jsonify(request.json), 200
        
    else:

        # Caution: RabbitMQ will only return false if the RabbitMQ is not
        # connected. If the queue doesn't exist, for example, RabbitMQ
        # accepts the message and immediately discards it.

        return Response( error , 500, mimetype='application/json')
    


if __name__ == "__main__":
    application.run(host='0.0.0.0')
    

