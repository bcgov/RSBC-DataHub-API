from keycloak import KeycloakOpenID
from python.common.config import Config
import requests
import json
import logging
from jinja2 import Environment, select_autoescape, FileSystemLoader

logging.basicConfig(level=Config.LOG_LEVEL)


def application_accepted(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    subject = 'Re: Driving Prohibition Review - Application Received  - {}'.format(prohibition_number)
    template = get_jinja2_env().get_template('application_accepted.html')
    return send_email(
        [args.get('applicant_email_address')],
        subject,
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def send_email_to_admin(**args):
    subject = args.get('subject')
    config = args.get('config')
    message = args.get('message')
    body = args.get('body')
    template = get_jinja2_env().get_template('admin_notice.html')
    return send_email(
        [config.ADMIN_EMAIL_ADDRESS],
        subject,
        config,
        template.render(subject=subject, body=body, message=json.dumps(message)),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_prohibition_served_more_than_7_days_ago(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    subject = 'Re: Driving Prohibition Review - 7-day Application Window Missed - {}'.format(prohibition_number)
    template = get_jinja2_env().get_template('application_not_received_in_time.html')
    return send_email(
        [args.get('applicant_email_address')],
        subject,
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_licence_not_seized(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    subject = 'Re: Driving Prohibition Review - Licence Not Returned - {}'.format(prohibition_number)
    template = get_jinja2_env().get_template('licence_not_seized.html')
    return send_email(
        [args.get('applicant_email_address')],
        subject,
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_prohibition_not_found(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    subject = 'Re: Driving Prohibition Review - Not Found - {}'.format(prohibition_number)
    template = get_jinja2_env().get_template('application_not_found.html')
    return send_email(
        [args.get('applicant_email_address')],
        subject,
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_to_schedule_review(**args):
    """
    This message is sent immediately after an applicant pays
    the application fee.  Since we don't have the driver's
    first name handy, this email is addressed to the applicant.
    """
    config = args.get('config')
    vips_application = args.get('vips_application')
    email_address = vips_application['email']
    full_name = "{} {}".format(vips_application['firstGivenNm'], vips_application['surnameNm'])
    prohibition_number = args.get('prohibition_number')
    subject = 'Re: Driving Prohibition Review - Select a Review Date - {}'.format(prohibition_number)
    template = get_jinja2_env().get_template('select_review_date.html')
    return send_email(
        [email_address],
        subject,
        config,
        template.render(
            full_name=full_name,
            prohibition_number=prohibition_number,
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_last_name_mismatch(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    subject = "Re: Driving Prohibition Review - Prohibition Number and Name Don't Match - {}".format(prohibition_number)
    template = get_jinja2_env().get_template('last_name_mismatch.html')
    return send_email(
        [args.get('applicant_email_address')],
        subject,
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_prohibition_not_yet_in_vips(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    subject = 'Re: Driving Prohibition Review - Not Entered Yet - {}'.format(prohibition_number)
    logging.info('Re: Driving Prohibition Review - Not Yet in VIPS')
    template = get_jinja2_env().get_template('application_not_yet_in_vips.html')
    return send_email(
        [args.get('applicant_email_address')],
        subject,
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def admin_unable_to_save_to_vips(**args) -> tuple:
    logging.critical('inside unable_to_save_to_vips_api()')
    config = args.get('config')
    message = args.get('message')
    subject = 'Critical Error: Unable to save to VIPS'
    body_text = 'While attempting to save an application to VIPS, an error was returned. ' + \
                'We will save the record to a failed write queue in RabbitMQ.'
    logging.critical('unable to save to VIPS: {}'.format(json.dumps(message)))
    return send_email_to_admin(config=config, subject=subject, body=body_text), args


def admin_unknown_event_type(**args) -> tuple:
    message = args.get('message')
    config = args.get('config')
    title = 'Critical Error: Unknown Event Type'
    body_text = "An unknown event has been received: " + message['event_type']
    logging.critical('unknown event type: {}'.format(message['event_type']))
    return send_email_to_admin(config=config, title=title, body=body_text), args


def send_email(to: list, subject: str, config, template, api_root_url: str, token: str) -> tuple:
    payload = {
        "bodyType": "html",
        "body": template,
        "from": config.REPLY_EMAIL_ADDRESS,
        "bcc": config.BCC_EMAIL_ADDRESSES.split(','),
        "encoding": "utf-8",
        "subject": subject,
        "to": to
    }
    logging.info('Sending email to: {} - {}'.format(to, subject))
    auth_header = {"Authorization": "Bearer {}".format(token)}
    try:
        response = requests.post(api_root_url + '/api/v1/email', headers=auth_header, json=payload)
    except AssertionError as error:
        logging.critical('No response from BC Common Services: {}'.format(json.dumps(error)))
        return False, error
    data = response.json()
    if response.status_code == 201:
        return True, data
    logging.info('response from common services: {}'.format(json.dumps(data)))
    return False, data


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
    template_loader = FileSystemLoader(searchpath="./python/common/templates")
    return Environment(
        loader=template_loader,
        autoescape=select_autoescape(['html', 'xml'])
    )
