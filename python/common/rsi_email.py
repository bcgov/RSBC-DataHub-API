import python.common.helper as helper
from python.common.config import Config
import python.common.common_email_services as common_email_services
from datetime import datetime
import json
import logging
from jinja2 import Environment, select_autoescape, FileSystemLoader

logging.basicConfig(level=Config.LOG_LEVEL)


def application_accepted(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    vips_data = args.get('vips_data')
    t = "{}_application_accepted.html".format(vips_data['noticeTypeCd'])
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=content["subject"])), args


def applicant_review_type_change(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = "review_type_change.html"
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=content["subject"])), args


def send_form_xml_to_admin(**args):
    xml = args.get('xml_base64', None)
    if xml:
        config = args.get('config')
        prohibition_number = args.get('prohibition_number')
        subject = 'DEBUG - Form XML attached - {}'.format(prohibition_number)
        template = get_jinja2_env().get_template('admin_notice.html')
        return common_email_services.send_email(
            [config.ADMIN_EMAIL_ADDRESS],
            subject,
            config,
            template.render(
                body='XML attached',
                message='message xml attached',
                subject=subject),
            [{
                "content": args.get('xml_base64'),
                "contentType": "string",
                "encoding": "base64",
                "filename": "submitted_form.xml"
            }]), args
    logging.info('No XML to send')


def send_email_to_admin(**args):
    subject = args.get('subject')
    config = args.get('config')
    message = args.get('message')
    body = args.get('body')
    template = get_jinja2_env().get_template('admin_notice.html')
    return common_email_services.send_email(
        [config.ADMIN_EMAIL_ADDRESS],
        subject,
        config,
        template.render(subject=subject, body=body, message=json.dumps(message))), args


def applicant_prohibition_served_more_than_7_days_ago(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = "not_received_in_time.html"
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=content["subject"])), args


def applicant_licence_not_seized(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = "licence_not_seized.html"
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=content["subject"])), args


def applicant_prohibition_not_found(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    notice_type = args.get('user_entered_notice_type')
    t = "{}_prohibition_not_found.html".format(notice_type)
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=content["subject"])), args


def applicant_to_schedule_review(**args):
    """
    This message is sent immediately after an applicant pays
    the application fee.  Since we don't have the driver's
    first name handy, this email is addressed to the applicant.
    """
    config = args.get('config')
    vips_application = args.get('vips_application')
    vips_data = args.get('vips_data')
    t = "{}_select_review_date.html".format(vips_data['noticeTypeCd'])
    args['email_template'] = t
    email_address = vips_application['email']
    full_name = "{} {}".format(vips_application['firstGivenNm'], vips_application['surnameNm'])
    prohibition_number = args.get('prohibition_number')
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [email_address],
        content["subject"],
        config,
        template.render(
            full_name=full_name,
            prohibition_number=prohibition_number,
            subject=content["subject"])), args


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
    args['email_template'] = t
    phone = vips_application['phoneNo']
    prohibition_number = args.get('prohibition_number')
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [email_address],
        content["subject"],
        config,
        template.render(
            full_name=args.get('applicant_name'),
            prohibition_number=prohibition_number,
            subject=content["subject"],
            phone=phone,
            human_friendly_time_slot=args.get('friendly_review_time_slot'))), args


def applicant_last_name_mismatch(**args):
    """
    This email is sent to the applicant if the last name entered by the applicant
    does not match the last name of the driver as entered in VIPS
    """
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    vips_data = args.get('vips_data')
    t = "{}_last_name_mismatch.html".format(vips_data['noticeTypeCd'])
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=content["subject"])), args


def applicant_prohibition_not_found_yet(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    date_served_string = args.get('date_of_service')
    date_served = helper.localize_timezone(datetime.strptime(date_served_string, '%Y-%m-%d'))
    human_friendly_date_served = date_served.strftime("%B %d, %Y")
    notice_type = args.get('user_entered_notice_type')
    t = "{}_prohibition_not_found_yet.html".format(notice_type)
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)

    # Note: we rely on the date_served as submitted by the user -- not the date in VIPS
    # Check to see if enough time has elapsed to enter the prohibition into VIPS
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            date_of_service=human_friendly_date_served,
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=content["subject"])), args


def already_applied(**args):
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = 'already_applied.html'
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            full_name=args.get('driver_full_name'),
            prohibition_number=prohibition_number,
            subject=content["subject"])), args


def applicant_disclosure(**args) -> tuple:
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = 'send_disclosure_documents.html'
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            full_name=args.get('applicant_name'),
            prohibition_number=prohibition_number,
            callout=content['callout'],
            timeline=content['timeline'],
            subject=content["subject"]),
        args.get('disclosure_for_applicant')), args


def applicant_evidence_instructions(**args) -> tuple:
    config = args.get('config')
    prohibition_number = args.get('prohibition_number')
    t = 'send_evidence_instructions.html'
    args['email_template'] = t
    content = get_email_content(t, prohibition_number)
    template = get_jinja2_env().get_template(t)
    return common_email_services.send_email(
        [args.get('applicant_email_address')],
        content["subject"],
        config,
        template.render(
            full_name=args.get('applicant_name'),
            prohibition_number=prohibition_number,
            callout=content['callout'],
            timeline=content['timeline'],
            subject=content["subject"])), args


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


def get_jinja2_env():
    template_loader = FileSystemLoader(searchpath="./python/common/templates")
    return Environment(
        loader=template_loader,
        autoescape=select_autoescape(['html', 'xml'])
    )


def get_email_content(template_name: str, prohibition_number: str):
    content = content_data()
    if template_name in content:
        email_content = content[template_name]
        email_content['subject'] = email_content['raw_subject'].format(prohibition_number)
        logging.info(email_content)
        return email_content
    return dict({
            "raw_subject": "Unknown template requested {}",
            "subject": "Unknown template",
            "callout": "",
            "title": "Unknown Template",
            "timeline": ""
        })


def content_data() -> dict:
    return dict({
        "IRP_last_name_mismatch.html": {
            "raw_subject": "Prohibition Number or Name Don't Match - Driving Prohibition Review {}",
            "title": "IRP Prohibition Number or Name Don’t Match",
        },
        "ADP_last_name_mismatch.html": {
            "raw_subject": "Prohibition Number or Name Don't Match - Driving Prohibition Review {}",
            "title": "ADP Prohibition Number or Name Don’t Match",
        },
        "UL_last_name_mismatch.html": {
            "raw_subject": "Prohibition Number or Name Don't Match - Driving Prohibition Review {}",
            "title": "UL Prohibition Number or Name Don’t Match",
        },
        "IRP_prohibition_not_found_yet.html": {
            "raw_subject": "Prohibition Not Found Yet - Driving Prohibition Review {}",
            "title": "IRP Prohibition Not Found Yet",
        },
        "ADP_prohibition_not_found_yet.html": {
            "raw_subject": "Prohibition Not Found Yet - Driving Prohibition Review {}",
            "title": "ADP Prohibition Not Found Yet",
        },
        "UL_prohibition_not_found_yet.html": {
            "raw_subject": "Prohibition Not Found Yet - Driving Prohibition Review {}",
            "title": "UL Prohibition Not Found Yet",
        },
        "already_applied.html": {
            "raw_subject": "Already Applied – Driving Prohibition Review {}",
            "title": "Already Applied",
        },
        "review_date_confirmed_ORAL.html": {
            "raw_subject": "Review Date Confirmed - Driving Prohibition Review {}",
            "title": "Review Date Confirmed Oral",
        },
        "review_date_confirmed_WRIT.html": {
            "raw_subject": "Review Date Confirmed - Driving Prohibition Review {}",
            "title": "Review Date Confirmed Written",
        },
        "IRP_select_review_date.html": {
            "raw_subject": "Select Review Date - Driving Prohibition Review {}",
            "title": "IRP Select Review Date",
        },
        "ADP_select_review_date.html": {
            "raw_subject": "Select Review Date - Driving Prohibition Review {}",
            "title": "ADP Select Review Date",
        },
        "UL_select_review_date.html": {
            "raw_subject": "Select Review Date - Driving Prohibition Review {}",
            "title": "UL Select Review Date",
        },
        "IRP_prohibition_not_found.html": {
            "raw_subject": "Prohibition Not Found – Driving Prohibition Review {}",
            "title": "IRP Prohibition Not Found"
        },
        "ADP_prohibition_not_found.html": {
            "raw_subject": "Prohibition Not Found – Driving Prohibition Review {}",
            "title": "ADP Prohibition Not Found"
        },
        "UL_prohibition_not_found.html": {
            "raw_subject": "Prohibition Not Found – Driving Prohibition Review {}",
            "title": "UL Prohibition Not Found"
        },
        "licence_not_seized.html": {
            "raw_subject": "Licence Not Surrendered - Driving Prohibition Review {}",
            "title": "Licence Not Surrendered",
        },
        "not_received_in_time.html": {
            "raw_subject": "7-day Application Window Missed - Driving Prohibition Review {}",
            "title": "7-day Application Window Missed",
        },
        "IRP_application_accepted.html": {
            "raw_subject": "Application Accepted - Driving Prohibition Review {}",
            "title": "IRP Application Accepted",
        },
        "ADP_application_accepted.html": {
            "raw_subject": "Application Accepted - Driving Prohibition Review {}",
            "title": "ADP Application Accepted",
        },
        "UL_application_accepted.html": {
            "raw_subject": "Application Accepted - Driving Prohibition Review {}",
            "title": "UL Application Accepted",
        },
        "send_disclosure_documents.html": {
            "raw_subject": "Disclosure Documents Attached - Driving Prohibition Review {}",
            "title": "Send Disclosure",
        },
        "send_evidence_instructions.html": {
            "raw_subject": "Submit Evidence - Driving Prohibition Review {}",
            "title": "Submit Evidence",
        },
        "evidence_received.html": {
            "raw_subject": "Evidence Received - Driving Prohibition Review {}",
            "title": "Evidence Received",
        },
        "review_type_change.html": {
            "raw_subject": "Review Type Change - Driving Prohibition Review {}",
            "title": "Review Type Change",
        }
    })
