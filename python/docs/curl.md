# Sample Curl Requests

##### Note: the URL `localhost:5000` used in the examples below will need to be changed

###evt_issuance
```
curl --request POST \
  --url http://localhost:5000/v1/publish/event \
  --header 'content-type: application/json' \
  --data '{
    "event_id": 12351,
    "event_version": "1.4",
    "event_date_time": "2020-01-20 08:23:16",
    "event_type": "evt_issuance",
    "evt_issuance": {
        "ticket_number": "EZ12345680 ",
        "violation_date": "2019-09-01",
        "violation_time": "12:01",
        "vehicle_make_name": "FORD",
        "vehicle_type_code": "4DR",
        "violation_city_name": "ABBOTSFORD",
        "violation_city_code": "ABB",
        "violation_highway_desc": "HWY # 1 / CLEARBROOK ON RAMP",
        "enforcement_jurisdiction_name": "UPPER FRASER VALLEY REG RCMP",
        "enforcement_jurisdiction_code":"1501",
        "enforcement_officer_number": "1111",
        "enforcement_officer_name": "SMITH, JANE",
        "count_quantity": 2,
        "counts": [
            {
                "count_number": 1,
                "act_code": "MR",
                "section_text": "30.10(4)",
                "section_desc": "FAIL TO DISPLAY \"N\" SIGN IN VIOLATION OF DRIVER'\''S LICENCE CONDITION (S. 25(15) MV)",
                "fine_amount": "109.0"
            },
						{
                "count_number": 2,
                "act_code": "MR",
                "section_text": "30.10(4)",
                "section_desc": "FAIL TO DISPLAY \"N\" SIGN IN VIOLATION OF DRIVER'\''S LICENCE CONDITION (S. 25(15) MV)",
                "fine_amount": "109.0"
            }

        ]
        
    }
}'
```

###vt_query
```
curl --request POST \
  --url https://localhost:5000/v1/publish/event \
  --header 'content-type: application/json' \
  --data '{
    "event_id": 1236,
    "event_version": "1.4",
    "event_date_time": "2020-01-20 08:23:16",
    "event_type": "vt_query",
    "vt_query": {
        "ticket_number": "EZ12345678"
      }
}'
```

###vt_payment
```
curl --request POST \
  --url http://localhost:5000/v1/publish/event \
  --header 'content-type: application/json' \
  --data '{
    "event_id": 1234,
    "event_version": "1.4",
    "event_date_time": "2020-01-20 08:23:16",
    "event_type": "vt_payment",
    "vt_payment": {
        "ticket_number": "EZ12345678",
        "count_number": 1,
        "payment_card_type": "Visa",
        "payment_ticket_type_code": "S",
        "payment_amount": 142
      }
}'
```

###vt_dispute
```
curl --request POST \
  --url http://localhost:5000/v1/publish/event \
  --header 'content-type: application/json' \
  --data '{
    "event_id": 1234,
    "event_version": "1.4",
    "event_date_time": "2020-01-20 08:23:16",
    "event_type": "vt_dispute",
    "vt_dispute": {
        "ticket_number": "EZ12345678",
        "count_number": 1,
        "dispute_action_date": "2019-09-01",
        "dispute_type_code": "A",
        "count_act_regulation": "MVA",
        "compressed_section": "146.1"
      }
}'
```

###vt_dispute_finding
```
curl --request POST \
  --url http://localhost:5000/v1/publish/event \
  --header 'content-type: application/json' \
  --data '{
    "event_id": 1234,
    "event_version": "1.4",
    "event_date_time": "2020-01-20 08:23:16",
    "event_type": "vt_dispute_finding",
    "vt_dispute_finding": {
        "ticket_number": "EZ12345678",
        "count_number": 1,
        "finding_date": "2019-09-01",
        "finding_code": "string",
        "finding_description": "string"
      }
}'
```

###vt_dispute_status_update
```
curl --request POST \
  --url http://localhost:5000/v1/publish/event \
  --header 'content-type: application/json' \
  --data ' {
    "event_id": 1234,
    "event_version": "1.4",
    "event_date_time": "2020-01-20 08:23:16",
    "event_type": "vt_dispute_status_update",
    "vt_dispute_status_update": {
        "ticket_number": "EZ12345678",
        "count_number": 1,
        "dispute_action_code": "P",
        "dispute_action_date": "2019-09-01"
      }
}'
```