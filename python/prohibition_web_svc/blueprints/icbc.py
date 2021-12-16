from python.prohibition_web_svc.config import Config
import python.prohibition_web_svc.business.icbc_logic as rules
from python.common.helper import middle_logic
from flask import request, Blueprint
from flask_cors import CORS
import logging.config

logging.config.dictConfig(Config.LOGGING)
logging.info('*** icbc blueprint loaded ***')

bp = Blueprint('icbc', __name__, url_prefix='/api/v1/icbc')
CORS(bp, resources={"/api/v1/icbc/*": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/drivers/<string:dl_number>', methods=['GET'])
def get_driver(dl_number):
    if request.method == 'GET':
        kwargs = middle_logic(rules.get_driver(),
                              required_permission='driver-get',
                              dl_number=dl_number,
                              request=request,
                              config=Config)
        return kwargs.get('response')


@bp.route('/vehicles/<string:plate_number>', methods=['GET'])
def get_vehicle(plate_number):
    if request.method == 'GET':
        kwargs = middle_logic(rules.get_vehicle(),
                              required_permission='vehicle-get',
                              plate_number=plate_number.upper(),
                              request=request,
                              config=Config)
        return kwargs.get('response')

