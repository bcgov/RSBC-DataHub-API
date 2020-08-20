from keycloak import KeycloakOpenID
import requests
import json
import logging
from jinja2 import Environment, PackageLoader, select_autoescape


def application_received(**args):
    config = args.get('config')
    message = args.get('message')
    subject = 'Re: Driving Prohibition Review - Approved'
    template = get_jinja2_env().get_template('application_approved.html')
    return send_email(
        [get_email_address(message)],
        subject,
        config.REPLY_EMAIL_ADDRESS,
        template.render(
            full_name=get_full_name(message),
            prohibition_number=get_prohibition_number(message),
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def send_email_to_admin(**args):
    title = args.get('title')
    config = args.get('config')
    message = args.get('message')
    body = args.get('body')
    template = get_jinja2_env().get_template('admin_notice.html')
    return send_email(
        [config.ADMIN_EMAIL_ADDRESS],
        title,
        config.REPLY_EMAIL_ADDRESS,
        template.render(subject=title, body=body, message=json.dumps(message)),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_prohibition_served_more_than_7_days_ago(**args):
    config = args.get('config')
    message = args.get('message')
    subject = 'Re: Driving Prohibition Review - Expired'
    template = get_jinja2_env().get_template('application_not_received_in_time.html')
    return send_email(
        [get_email_address(message)],
        subject,
        config.REPLY_EMAIL_ADDRESS,
        template.render(
            full_name=get_full_name(message),
            prohibition_number=get_prohibition_number(message),
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_licence_not_seized(**args):
    # TODO - write method
    logging.critical('message not implemented')
    return True, args


def applicant_prohibition_not_found(**args):
    config = args.get('config')
    message = args.get('message')
    subject = 'Re: Driving Prohibition Review - Not Found'
    template = get_jinja2_env().get_template('application_not_found.html')
    return send_email(
        [get_email_address(message)],
        subject,
        config.REPLY_EMAIL_ADDRESS,
        template.render(
            full_name=get_full_name(message),
            prohibition_number=get_prohibition_number(message),
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_prohibition_not_yet_in_vips(**args):
    # TODO - write method
    logging.critical('message not implemented')
    return True, args


def send_email(to: list, subject: str, from_address: str, html_template, api_root_url: str, access_token: str) -> bool:
    payload = {
        "bodyType": "html",
        "body": html_template,
        "from": from_address,
        "encoding": "utf-8",
        "subject": subject,
        "to": to
    }
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    try:
        response = requests.post(api_root_url + '/api/v1/email', headers=auth_header, json=payload)
    except AssertionError as error:
        logging.critical('No response from BC Common Services: {}'.format(json.dumps(error)))
        return False
    data = response.json()
    logging.warning('response from common services: {}'.format(json.dumps(data)))
    return "msgId" in data['messages'][0]


def get_common_services_access_token(config):
    # Configure Keycloak client
    keycloak_openid = KeycloakOpenID(server_url=config.COMM_SERV_AUTH_URL,
                                     client_id=config.COMM_SERV_CLIENT_ID,
                                     realm_name=config.COMM_SERV_REALM,
                                     client_secret_key=config.COMM_SERV_CLIENT_SECRET)
    # Get Token
    token = keycloak_openid.token('', '', 'client_credentials')
    return token['access_token']


def get_jinja2_env():
    return Environment(
        loader=PackageLoader('python', 'common/templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )


def get_email_address(message: dict) -> str:
    event_type = message['event_type']
    return message[event_type]['form']['identification-information']['driver-email-address']


def get_full_name(message: dict) -> str:
    event_type = message['event_type']
    first_name = message[event_type]['form']['identification-information']['driver-first-name']
    last_name = message[event_type]['form']['identification-information']['driver-last-name']
    return "{} {}".format(first_name, last_name)


def get_prohibition_number(message: dict) -> str:
    event_type = message['event_type']
    return message[event_type]['form']['prohibition-information']['control-prohibition-number']