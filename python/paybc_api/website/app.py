import time
import logging
from flask import Flask
from python.paybc_api.website.models import db, User, OAuth2Client
from python.paybc_api.website.oauth2 import config_oauth
from python.paybc_api.website.routes import bp
from python.paybc_api.website.config import Config


def create_app(config=Config):
    app = Flask(__name__)

    # Set the secret key to some random bytes
    app.secret_key = config.PAYBC_FLASK_SECRET

    # load app specified configuration
    app.config.update(
        OAUTH2_REFRESH_TOKEN_GENERATOR=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='sqlite:////{}/{}'.format(config.ABSOLUTE_DB_PATH, config.DB_NAME)
    )

    setup_app(app, config)
    return app


def setup_app(app, config):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables_and_seed():
        engine = db.get_engine()
        # If the database is deleted and recreated it will cause a delay until the
        # access token provided to PayBC expires and a new token is requested.
        tables = db.inspect(engine).get_table_names()
        if len(tables) == 0:
            logging.warning('Sqlite database does not exist - creating new file')
            db.create_all()
            user = User(username=config.OAUTH2_USER)
            db.session.add(user)

            client_id_issued_at = int(time.time())
            client = OAuth2Client(
                client_id=config.PAYBC_CLIENT_ID,
                client_id_issued_at=client_id_issued_at,
                user_id=user.id,
            )

            client.client_secret = config.PAYBC_CLIENT_SECRET

            client_metadata = {
                "client_name": 'test_client',
                "grant_types": "client_credentials",
                "token_endpoint_auth_method": "client_secret_basic"
            }
            client.set_client_metadata(client_metadata)
            db.session.add(client)
            db.session.commit()
        else:
            logging.warning("database already exists - no need to recreate")

    db.init_app(app)
    config_oauth(app)
    app.register_blueprint(bp, url_prefix='')
