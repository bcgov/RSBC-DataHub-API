import logging
import logging.config
import requests


def app_accepted_event(**args):
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
    payloadrecord["prohibitionNo"] = args['message']['prohibition_review']['form']['prohibition-information'][
        'prohibition-number-clean']
    payloadrecord["prohibitionNoClean"] = args['message']['prohibition_review']['form']['prohibition-information'][
        'prohibition-number-clean']

    # Get flags
    payloadrecord["isAdp"] = bool(
        args['message']['prohibition_review']['form']['prohibition-information']['control-is-adp'])
    payloadrecord["isIrp"] = bool(
        args['message']['prohibition_review']['form']['prohibition-information']['control-is-irp'])
    payloadrecord["isUl"] = bool(
        args['message']['prohibition_review']['form']['prohibition-information']['control-is-ul'])
    payloadrecord["licenceNotSurrendered"] = (lambda x: False if (x == None or x == False) else True)(
        args['message']['prohibition_review']['form']['prohibition-information']['licence-not-surrendered'])
    payloadrecord["licenceLostOrStolen"] = (lambda x: False if (x == None or x == False) else True)(
        args['message']['prohibition_review']['form']['prohibition-information']['licence-lost-or-stolen'])
    payloadrecord["licenceNotIssued"] = (lambda x: False if (x == None or x == False) else True)(
        args['message']['prohibition_review']['form']['prohibition-information']['licence-not-issued'])

    # get dt of service
    payloadrecord["dtOfService"] = args['message']['prohibition_review']['form']['prohibition-information'][
        'date-of-service']

    # get role
    payloadrecord["applicantRole"] = args['message']['prohibition_review']['form']['identification-information'][
        'applicant-role']

    # get applicant details
    payloadrecord["applicantFirstNm"] = args['message']['prohibition_review']['form']['identification-information'][
        'first-name-applicant']
    payloadrecord["applicantLastNm"] = args['message']['prohibition_review']['form']['identification-information'][
        'last-name-applicant']
    payloadrecord["applicantPhoneNo"] = args['message']['prohibition_review']['form']['identification-information'][
        'applicant-phone-number']
    payloadrecord["applicantEmailAddr"] = args['message']['prohibition_review']['form']['identification-information'][
        'applicant-email-address']
    payloadrecord["applicantEmailConfirm"] = \
    args['message']['prohibition_review']['form']['identification-information']['applicant-email-confirm']

    # Get driver deails
    payloadrecord["driverFirstNm"] = args['message']['prohibition_review']['form']['identification-information'][
        'driver-first-name']
    payloadrecord["driverLastNm"] = args['message']['prohibition_review']['form']['identification-information'][
        'driver-last-name']
    payloadrecord["driverInformationDriverDl"] = \
    args['message']['prohibition_review']['form']['identification-information']['driver-bcdl']
    payloadrecord["streetInformationStreetAddr"] = \
    args['message']['prohibition_review']['form']['identification-information']['street-address']
    payloadrecord["driverCityTown"] = args['message']['prohibition_review']['form']['identification-information'][
        'control-driver-city-town']
    payloadrecord["driverProvince"] = args['message']['prohibition_review']['form']['identification-information'][
        'control-driver-province']
    payloadrecord["driverPostalCde"] = args['message']['prohibition_review']['form']['identification-information'][
        'control-driver-postal-code']

    # get applicant signatue info
    payloadrecord["applicantSignature"] = args['message']['prohibition_review']['form']['consent-and-submission'][
        'signature-applicant-name']
    payloadrecord["applicantDtSigned"] = args['message']['prohibition_review']['form']['consent-and-submission'][
        'date-signed']

    eventpayload['appacceptedpayload'].append(payloadrecord)
    endpoint = "https://api-be5301-dev.apps.silver.devops.gov.bc.ca/dfevents/appaccepted"
    headers = {'ride-api-key': '7cb719a8-1d5a-4c65-9032-425e52355b07'}
    response = requests.post(endpoint, json=eventpayload, verify=False,headers=headers)
    print(response.json())


    #TODO: For errors write to RabbitMQ
    return True, args

def disclosure_sent(**args):
    logging.info("this is from ride function disclosure_sent")
    logging.info(args)
    # TODO: Call RIDE API endpoint
    # TODO: For errors write to RabbitMQ
    return True, args

def evidence_submitted(**args):
    logging.info("this is from ride function evidence_submitted")
    logging.info(args)
    # TODO: Call RIDE API endpoint
    # TODO: For errors write to RabbitMQ
    return True, args

def payment_received(**args):
    logging.info("this is from ride function payment_received")
    logging.info(args)
    # TODO: Call RIDE API endpoint
    # TODO: For errors write to RabbitMQ
    return True, args

def review_scheduled(**args):
    logging.info("this is from ride function review_scheduled")
    logging.info(args)
    # TODO: Call RIDE API endpoint
    # TODO: For errors write to RabbitMQ
    return True, args




