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
    t = "application_accepted.html"
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
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


def send_form_xml_to_admin(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    subject = 'DEBUG - Form XML attached - {}'.format(prohibition_number)
    template = get_jinja2_env().get_template('admin_notice.html')
    return send_email(
        [config.ADMIN_EMAIL_ADDRESS],
        subject,
        config,
        template.render(
            body='XML attached',
            message='message xml attached',
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config),
        [{
            "content": args.get('xml'),
            "contentType": "string",
            "encoding": "base64",
            "filename": "submitted_form.xml"
        }]), args


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
    t = "application_not_received_in_time.html"
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
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
    t = "licence_not_seized.html"
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
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
    t = "application_not_found.html"
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
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
    t = 'select_review_date.html'
    email_address = vips_application['email']
    full_name = "{} {}".format(vips_application['firstGivenNm'], vips_application['surnameNm'])
    prohibition_number = args.get('prohibition_number')
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
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


def applicant_schedule_confirmation(**args):
    """
    This message is sent to the applicant after the requested review date
    is successfully saved to VIPS.
    """
    config = args.get('config')
    vips_application = args.get('vips_application')
    email_address = vips_application['email']
    presentation_type = vips_application['presentationTypeCd']
    t = 'review_date_confirmed_{}.html'.format(presentation_type)
    phone = vips_application['phoneNo']
    prohibition_number = args.get('prohibition_number')
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return send_email(
        [email_address],
        subject,
        config,
        template.render(
            full_name=args.get('applicant_name'),
            prohibition_number=prohibition_number,
            subject=subject,
            phone=phone,
            human_friendly_time_slot=args.get('friendly_review_time_slot')),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config)), args


def applicant_last_name_mismatch(**args):
    """
    This email is sent to the applicant if the last name entered by the applicant
    does not match the last name of the driver as entered in VIPS
    """
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = 'last_name_mismatch.html'
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
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
    t = 'application_not_yet_in_vips.html'
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
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


def application_already_created(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = 'application_already_created.html'
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
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


def applicant_disclosure(**args) -> tuple:
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = 'send_disclosure_documents.html'
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return send_email(
        [args.get('applicant_email_address')],
        subject,
        config,
        template.render(
            full_name=args.get('applicant_name'),
            prohibition_number=prohibition_number,
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config),
        args.get('disclosure_for_applicant')), args


def applicant_evidence_instructions(**args) -> tuple:
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = 'send_evidence_instructions.html'
    subject = get_subject_string(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return send_email(
        [args.get('applicant_email_address')],
        subject,
        config,
        template.render(
            full_name=args.get('applicant_name'),
            prohibition_number=prohibition_number,
            subject=subject),
        config.COMM_SERV_API_ROOT_URL,
        get_common_services_access_token(config),
        args.get('disclosure_for_applicant')), args


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


def send_email(to: list, subject: str, config, template, api_root_url: str, token: str, attachments=None) -> tuple:
    if attachments is None:
        attachments = []
    payload = {
        "attachments": attachments,
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


def get_subject_string(template_name: str, prohibition_number: str):
    subjects = {
        "last_name_mismatch.html": "Re: Driving Prohibition Review - Prohibition Number and Name Don't Match - {}",
        "application_not_yet_in_vips.html": 'Re: Driving Prohibition Review - Not Entered Yet - {}',
        "application_already_created.html": "Re: Driving Prohibition Review - Already Applied - {}",
        "review_date_confirmed_ORAL.html": "Re: Driving Prohibition Review - Review Date Confirmed - {}",
        "review_date_confirmed_WRIT.html": "Re: Driving Prohibition Review - Review Date Confirmed - {}",
        "select_review_date.html": "Re: Driving Prohibition Review - Select a Review Date - {}",
        "application_not_found.html": "Re: Driving Prohibition Review - Not Found - {}",
        "licence_not_seized.html": "Re: Driving Prohibition Review - Licence Not Returned - {}",
        "application_not_received_in_time.html": "Re: Driving Prohibition Review - 7-day Application Window Missed - {}",
        "application_accepted.html": "Re: Driving Prohibition Review - Application Received  - {}",
        "send_disclosure_documents.html": "Re: Driving Prohibition Review - Disclosure Documents Attached - {}",
        "send_evidence_instructions.html": "Re: Driving Prohibition ReviewSubmit Evidence - {}"
    }
    subject_string = subjects[template_name].format(prohibition_number)
    logging.info(subject_string)
    return subject_string
