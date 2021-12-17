from python.prohibition_web_svc.config import Config
from flask import request, make_response, Blueprint
from flask_cors import CORS
import logging.config



logging.config.dictConfig(Config.LOGGING)
logging.info('*** keycloak blueprint loaded ***')

bp = Blueprint('keycloak', __name__, url_prefix='/api/v1')
CORS(bp, resources={"/api/v1/keycloak": {"origins": Config.ACCESS_CONTROL_ALLOW_ORIGIN}})


@bp.route('/keycloak', methods=['GET'])
def index():
    """
    Keycloak config
    """
    if request.method == 'GET':
        config = {
            "realm": Config.KEYCLOAK_REALM,
            "url": Config.KEYCLOAK_AUTH_URL,
            "clientId": Config.KEYCLOAK_CLIENT_ID
        }
        return make_response(config, 200)

