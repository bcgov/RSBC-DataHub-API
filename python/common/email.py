from keycloak import KeycloakOpenID
import requests
import json
import logging
from jinja2 import Environment, PackageLoader, select_autoescape


def invoice_to_applicant(**args):
    pass


def admin_unknown_event_type(**args):
    config = args.get('config')
    message = args.get('message')
    access_token = get_common_services_access_token(config)
    logging.warning('inside admin_unknown_event_type()')
    template = get_jinja2_env().get_template('admin_notice.html')
    title = 'Critical Error: Unknown Event Type'
    send_email(
        [config.ADMIN_EMAIL_ADDRESS],
        title,
        config.ADMIN_EMAIL_ADDRESS,
        template.render(title=title, event_type=message['event_type']),
        config.COMM_SERV_API_ROOT_URL,
        access_token)


def administrator(**args):
    config = args.get('config')
    access_token = get_common_services_access_token(config)
    template = "<h3>This is a test email</h3>"
    send_email(
        [config.ADMIN_EMAIL_ADDRESS],
        'TEST TEST',
        config.ADMIN_EMAIL_ADDRESS,
        template,
        config.COMM_SERV_API_ROOT_URL,
        access_token)


def send_email(to: list, subject: str, from_address: str, html_template, api_root_url: str, access_token: str) -> tuple:
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
        return False, error
    data = response.json()
    logging.warning('response from common services: {}'.format(json.dumps(data)))
    return True, data


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
