# Send 12/24 notices and PDF to ICBC

## Python script

Jonathan Longe wrote this script as a test tool, so he could verify that the ICBC API in the DEV environment was working.

He sent it to me to use as part of my testing with Brenda. See DF-2153.

Steps to run the Python script:
 
1. Create venv folder:
   - python -m venv venv
   - .\venv\scripts\Activate.ps1
2. Install packages: 
   - python-dotenv (for environment files)
   - requests (for REST API requests)
   - Faker (to generate test data)
3. Connect to office Ethernet, wifi, or IDIR VPN.
4. Find a suitable PDF file. 
   - Preferably one with a 12- or 24-hour prohibition.
   - Call script with PDF file as a parameter:

         > python .\send_to_ICBC.py --filename .\GAUDRY_J-100039_all.pdf 

5. Example output:
```
response status code: 200
payload: {                  
    "birthdate": "20110819",
    "dlJurisdiction": "BC", 
    "dlNumber": "0377118",  
    "firstName": "Joy",     
    "lastName": "Olson",
    "noticeNumber": "VA320723",
    "nscNumber": "045148",
    "officerDetachment": "VANCOUVER",
    "officerName": "Frederick",
    "officerNumber": "MB28566",
    "pdf": "[BASE64......]",
    "plateJurisdiction": "BC",
    "plateNumber": "QB 0701",
    "pujCode": "",
    "section": "215.2",
    "violationDate": "20220825",
    "violationLocation": "PORT HEATHERPORT",
    "violationTime": "12:08"
}
response: Contravention successfully stored.
```

## PowerShell

You can see the script send-to-icbc.ps1, where payload.json is the payload that gets sent to ICBC. It pulls in ${PDF_FILENAME}.

    $ICBC_ENDPOINT = "https://wsgw.dev.jag.gov.bc.ca/vips/icbc/dfft/contravention"
   
    # Set credentials and headers:
    $USERNAME   = ""
    $PASSWORD   = ""
    $Headers    = @{ Authorization = "Basic {0}" -f [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f "${USERNAME}","${PASSWORD}"))) }
   
    # Build the payload from a file template
    $PAYLOAD = Get-Content -Raw -Path payload-12-hour-alcohol.json | ConvertFrom-Json
    $PDF_FILENAME = "GAUDRY_J-100039_all.pdf"
    $PAYLOAD.pdf = [convert]::ToBase64String((Get-Content -path "${PDF_FILENAME}" -Encoding byte))
    $JSON_PAYLOAD = ${PAYLOAD} | ConvertTo-Json
   
    # Send payload
    $RESP = Invoke-WebRequest -UseBasicParsing -Method POST -ContentType "application/json" -Headers $Headers -Body ${JSON_PAYLOAD} -Uri ${ICBC_ENDPOINT}
   
    $RESP | Get-Method

## Curl command

Example:

    USERNAME=
    PASSWORD=
    curl --silent --verbose --request POST --header "Content-Type: application/json" --user "${USERNAME}:${PASSWORD}" --data @payload.json "https://wsgw.dev.jag.gov.bc.ca/vips/icbc/dfft/contravention"

### Example of successful send to ICBC

```
curl --silent --verbose --request POST --header "Content-Type: application/json" --user "${USERNAME}:${PASSWORD}" --data @payload.json "https://can01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwsgw.dev.jag.gov.bc.ca%2Fvips%2Ficbc%2Fdfft%2Fcontravention&data=05%7C01%7CSteve.1.Forsyth%40gov.bc.ca%7Caa19346f791a4aefafa908dab3a44e0e%7C6fdb52003d0d4a8ab036d3685e359adc%7C0%7C0%7C638019815505634691%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=vdaGFQzjuE5CTxWYtv9FDORvKzI9fF8LjWh7LA53MOU%3D&reserved=0"
* Trying 142.34.51.11:443...
* TCP_NODELAY set
* Connected to wsgw.dev.jag.gov.bc.ca (142.34.51.11) port 443 (#0)
* ALPN, offering h2
* ALPN, offering http/1.1
* successfully set certificate verify locations:
* CAfile: /etc/ssl/certs/ca-certificates.crt
CApath: /etc/ssl/certs
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
* TLSv1.2 (IN), TLS handshake, Request CERT (13):
* TLSv1.2 (IN), TLS handshake, Server finished (14):
* TLSv1.2 (OUT), TLS handshake, Certificate (11):
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
* TLSv1.2 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.2 (OUT), TLS handshake, Finished (20):
* TLSv1.2 (IN), TLS handshake, Finished (20):
* SSL connection using TLSv1.2 / ECDHE-RSA-AES256-GCM-SHA384
* ALPN, server did not agree to a protocol
* Server certificate:
* subject: C=CA; ST=British Columbia; L=Victoria; O=Ministry of Justice; CN=wsgw.dev.jag.gov.bc.ca
* start date: Mar 29 15:43:43 2022 GMT
* expire date: Apr 6 15:43:43 2023 GMT
* subjectAltName: host "wsgw.dev.jag.gov.bc.ca" matched cert's "wsgw.dev.jag.gov.bc.ca"
* issuer: C=US; O=Entrust, Inc.; OU=See https://can01.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.entrust.net%2Flegal-terms&data=05%7C01%7CSteve.1.Forsyth%40gov.bc.ca%7Caa19346f791a4aefafa908dab3a44e0e%7C6fdb52003d0d4a8ab036d3685e359adc%7C0%7C0%7C638019815505634691%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000%7C%7C%7C&sdata=2wyqKMWE5He6WBccGWMT9KOBXIzoGX9IVFzG0RyR2dk%3D&reserved=0; OU=(c) 2012 Entrust, Inc. - for authorized use only; CN=Entrust Certification Authority - L1K
* SSL certificate verify ok.
* Server auth using Basic with user 'SVCKE5B'
   > POST /vips/icbc/dfft/contravention HTTP/1.1
   > Host: wsgw.dev.jag.gov.bc.ca
   > Authorization: Basic ***********************==
   > User-Agent: curl/7.68.0
   > Accept: */*
   > Content-Type: application/json
   > Content-Length: 529237
   > Expect: 100-continue
   >
* Mark bundle as not supporting multiuse < HTTP/1.1 100 Continue
* We are completely uploaded and fine
* Mark bundle as not supporting multiuse < HTTP/1.1 200 OK < X-Backside-Transport: OK OK < X-Backside-Transport: OK OK < X-Powered-By: Servlet/4.0 < X-Content-Type-Options: nosniff < X-XSS-Protection: 1; mode=block < Cache-Control: no-cache, no-store, max-age=0, must-revalidate < Pragma: no-cache < Expires: 0 < X-Frame-Options: DENY < Content-Language: en-CA < Set-Cookie: LtpaToken2=npLLK3S0WwlWYjFynHS9QY9GyDGpGOguKCpw0wscgJmdvi0c79gvlLabqN65xtpMpJE7Yi4wgPiL+P6ZNaGnMLJl9n2ty/iZBNvbBnh8iXZb8eqPQZ3o9abduukwvaoGzu1y+G0UIInxgTSJKfyG7FvG42dBBf49jrhdVh5dhaLpDVSueaEiXy2MZe+Czup4fGLVffggKcNfq6lyD6cwDJpmiHxZ/aF4NqOR6YaHgGzxgYgboksQc3puVr9a+gPHsVLmy0F22dKHbntkPFxHBq2w3VMT5bnGE+8Vg8vSFz3O/mNyVXf2h/Efzc8yANYb3M23hA4KwjmXX1gWmUdk2TTwkMlRpI3jEHShpTeOQ7UdVmFhOkL+rB2y0swgcdb7; Path=/vips/icbc/dfft; HttpOnly; Secure; Domain=wsgw.dev.jag.gov.bc.ca < Strict-Transport-Security: max-age=31536000; includeSubDomains < X-Global-Transaction-ID: 6c77e8e66352ebc802081841 < Content-Type: application/json < Content-Length: 34 < Date: Fri, 21 Oct 2022 18:58:18 GMT < Server: Layer7-API-Gateway <
* Connection #0 to host wsgw.dev.jag.gov.bc.ca left intact
Contravention successfully stored.
```

## DLs from ICBC

   0000625, SYC-TSTFOUR, JOEY, 1985-02-02

   1695672, SYC-TSTFOUR, TST, 1992-06-06
   
## ICBC endpoint

The original endpoint on ICBC's side is: https://b2bmrg.icbc.com:7449/dfft/contravention