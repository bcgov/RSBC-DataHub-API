import python.common.helper as helper
from python.ingestor.config import Config
from python.common.rabbitmq import RabbitMQ
from python.common.message import Message
from flask import request, jsonify, Response
from flask_api import FlaskAPI
import xmltodict
import logging


application = FlaskAPI(__name__)
application.secret = Config.FLASK_SECRET_KEY
logging.basicConfig(level=Config.LOG_LEVEL)
logging.warning('*** ingestor initialized ***')

rabbit_mq = RabbitMQ(
        Config.RABBITMQ_USER,
        Config.RABBITMQ_PASS,
        Config.RABBITMQ_URL,
        Config.LOG_LEVEL,
        Config.MAX_CONNECTION_RETRIES,
        Config.RETRY_DELAY)

available_parameters = helper.load_json_into_dict('python/ingestor/' + Config.PARAMETERS_FILE)


@application.route('/v1/publish/event/<data_type>', methods=["POST"])
@application.route('/v1/publish/event', methods=["POST"])
def create(data_type='ETK'):

    if data_type not in available_parameters:
        warning_string = data_type + ' is a not a valid parameter'
        logging.warning(warning_string)
        return jsonify({"error": warning_string}), 500

    logging.debug('content-type: ' + request.content_type)
    if data_type == "ETK":
        payload = request.json
    elif data_type == "form":
        payload = {
            "event_version": "1.4",
            "encrypt_at_rest": available_parameters[data_type]['encrypt-at-rest'],
            "event_date_time": "",
            "event_type": "form_submission",
            "form_submission": xmltodict.parse(request.get_data())
        }
        logging.warning(request.get_data)

    if rabbit_mq.publish(available_parameters[data_type]['queue'], Message.encode_message(payload, Config.ENCRYPT_KEY)):
        return jsonify(payload), 200
    else:
        return Response('Unavailable', 500, mimetype='application/json')


if __name__ == "__main__":
    application.run(host='0.0.0.0')
