from python.prohibition_web_service.config import Config
from flask import request, Blueprint, send_from_directory
import logging.config

logging.config.dictConfig(Config.LOGGING)
logging.info('*** static assets blueprint loaded ***')

bp = Blueprint('static_assets', __name__)

TEMPLATE_PATH = "./python/prohibition_web_service/templates/"


@bp.route('/css/<path:name>', methods=['GET'])
def css(name):
    """
    Make available CSS assets
    """
    if request.method == 'GET':
        logging.warning("inside css()")
        return send_from_directory('templates/assets/bootstrap-4.6.0-dist/css', name, as_attachment=True)

