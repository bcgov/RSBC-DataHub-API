from flask import make_response
import logging


def successful_create_response(**kwargs) -> tuple:
    response_dict = kwargs.get('response_dict')
    kwargs['response'] = make_response(response_dict, 201)
    return True, kwargs


def successful_update_response(**kwargs) -> tuple:
    response_dict = kwargs.get('response_dict')
    kwargs['response'] = make_response(response_dict, 200)
    return True, kwargs


def server_error_response(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'server error'}, 500)
    return True, kwargs


def bad_request_response(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'bad request'}, 400)
    return True, kwargs


def record_not_found(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'record not found'}, 400)
    return True, kwargs


def unauthorized(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'unauthorized'}, 401)
    return True, kwargs


def unable_to_retrieve_keycloak_certificates(**kwargs) -> tuple:
    logging.warning("unable to retrieve keycloak certificates")
    kwargs['response'] = make_response({'error': 'unable to retrieve keycloak certificates'}, 500)
    return True, kwargs


def keycloak_token_not_valid(**kwargs) -> tuple:
    logging.warning("keycloak access token not valid")
    kwargs['response'] = make_response({'error': 'token not valid'}, 401)
    return True, kwargs


def keycloak_no_username(**kwargs) -> tuple:
    logging.warning("decoded keycloak token has no username")
    kwargs['response'] = make_response({'error': 'server error'}, 500)
    return True, kwargs


def no_user_guid(**kwargs) -> tuple:
    logging.warning("decoded keycloak token has no user_guid")
    kwargs['response'] = make_response({'error': 'server error'}, 500)
    return True, kwargs


def role_already_exists(**kwargs) -> tuple:
    logging.warning("role for {} already exists".format(kwargs.get('username')))
    kwargs['response'] = make_response({'error': 'role already exists'}, 400)
    return True, kwargs


def user_already_exists(**kwargs) -> tuple:
    logging.warning("user for {} already exists".format(kwargs.get('username')))
    kwargs['response'] = make_response({'error': 'user already exists'}, 400)
    return True, kwargs


def payload_missing(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'missing payload'}, 403)
    return True, kwargs


def failed_validation(**kwargs) -> tuple:
    kwargs['response'] = make_response({
        'message': 'failed validation',
        'errors': kwargs.get('validation_errors')
    }, 400)
    return True, kwargs


def no_payload(**kwargs) -> tuple:
    kwargs['response'] = make_response({'error': 'no payload'}, 400)
    return True, kwargs


def respond_test_vehicle(**kwargs) -> tuple:
    # TODO - Remove before flight
    kwargs['response'] = make_response(sample_vehicle_response(), 200)
    return True, kwargs


def sample_vehicle_response() -> list:
    # TODO - Remove before flight
    return [
        {
            "plateNumber": "LD626J",
            "registrationNumber": "03371224",
            "vehicleIdNumber": "5Y2SL65806Z418645",
            "effectiveDate": "",
            "vehicleMake": "PONTIAC",
            "vehicleModel": "VIBE",
            "vehicleStyle": "FourDoorSedan",
            "vehicleModelYear": "2006",
            "vehicleColour": "Grey",
            "vehicleType": "Passenger",
            "nscNumber": "",
            "vehicleParties": [
                {
                    "roleType": "RegisteredOwner",
                    "party": {
                        "ICBCEnterpriseID": "138929719980602",
                        "partyType": "Person",
                        "lastName": "WIEBE",
                        "firstName": "ANDREW",
                        "secondName": "JAMES",
                        "thirdName": "",
                        "nameType": "Legal",
                        "birthDate": "1964-09-22",
                        "dlNumber": "4714606",
                        "dlPlaceOfIssue": "BC",
                        "addresses": [
                            {
                                "addressType": "Residence",
                                "addressLine1": "7608 HEATHER ST",
                                "addressLine2": "",
                                "addressLine3": "",
                                "city": "VANCOUVER",
                                "region": "BC",
                                "country": "CAN",
                                "postalCode": "V6P3R1",
                                "unitNumber": "",
                                "streetNumber": "7608",
                                "streetName": "HEATHER",
                                "streetType": "ST",
                                "streetDirection": "",
                                "boxNumber": "",
                                "location": "",
                                "postalStationName": "",
                                "postalStationQualifier": "",
                                "postalStationType": "",
                                "routeServiceClass": "",
                                "routeServiceNumber": "",
                                "additionalDeliveryInfo": ""
                            }
                        ]
                    }
                }
            ]
        }
    ]
