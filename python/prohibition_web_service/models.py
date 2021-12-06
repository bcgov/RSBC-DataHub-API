from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()


class Form(db.Model):
    id = db.Column('id', db.String(20), primary_key=True)
    form_type = db.Column(db.String(20), nullable=False)
    lease_expiry = db.Column(db.Date, nullable=True)
    printed_timestamp = db.Column(db.DateTime, nullable=True)
    username = db.Column(db.String(25), nullable=True)

    def __init__(self, form_id, form_type, printed=None, lease_expiry=None, username=None):
        self.id = form_id
        self.form_type = form_type
        self.printed_timestamp = printed
        self.lease_expiry = lease_expiry
        self.username = username

    @staticmethod
    def serialize(form):
        return {
            "id": form.id,
            "form_type": form.form_type,
            "lease_expiry": Form._format_lease_expiry(form.lease_expiry),
            "printed_timestamp": form.printed_timestamp,
            "username": form.username
        }

    def lease(self, username):
        today = datetime.now()
        lease_expiry = today + timedelta(days=30)
        self.lease_expiry = lease_expiry
        self.username = username
        logging.info("{} leased {} until {}".format(
            self.username, self.id, self.lease_expiry.strftime("%Y-%m-%d")))

    @staticmethod
    def _format_lease_expiry(lease_expiry):
        if lease_expiry is None:
            return ''
        else:
            return datetime.strftime(lease_expiry, "%Y-%m-%d")

    @staticmethod
    def collection_to_dict(all_rows):
        result_list = []
        for row in all_rows:
            result_list.append(Form.serialize(row))
        return result_list


class UserRole(db.Model):
    role_name = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(25), primary_key=True)
    submitted_dt = db.Column(db.DateTime, nullable=True)
    approved_dt = db.Column(db.DateTime, nullable=True)

    def __init__(self, role_name, username, submitted_dt=None, approved_dt=None):
        self.role_name = role_name
        self.username = username
        self.submitted_dt = submitted_dt
        self.approved_dt = approved_dt

    @staticmethod
    def serialize(role):
        return {
            "role_name": role.role_name,
            "username": role.username,
            "submitted_dt": role.submitted_dt,
            "approved_dt": role.approved_dt
        }

    @staticmethod
    def collection_to_dict(all_rows):
        result_list = []
        for row in all_rows:
            result_list.append(UserRole.serialize(row))
        return result_list

    @staticmethod
    def collection_to_list_roles(all_rows):
        result_list = []
        for row in all_rows:
            result_list.append(row.role_name)
        return result_list

    @staticmethod
    def get_roles(username):
        rows = db.session.query(UserRole) \
            .filter(UserRole.username == username) \
            .filter(UserRole.approved_dt != None) \
            .all()
        return UserRole.collection_to_list_roles(rows)


