$ICBC_ENDPOINT = "https://wsgw.dev.jag.gov.bc.ca/vips/icbc/dfft/contravention"

# Set credentials and headers:
$USERNAME   = "SVCKE5B"
$PASSWORD   = "6zVk2ich"
$Headers    = @{ Authorization = "Basic {0}" -f [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f "${USERNAME}","${PASSWORD}"))) }

# Build the payload from a file template
$PAYLOAD = Get-Content -Raw -Path payload-12-hour-alcohol.json | ConvertFrom-Json
$PDF_FILENAME = "GAUDRY_J-100039_all.pdf"
$PAYLOAD.pdf = [convert]::ToBase64String((Get-Content -path "${PDF_FILENAME}" -Encoding byte))
$JSON_PAYLOAD = ${PAYLOAD} | ConvertTo-Json


# Send payload
$RESP = Invoke-WebRequest -UseBasicParsing -Method POST -ContentType "application/json" -Headers $Headers -Body ${JSON_PAYLOAD} -Uri ${ICBC_ENDPOINT}

$RESP | Get-Method