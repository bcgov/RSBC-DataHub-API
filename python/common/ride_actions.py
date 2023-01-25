import logging
import logging.config
import requests
import datetime
from python.common.vips_api import vips_str_to_datetime
import python.common.vips_api as vips
import iso8601


def app_accepted_event(**args):
    try:
        logging.info("this is from ride function new app_accepted_event")
        logging.info(args)
        #TODO: Call RIDE API endpoint
        eventpayload = {}
        eventpayload['typeofevent'] = 'app_accepted'
        eventpayload['appacceptedpayload'] = []
        payloadrecord = {}
        payloadrecord["eventVersion"] = 1.0

        # convert date time to string
        tvalue = args['message']['event_date_time']
        tformat = "%Y-%m-%dT%H:%M:%S.%f"
        tformatted = datetime.datetime.strptime(tvalue, tformat)
        format_string = "%Y-%m-%d %H:%M:%S"
        dtstr = tformatted.strftime(format_string)
        payloadrecord["eventDtm"] = dtstr

        payloadrecord["eventType"] = "app_accepted"

        # Get prohibition no
        payloadrecord["prohibitionNo"] = args['message']['prohibition_review']['form']['prohibition-information']['prohibition-number-clean']
        payloadrecord["prohibitionNoClean"] = args['message']['prohibition_review']['form']['prohibition-information']['prohibition-number-clean']

        # Get flags
        payloadrecord["isAdp"] = (lambda x: False if (x==None or x=='false') else True)(args['message']['prohibition_review']['form']['prohibition-information']['control-is-adp'])
        payloadrecord["isIrp"] = (lambda x: False if (x==None or x=='false') else True)(args['message']['prohibition_review']['form']['prohibition-information']['control-is-irp'])
        payloadrecord["isUl"] = (lambda x: False if (x==None or x=='false') else True)(args['message']['prohibition_review']['form']['prohibition-information']['control-is-ul'])
        payloadrecord["licenceNotSurrendered"] = (lambda x: False if (x == None or x == False or x=='false') else True)(args['message']['prohibition_review']['form']['prohibition-information']['licence-not-surrendered'])
        payloadrecord["licenceLostOrStolen"] = (lambda x: False if (x == None or x == False or x=='false') else True)(args['message']['prohibition_review']['form']['prohibition-information']['licence-lost-or-stolen'])
        payloadrecord["licenceNotIssued"] = (lambda x: False if (x == None or x == False or x=='false') else True)(args['message']['prohibition_review']['form']['prohibition-information']['licence-not-issued'])

        # get dt of service
        payloadrecord["dtOfService"] = args['message']['prohibition_review']['form']['prohibition-information']['date-of-service']

        # get role
        payloadrecord["applicantRole"] = args['message']['prohibition_review']['form']['identification-information']['applicant-role']

        # get applicant details
        payloadrecord["applicantFirstNm"] = args['message']['prohibition_review']['form']['identification-information']['first-name-applicant']
        payloadrecord["applicantLastNm"] = args['message']['prohibition_review']['form']['identification-information']['last-name-applicant']
        payloadrecord["applicantPhoneNo"] = args['message']['prohibition_review']['form']['identification-information']['applicant-phone-number']
        payloadrecord["applicantEmailAddr"] = args['message']['prohibition_review']['form']['identification-information']['applicant-email-address']
        payloadrecord["applicantEmailConfirm"] = args['message']['prohibition_review']['form']['identification-information']['applicant-email-confirm']

        # Get driver deails
        payloadrecord["driverFirstNm"] = args['message']['prohibition_review']['form']['identification-information']['driver-first-name']
        payloadrecord["driverLastNm"] = args['message']['prohibition_review']['form']['identification-information']['driver-last-name']
        payloadrecord["driverInformationDriverDl"] = args['message']['prohibition_review']['form']['identification-information']['driver-bcdl']
        payloadrecord["streetInformationStreetAddr"] = args['message']['prohibition_review']['form']['identification-information']['street-address']
        payloadrecord["driverCityTown"] = args['message']['prohibition_review']['form']['identification-information']['control-driver-city-town']
        payloadrecord["driverProvince"] = args['message']['prohibition_review']['form']['identification-information']['control-driver-province']
        payloadrecord["driverPostalCde"] = args['message']['prohibition_review']['form']['identification-information']['control-driver-postal-code']

        # get applicant signatue info
        payloadrecord["applicantSignature"] = args['message']['prohibition_review']['form']['consent-and-submission']['signature-applicant-name']
        payloadrecord["applicantDtSigned"] = args['message']['prohibition_review']['form']['consent-and-submission']['date-signed']

        eventpayload['appacceptedpayload'].append(payloadrecord)
        endpoint = "https://api-be5301-dev.apps.silver.devops.gov.bc.ca/dfevents/appaccepted"
        headers = {'ride-api-key': '7cb719a8-1d5a-4c65-9032-425e52355b07'}
        response = requests.post(endpoint, json=eventpayload, verify=False,headers=headers)
        print(response.json())
    except Exception as e:
        logging.error('error in sending app_accepted event to RIDE')
        logging.error(e)
    


    #TODO: For errors write to RabbitMQ
    return True, args

def disclosure_sent(**args):
    logging.info("this is from ride function disclosure_sent")
    logging.info(args)
    try:
        logging.info(args)
        # TODO: Call RIDE API endpoint
        eventpayload = {}
        eventpayload['typeofevent'] = 'disclosure_sent'
        eventpayload['disclosuresentpayload'] = []
        payloadrecord = {}
        payloadrecord["eventVersion"] = 1.0

        # convert date time to string
        dt1 = datetime.datetime.now()
        format_string = "%Y-%m-%d %H:%M:%S"
        dtstr = dt1.strftime(format_string)
        payloadrecord["eventDtm"] = dtstr

        payloadrecord["eventType"] = "disclosure_sent"

        # Get prohibition no
        payloadrecord["prohibitionNo"] = args.get('prohibition_number')
        # payloadrecord["prohibitionNo"] = args['message']['prohibition_review']['form']['prohibition-information'][
        #     'prohibition-number-clean']

        payloadrecord["applicantNm"] = args.get('applicant_name')
        payloadrecord["applicantEmail"] = args.get('applicant_email_address')

        message = args.get('message')
        # hold_hours = int(config.HOURS_TO_HOLD_BEFORE_DISCLOSURE)
        # message['hold_until'] = (datetime.datetime.today() + datetime.timedelta(hours=hold_hours)).isoformat()
        hold_until_val=""
        if 'hold_until' not in message:
            pass
        else:
            tmpval=iso8601.parse_date(message['hold_until'], "")
            hold_until_val=tmpval.strftime(format_string)
        payloadrecord["holdUntil"] = hold_until_val

        eventpayload['disclosuresentpayload'].append(payloadrecord)
        endpoint = "https://api-be5301-dev.apps.silver.devops.gov.bc.ca/dfevents/evidencesubmitted"
        headers = {'ride-api-key': '7cb719a8-1d5a-4c65-9032-425e52355b07'}
        response = requests.post(endpoint, json=eventpayload, verify=False, headers=headers)
        print(response.json())
    except Exception as e:
        logging.error('error in sending disclosure_sent event to RIDE')
        logging.error(e)
    # TODO: For errors write to RabbitMQ
    return True, args

def evidence_submitted(**args):
    logging.info("this is from ride function evidence_submitted")
    logging.info(args)
    try:
        logging.info("this is from ride function new evidence_submitted")
        logging.info(args)
        # TODO: Call RIDE API endpoint
        eventpayload = {}
        eventpayload['typeofevent'] = 'evidence_submitted'
        eventpayload['evidencesubmittedpayload'] = []
        payloadrecord = {}
        payloadrecord["eventVersion"] = 1.0

        # convert date time to string
        # tvalue = args['message']['event_date_time']
        # tformat = "%Y-%m-%dT%H:%M:%S.%f"
        # tformatted = datetime.datetime.strptime(tvalue, tformat)
        # format_string = "%Y-%m-%d %H:%M:%S"
        # dtstr = tformatted.strftime(format_string)
        # payloadrecord["eventDtm"] = dtstr
        dt1 = datetime.datetime.now()
        format_string = "%Y-%m-%d %H:%M:%S"
        dtstr = dt1.strftime(format_string)
        payloadrecord["eventDtm"] = dtstr

        payloadrecord["eventType"] = "evidence_submitted"

        # Get prohibition no
        payloadrecord["prohibitionNo"]=args.get('prohibition_number')
        # payloadrecord["prohibitionNo"] = args['message']['prohibition_review']['form']['prohibition-information'][
        #     'prohibition-number-clean']

        eventpayload['evidencesubmittedpayload'].append(payloadrecord)
        endpoint = "https://api-be5301-dev.apps.silver.devops.gov.bc.ca/dfevents/evidencesubmitted"
        headers = {'ride-api-key': '7cb719a8-1d5a-4c65-9032-425e52355b07'}
        response = requests.post(endpoint, json=eventpayload, verify=False, headers=headers)
        print(response.json())
    except Exception as e:
        logging.error('error in sending evidence_submitted event to RIDE')
        logging.error(e)
    # TODO: For errors write to RabbitMQ
    return True, args

def payment_received(**args):
    logging.info("this is from ride function payment_received")
    logging.info(args)
    try:
        logging.info(args)
        payload = args.get('payload')
        # TODO: Call RIDE API endpoint
        eventpayload = {}
        eventpayload['typeofevent'] = 'payment_received'
        eventpayload['payrecvdpayload'] = []
        payloadrecord = {}
        payloadrecord["eventVersion"] = 1.0

        # convert date time to string
        # "eventDtm":"2021-12-27 15:40:45",
        dt1 = datetime.datetime.now()
        format_string = "%Y-%m-%d %H:%M:%S"
        dtstr = dt1.strftime(format_string)
        payloadrecord["eventDtm"] = dtstr

        payloadrecord["eventType"] = "payment_received"

        # Get prohibition no
        payloadrecord["prohibitionNo"] = args.get('prohibition_number')

        payloadrecord["recieptNo"] = payload['receipt_number']

        payloadrecord["receiptAmt"] = payload['receipt_amount']

        payloadrecord["transactionId"] = payload.get('transaction_id')

        payloadrecord["paymentMethod"] = payload.get('payment_method')

        payloadrecord["cardType"] = payload.get('cardtype')

        receipt_datetime_object = args.get('receipt_date')

        payloadrecord["receiptDtm"] = receipt_datetime_object.strftime(format_string)

        eventpayload['payrecvdpayload'].append(payloadrecord)
        endpoint = "https://api-be5301-dev.apps.silver.devops.gov.bc.ca/dfevents/paymentreceived"
        headers = {'ride-api-key': '7cb719a8-1d5a-4c65-9032-425e52355b07'}
        response = requests.post(endpoint, json=eventpayload, verify=False, headers=headers)
        print(response.json())
    except Exception as e:
        logging.error('error in sending payment_received event to RIDE')
        logging.error(e)
    # TODO: For errors write to RabbitMQ
    return True, args

def review_scheduled(**args):
    logging.info("this is from ride function review_scheduled")
    logging.info(args)
    try:
        logging.info(args)
        # TODO: Call RIDE API endpoint
        eventpayload = {}
        eventpayload['typeofevent'] = 'review_scheduled'
        eventpayload['payrecvdpayload'] = []
        payloadrecord = {}
        payloadrecord["eventVersion"] = 1.0

        # convert date time to string
        # "eventDtm":"2021-12-27 15:40:45",
        dt1 = datetime.datetime.now()
        format_string = "%Y-%m-%d %H:%M:%S"
        dtstr = dt1.strftime(format_string)
        payloadrecord["eventDtm"] = dtstr

        payloadrecord["eventType"] = "review_scheduled"

        # Get prohibition no
        payloadrecord["prohibitionNo"] = args.get('prohibition_number')

        timeslotvalue=args.get('requested_time_slot')
        start_time = timeslotvalue['reviewStartDtm']
        end_time = timeslotvalue['reviewEndDtm']
        # {"reviewStartDtm":"2020-09-30 13:00:00 -07:00","reviewEndDtm":"2020-09-30 13:30:00 -07:00"}
        start_str=vips_str_to_datetime(start_time).strftime(format_string)
        end_str = vips_str_to_datetime(end_time).strftime(format_string)


        payloadrecord["reviewStartDtm"] = start_str

        payloadrecord["reviewEndDtm"] = end_str

        eventpayload['reviewscheduledpayload'].append(payloadrecord)
        endpoint = "https://api-be5301-dev.apps.silver.devops.gov.bc.ca/dfevents/reviewscheduled"
        headers = {'ride-api-key': '7cb719a8-1d5a-4c65-9032-425e52355b07'}
        response = requests.post(endpoint, json=eventpayload, verify=False, headers=headers)
        print(response.json())
    except Exception as e:
        logging.error('error in sending payment_received event to RIDE')
        logging.error(e)
    # TODO: For errors write to RabbitMQ
    return True, args




