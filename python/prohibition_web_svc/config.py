import os
from python.common.config import Config as BaseConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(BaseConfig):
    FLASK_SECRET_KEY                    = os.getenv('FLASK_SECRET_KEY')

    FLASK_BASIC_AUTH_USER               = os.getenv('FLASK_BASIC_AUTH_USER')
    FLASK_BASIC_AUTH_PASS               = os.getenv('FLASK_BASIC_AUTH_PASS')

    ICBC_API_ROOT                       = os.getenv('ICBC_API_ROOT', "http://localhost:8080/api")
    ICBC_API_USERNAME                   = os.getenv('ICBC_API_USERNAME', 'user1')
    ICBC_API_PASSWORD                   = os.getenv('ICBC_API_PASSWORD', 'secret')

    # URL of requesting resource
    ACCESS_CONTROL_ALLOW_ORIGIN         = os.getenv('ACCESS_CONTROL_ALLOW_ORIGIN', '*')

    DATABASE_URI                        = os.getenv('DATABASE_URI', 'sqlite:///:memory:')

    # This user has the ability to add, edit and delete other users
    ADMIN_USERNAME                      = os.getenv('ADMIN_USERNAME')

    KEYCLOAK_REALM                      = os.getenv("KEYCLOAK_REALM", "some-realm")
    KEYCLOAK_AUTH_URL                   = os.getenv("KEYCLOAK_AUTH_URL", "http://localhost/auth/")
    KEYCLOAK_CLIENT_ID                  = os.getenv("KEYCLOAK_CLIENT_ID", 'my-client')
    KEYCLOAK_ALGORITHM                  = os.getenv("KEYCLOAK_ALGORITHM", "RS256")

    KEYCLOAK_CERTS_URL = "{}realms/{}/protocol/openid-connect/certs".format(KEYCLOAK_AUTH_URL, KEYCLOAK_REALM)

    URL_PREFIX                          = os.getenv('URL_PREFIX', '')

    MAX_RECORDS_RETURNED = 200


