# PowerShell script to iterate the DF VI-IRP API, looking for free record numbers.
#
# Because VIPS records are not assigned in order, developers and testers create test records
# with any available number. This makes it impossible to get the next available record number
# without querying VIPS to see if that record already exists.
#
# This script works in the DEV or TEST environment. It defaults to DEV, but you can manually
# specify an environment with switch like this: "-environment DEV" or "-environment TEST"
# 
# Valid numbers are listed in Codetables noticePrefixNos section.
# - ADP: 00
# - IRP: 20, 21, 40
# - UL:  30
# - IMP: 00, 20, 22
#
# SCRIPT ARGUMENTS
#
# This script has named arguments. You can use the names, or just call them in order.
#
# -NUMBER_TYPE <ADP|IRP|UL|IMP|NUMBER>: either a record type or record number
# -SPECIFIED_NUMBER <NUMBER>: the first record number to check before iterating.
# -ENVIRONMENT <DEV|TEST>
#
# Example:
#
#   > .\get-next-available-vips-number.ps1 -number_type adp -specificed_number 00123456 -environment dev
#
# You can also call this script from the PowerShell prompt in four different ways without
# named arguments:
#
# 1) With a record number to check. Example:
#
#    > .\get-next-available-vips-number.ps1 <RECORD_NUMBER>
#    > .\get-next-available-vips-number.ps1 00123456
#
#    The script will iterate the number in the first parameter until it finds a free record number.
#    The first found record number is stored in a memory file in your home folder:
#    ${HOME}\.vips\last-prohibition-number.txt.
#
# 2) With no record number. Example:
#
#    > .\get-next-available-vips-number.ps1
#
#    The script will get the last found record number from the memory file and check to see if it
#    is still free. If it's no longer free, it will iterate until a free number is found. The
#    memory file is in your home folder as ${HOME}\.vips\last-prohibition-number.txt. 
#
# 3) With a record type and a record number. Example:
#
#    > .\get-next-available-vips-number.ps1 [ADP|IRP|UL|IMP] <RECORD_NUMBER>
#    > .\get-next-available-vips-number.ps1 adp 00123456
#
#    The script will check that the number sequence is correct for a record type (e.g. ADP numbers
#    start with '00') and will store the first found ADP record number in a memory file.
#    For example, for ADP, the memory file is ${HOME}\.vips\last-prohibition-number-adp.txt.
#
# 4) With a record type and no record number. Example:
#
#    > .\get-next-available-vips-number.ps1 [ADP|IRP|UL|IMP]
#    > .\get-next-available-vips-number.ps1 adp
#
#    The script will get the last found record number from the memory file and check to see if it is
#    still available. If not, it will iterate the number until a new record number is found.
#

param (
    [string] $NUMBER_TYPE,             # Example: ADP, IRP, UL, or IMP. Or empty
    [string] $SPECIFIED_NUMBER,        # Example: 00123456. Or empty.
    [string] $ENVIRONMENT = "DEV"      # Example, DEV, TEST. Defaults to DEV.
)

# Check to see if a value is numeric with regular expression
function Is-Numeric ($Value) {
    return $Value -match "^[\d\.]+$"
}

# Retrieve API credentials from OpenShift using supplied namespace, username, and password. Returns the HTTP header with basic creds.
function Create-ApiHeader() {
    param (
        $NAMESPACE,
        $USERNAME_SECRET,
        $PASSWORD_SECRET
    )
    # Set DF VI-IRP API credentials from OpenShift secrets in c220ad-dev
    $USERNAME64 = oc --namespace=${NAMESPACE} get secret digitalforms-api -o jsonpath="{.data.${USERNAME_SECRET}}"
    $PASSWORD64 = oc --namespace=${NAMESPACE} get secret digitalforms-api -o jsonpath="{.data.${PASSWORD_SECRET}}"
    $USERNAME   = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(${USERNAME64}))
    $PASSWORD   = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(${PASSWORD64}))
    $Headers    = @{ Authorization = "Basic {0}" -f [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f "${USERNAME}","${PASSWORD}"))) }
    return ${Headers}
}

# Exit if not logged in to OpenShift
oc whoami | out-null
if ( !$? ) { exit 2 } 

# Default variable
Set-Variable -Name "API_NAMESPACE"       -Value "c220ad-${ENVIRONMENT}".ToLower()
Set-Variable -Name "API_SECRET_USERNAME" -Value "DIGITALFORMS_BASICAUTH_USER"
Set-Variable -Name "API_SECRET_PASSWORD" -Value "DIGITALFORMS_BASICAUTH_PASSWORD"
Set-Variable -Name "MEMORY_FOLDER"       -Value "${HOME}\.vips"
Set-Variable -Name "MEMORY_FILE"         -Value "${MEMORY_FOLDER}\next-document-number-${ENVIRONMENT}.txt"
Set-Variable -Name "DOCUMENT_NUMBER"  -Value ""


# If the first argument was given, it could be numeric (an record number) or alphanumeric (an record type).
# For example "00123456" or "ADP"/"IRP"/"UL"/"IMP".
if (-Not [string]::IsNullOrEmpty(${NUMBER_TYPE}))
{
    # e.g. "00123456"
    if (Is-Numeric ${NUMBER_TYPE})
    {
        #Write-Host "Numeric first argument: ${NUMBER_TYPE}"
        $INTEGER = [int]${NUMBER_TYPE}
        Set-Variable -Name "DOCUMENT_NUMBER" -Value ${INTEGER}
    }
}

# If no number was given on the command-line, get it from a memory file
if ([string]::IsNullOrEmpty(${DOCUMENT_NUMBER}))
{
    # If no memory file, prompt for a number
    if (-Not (Test-Path -Path ${MEMORY_FILE} -PathType Leaf)){
        Write-Host "You must give a starting number to search. For example '15' to starting iterating, looking for a free document number."
        exit(3)
    }
    else {
        $FILE_CONTENT = Get-Content -Path ${MEMORY_FILE}
        $INTEGER = [int]${FILE_CONTENT}
        Set-Variable -Name "DOCUMENT_NUMBER" -Value ${INTEGER}
    }
}

# Sanity-check document number. Can only be eight numbers long.
if (${DOCUMENT_NUMBER} -gt 99999999 -Or ${SPECIFIED_NUMBER}.Length -gt 8)
{
    Write-Host "document number should be maximum of 8 characters. You gave: '${DOCUMENT_NUMBER}'."
}

# Generate API request header using nampespace secrets
${Headers} = Create-ApiHeader ${API_NAMESPACE} ${API_SECRET_USERNAME} ${API_SECRET_PASSWORD}

# Iterate DF VI-IRP API document numbers until an HTTP 404 indicates an unused record number
while(1)
{
    # Request document number from DF VI-IRP API
    try {
        $NUMBER = [string]${DOCUMENT_NUMBER}
        #Write-Host "Checking document ${DOCUMENT_NUMBER}..."

        $URL = "https://digitalforms-viirp-api-${API_NAMESPACE}.apps.silver.devops.gov.bc.ca/digitalforms-viirp/v1/documents/${NUMBER}/searching-for-next-available-document"
        #Write-Host "Invoke-WebRequest -UseBasicParsing -Method GET -Headers ${Headers} '${URL}' | Out-Null"
        $Resp = Invoke-WebRequest -UseBasicParsing -Method GET -Headers ${Headers} "${URL}" | Out-Null
        $Resp.ResponseCode
    } 
    catch {
        #Write-Host "${DOCUMENT_NUMBER} not found: HTTP " $_.Exception.Response.StatusCode.Value__
        break
        # An HTTP 404 indicates an available document number. This is what we want.
        #if ($_.Exception.Response.StatusCode.Value__ -eq 404) {
        #    #Write-Host "Returned 404: ${NUMBER}"
        #    break
        #}
        # A non-HTTP 200 response indicates a server or user issue. Stop looping.
        # elseif ($_.Exception.Response.StatusCode.Value__ -ne 200) {
        #     Write-Host "Server returned HTTP $_"
        #     ${ResponseCode} = $_.Exception.Response.StatusCode.Value__
        #     "HTTP ${ResponseCode}"
        #     exit(1)
        #}
    }

    ${DOCUMENT_NUMBER}+=1
}

# Ensure formatting for record numbers with leading zeros (ADP, IMP)
$NUMBER

# Save the document number so we don't need to iterate over already checked numbers
if (-Not (Test-Path -Path ${MEMORY_FOLDER} -PathType Container)){
    New-Item -Path "${MEMORY_FOLDER}" -ItemType Directory
}
# Create or update the memory file
${NUMBER} | Out-File -FilePath ${MEMORY_FILE}
