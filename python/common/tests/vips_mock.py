import json
from datetime import datetime, timedelta
import python.common.vips_api as vips
import python.common.helper as help


def status_has_never_applied(prohibition_type, date_served='2018-04-12', last_name='Gordon', licence_seized='Y') -> dict:
    data = json.loads(json.dumps(status_get(date_served, prohibition_type, last_name, licence_seized)))  # deep copy
    data['data']['status']['notice_type'] = prohibition_type
    del data['data']['status']['reviews'][0]
    return data


def status_applied_and_paid_not_scheduled(prohibition_type, date_served='2018-04-12') -> dict:
    data = json.loads(json.dumps(status_get(date_served)))  # deep copy
    data['data']['status']['noticeTypeCd'] = prohibition_type
    del data['data']['status']['reviews'][0]['status']
    del data['data']['status']['reviews'][0]['reviewId']
    del data['data']['status']['reviews'][0]['reviewStartDtm']
    del data['data']['status']['reviews'][0]['reviewEndDtm']
    return data


def status_applied_not_paid(prohibition_type, date_served='2018-04-12') -> dict:
    data = json.loads(json.dumps(status_get(date_served)))  # deep copy
    data['data']['status']['noticeTypeCd'] = prohibition_type
    del data['data']['status']['reviews'][0]['status']
    del data['data']['status']['reviews'][0]['reviewId']
    del data['data']['status']['reviews'][0]['reviewStartDtm']
    del data['data']['status']['reviews'][0]['reviewEndDtm']
    del data['data']['status']['reviews'][0]['receiptNumberTxt']
    return data


def status_review_concluded(prohibition_type, date_served='2018-04-12') -> dict:
    data = json.loads(json.dumps(status_get(date_served)))  # deep copy
    data['data']['status']['noticeTypeCd'] = prohibition_type
    return data


def status_applied_paid_and_scheduled(prohibition_type, review_start_date: str) -> dict:
    data = json.loads(json.dumps(status_get('2018-04-12')))  # deep copy
    data['data']['status']['noticeTypeCd'] = prohibition_type
    data['data']['status']['reviews'][0]['reviewStartDtm'] = review_start_date
    return data


def status_previously_applied_review_unsuccessful(prohibition_type) -> dict:
    data = json.loads(json.dumps(status_get('2018-04-12')))  # deep copy
    data['data']['status']['noticeTypeCd'] = prohibition_type
    data['data']['status']['reviews'][0]['status'] = "unsuccessful"
    return data


def status_previously_applied_review_successful(prohibition_type) -> dict:
    data = json.loads(json.dumps(status_get('2018-04-12')))  # deep copy
    data['data']['status']['noticeTypeCd'] = prohibition_type
    data['data']['status']['reviews'][0]['status'] = "successful"
    return data

def status_applied_at_icbc(prohibition_type, review_start_date: str) -> dict:
    data = json.loads(json.dumps(status_get('2018-04-12')))  # deep copy
    data['data']['status']['noticeTypeCd'] = prohibition_type
    data['data']['status']['reviews'][0]['reviewStartDtm'] = review_start_date
    del data['data']['status']['reviews'][0]['applicationId']
    return data


def status_with_no_disclosure(prohibition_type, review_start_date: str) -> dict:
    data = json.loads(json.dumps(status_applied_paid_and_scheduled(prohibition_type, review_start_date)))  # deep copy
    data['data']['status']['disclosure'] = []
    return data


def status_with_one_sent_on_unsent_disclosure(prohibition_type, review_start_date: str) -> dict:
    data = json.loads(json.dumps(status_applied_paid_and_scheduled(prohibition_type, review_start_date)))  # deep copy
    yesterday = help.localize_timezone(datetime.today()) - timedelta(days=1)
    del data['data']['status']['disclosure'][0]['disclosedDtm']
    data['data']['status']['disclosure'][1]['disclosedDtm'] = vips.vips_datetime(yesterday)
    return data


def status_with_two_unsent_disclosures(prohibition_type, review_start_date: str) -> dict:
    data = json.loads(json.dumps(status_applied_paid_and_scheduled(prohibition_type, review_start_date)))  # deep copy
    del data['data']['status']['disclosure'][0]['disclosedDtm']
    del data['data']['status']['disclosure'][1]['disclosedDtm']
    return data


def status_with_two_disclosures_sent_last_month(prohibition_type, review_start_date: str) -> dict:
    data = json.loads(json.dumps(status_applied_paid_and_scheduled(prohibition_type, review_start_date)))  # deep copy
    last_month = help.localize_timezone(datetime.today() - timedelta(days=35))
    data['data']['status']['disclosure'][0]['disclosedDtm'] = vips.vips_datetime(last_month)
    data['data']['status']['disclosure'][1]['disclosedDtm'] = vips.vips_datetime(last_month)
    return data


def status_returns_html_response() -> str:
    return '<html><p>VIPS is offline</p></html>'


def status_not_found() -> dict:
    return {
      "resp": "fail",
      "error": {
        "message": "Record not found",
        "httpStatus": 404
      }
    }


def status_get(date_served, notice_type="UL", last_name='Gordon', licence_seized='Y') -> dict:
    return {
      "resp": "success",
      "data": {
        "status": {
          "noticeTypeCd": notice_type,
          "noticeServedDt": date_served + " 00:00:00 -07:00",
          "reviewFormSubmittedYn": "N",
          "reviewCreatedYn": "N",
          "originalCause": "IRPINDEF",
          "surnameNm": last_name,
          "driverLicenceSeizedYn": licence_seized,
          "disclosure": [
            {
                "documentId": "111",
                "disclosedDtm": "2019-01-02 17:30:00 -08:00"
            },
            {
                "documentId": "222",
                "disclosedDtm": "2019-01-02 17:30:00 -08:00"
            }
          ],
          "reviews": [
            {
              "status": "in_progress",
              "receiptNumberTxt": "1234",
              "applicationId": "bb71037c-f87b-0444-e054-00144ff95452",
              "reviewStartDtm": "2021-02-24 12:00:00 -08:00",
              "reviewEndDtm": "2021-02-24 12:30:00 -08:00",
              "reviewId": "2466"
            }
          ]
        }
      }
    }


def application_get(presentation_type='ORAL') -> dict:
    return {
      "resp": "success",
      "data": {
        "applicationInfo": {
          "prohibitionNoticeNo": "21900309",
          "noticeTypeCd": "IRP",
          "reviewApplnTypeCd": "IRP",
          "noticeSubjectCd": "PERS",
          "presentationTypeCd": presentation_type,
          "reviewRoleTypeCd": "APPNT",
          "firstGivenNm": "Developer",
          "surnameNm": "Norris",
          "phoneNo": "2505551212",
          "email": "applicant_fake@gov.bc.ca",
          "manualEntryYN": "N",
          "formData": "PD94bWwgdmVyc2lv3ZlPCbT4KItZW50cz4KPC9kYXRhPg=="
        }
      }
    }


def application_get_not_found() -> dict:
    return {
      "resp": "fail",
      "error": {
        "message": "Record not found",
        "httpStatus": 404
      }
    }


def payment_patch_payload() -> dict:
    return {

    }


def payment_get(payment_date: str) -> dict:
    return {
      "resp": "success",
      "data": {
        "transactionInfo": {
          "paymentCardType": "VISA",
          "paymentAmount": "222.00",
          "receiptNumberTxt": "12344444",
          "paymentDate": payment_date + " 04:30:00 -08:00"
        }
      }
    }


def schedule_get(start_date_iso: str) -> dict:
    return {
      "resp": "success",
      "data": {
        "timeSlots": [
          {
            "reviewStartDtm": start_date_iso + ' 09:30:00 -07:00',
            "reviewEndDtm": start_date_iso + ' 10:00:00 -07:00'
          }
        ]
      }
    }


def disclosure_get() -> dict:
    return {
        "resp": "success",
        "data": {
            "document": {
                "document": "base64_string_of_encoded_document",
                "mimeType": "application/pdf"
            }
        }
    }

