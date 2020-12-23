# About the Geocoder

The RSI Geocoder API provides the lat / lon of street addresses or the intersection of two roadways.  The API
extends the DataBC Geocoder API and provides the option to submit the address to Google's geocoding service if
the score returned by DataBC doesn't meet a minimum score.

### End point:  /address

Accepts POST requests in the form of a JSON payload:  Sample Curl request:   

 
``` 
  curl --request POST --url http://<host_name>/address \
  -u "<username>:<password>" \
  --header 'Content-Type: application/json' \
  --data '{"address": "GREAT NORTHERN WAY AND KEITH DR, VANCOUVER, BC"}' 
```

Returns a JSON object that like this:
 
```
{
  "address_raw": "GREAT NORTHERN WAY AND KEITH DR, VANCOUVER, BC",
  "data_bc": {
    "faults": [
      {
        "element": "LOCALITY_GARBAGE",
        "fault": "notAllowed",
        "penalty": 3,
        "value": "AND KEITH DR"
      }
    ],
    "full_address": "Great Northern Way, Vancouver, BC",
    "lat": 49.2665959,
    "lon": -123.0885533,
    "precision": "STREET",
    "score": 75
  },
  "is_success": true
} 
```

If the Google fail-over option is enabled (see environment variables below) then the response expands to include the
response from DataBC and Google:

```
{
  "address_raw": "GREAT NORTHERN WAY AND KEITH DR, VANCOUVER, BC",
  "data_bc": {
    "faults": [
      {
        "element": "LOCALITY_GARBAGE",
        "fault": "notAllowed",
        "penalty": 3,
        "value": "AND KEITH DR"
      }
    ],
    "full_address": "Great Northern Way, Vancouver, BC",
    "lat": 49.2665959,
    "lon": -123.0885533,
    "precision": "STREET",
    "score": 75
  },
  "google": {
    "lat": 49.2665959,
    "lon": -123.0885533,
    "score": 90
  },
  "is_success": true
} 
```


 # Environment Variables

 The geocoder is configured using environment variables.  
 - `GEOCODE_SECRET_KEY` - is an alpha numerical string that Flask uses to keep client-side sessions secure. Each instance **MUST** set a unique key.
 - `GEOCODE_BASIC_AUTH_USER` & `GEOCODE_BASIC_AUTH_PASS` - are the credentials API consumers need to use when making requests to the geocoder.
 - `LOG_LEVEL` - sets the verbosity of the logging system. Options are: WARN, INFO or DEBUG. By default the log level is set to INFO.
 - `DATA_BC_API_URL` - the DataBC root URL.  By default, it's set to:  https://geocoder.api.gov.bc.ca
 - `DATA_BC_API_KEY` - the DataBC API key.  Required for high-volume users, but not required for testing.
 - `MIN_CONFIDENCE_SCORE` - a DataBC score below which the address is sent to Google.  Requires "GOOGLE_FAIL_OVER_ENABLED" environment variable to be set to "TRUE"     
 - `GOOGLE_FAIL_OVER_ENABLED` - set to either "TRUE" or "FALSE"
 - `GOOGLE_API_ROOT_URL` - the Google root URL.  By default, it's set to:  https://maps.googleapis.com/maps/api/geocode/json
 - `GOOGLE_API_KEY` - the Google API key that's required to access Google's servers

