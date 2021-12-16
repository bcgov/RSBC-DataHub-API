from flask_api import FlaskAPI
import logging
from datetime import datetime
from python.prohibition_web_svc.models import db, Form, UserRole
from python.prohibition_web_svc.config import Config
from python.prohibition_web_svc.blueprints import impound_lot_operators, jurisdictions, forms, admin_forms, agencies
from python.prohibition_web_svc.blueprints import provinces, countries, cities, colors, vehicles, icbc, keycloak
from python.prohibition_web_svc.blueprints import vehicle_styles, user_roles, admin_user_roles, admin_users


application = FlaskAPI(__name__)
application.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
application.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

application.register_blueprint(admin_forms.bp)
application.register_blueprint(admin_user_roles.bp)
application.register_blueprint(admin_users.bp)
application.register_blueprint(agencies.bp)
application.register_blueprint(cities.bp)
application.register_blueprint(colors.bp)
application.register_blueprint(countries.bp)
application.register_blueprint(forms.bp)
application.register_blueprint(icbc.bp)
application.register_blueprint(impound_lot_operators.bp)
application.register_blueprint(jurisdictions.bp)
application.register_blueprint(keycloak.bp)
application.register_blueprint(provinces.bp)
application.register_blueprint(user_roles.bp)
application.register_blueprint(vehicle_styles.bp)
application.register_blueprint(vehicles.bp)


db.init_app(application)


def create_app():
    with application.app_context():
        logging.warning('inside create_app()')
        initialize_app(application)
        return application


def initialize_app(app):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables_and_seed():
        engine = db.get_engine()
        tables = db.inspect(engine).get_table_names()
        if len(tables) == 0:
            logging.warning('Sqlite database does not exist - creating new file')
            db.create_all()
            _seed_forms_for_development(db)
            seed_initial_administrator(db)
        else:
            logging.info("database already exists - no need to recreate")


def _seed_forms_for_development(database):
    # TODO - Remove before flight
    seed_records = []
    prefix = ["J", "V", "40", "22"]
    for idx, form_type in enumerate(["12Hour", "24Hour", "IRP", "VI"]):
        for x in range(100000, 100100):
            unique_id = '{}-{}'.format(prefix[idx], str(x))
            seed_records.append(Form(
                form_id=unique_id,
                form_type=form_type))
    database.session.bulk_save_objects(seed_records)
    database.session.commit()
    logging.warning("seed temporary unique form_ids")
    return


def seed_initial_administrator(database):
    current_dt = datetime.now()
    users = [
        UserRole(username=Config.ADMIN_USERNAME, role_name='officer', submitted_dt=current_dt, approved_dt=current_dt),
        UserRole(username=Config.ADMIN_USERNAME, role_name='administrator', submitted_dt=current_dt, approved_dt=current_dt)
    ]
    database.session.bulk_save_objects(users)
    database.session.commit()
    logging.warning("seed initial administrator: " + Config.ADMIN_USERNAME)
    return
