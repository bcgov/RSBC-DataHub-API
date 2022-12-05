# Get a document record from DEV
param (
    [string] $DOCUMENT_NUMBER,      # Example: 00197501
    [string] $ENVIRONMENT = "DEV"      # Example, DEV, TEST. Defaults to DEV.
)

if (${Headers} -eq "") {
    $USERNAME64 = oc --namespace=c220ad-dev get secret digitalforms-api -o jsonpath="{.data.DIGITALFORMS_BASICAUTH_USER}"
    $PASSWORD64 = oc --namespace=c220ad-dev get secret digitalforms-api -o jsonpath="{.data.DIGITALFORMS_BASICAUTH_PASSWORD}"
    $USERNAME   = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(${USERNAME64}))
    $PASSWORD   = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(${PASSWORD64}))
    $Headers    = @{ Authorization = "Basic {0}" -f [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f "${USERNAME}","${PASSWORD}"))) }
}

$URL = "https://digitalforms-viirp-api-c220ad-${ENVIRONMENT}.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${DOCUMENT_NUMBER}/Get-Document.ps1"

try {
    $Response = Invoke-WebRequest -UseBasicParsing -Method GET -Headers $Headers ${URL}
    $Response.Content
}
catch {
    $ReturnCode = $_.Exception.Response.StatusCode.Value__
    $Error = $_.ErrorDetails.Message
    "HTTP ${ReturnCode}: ${Error}"
}
