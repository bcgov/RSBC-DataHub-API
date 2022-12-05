<#
.SYNOPSIS
    Creates a new document in VIPS using the DF VI-IRP API.

.DESCRIPTION
    Calls the DF VI-IRP API endpoint POST /v1/document/correlation endpoint to create a new VIPS document.

.PARAMETER ServerUri
The URI for the server. If omitted, will default to the DEV environment.

.PARAMETER Environment
The OpenShift environment to use: either DEV or TEST. If omitted, will default to the DEV environment.

.PARAMETER PdfBase64
A base64-encoded string from a PDF. If omitted, a small placeholder PDF will be used instead.

.PARAMETER DocumentId
An explicit document id to use for creation. If omitted, the next available document number will be used.

.PARAMETER DocumentType
The type of document to create.

.PARAMETER NoticeType
The type of notice to use when creating the document (ADP, IRP, UL, IMP).

.EXAMPLE
PS> .\Create-Document.ps1

.EXAMPLE
PS> .\Create-Document.ps1 -noticetype imp -environment dev -verbose
#>

param(
    [string]$ServerUri,
    [string]$Environment,
    [string]$PdfBase64,
    [string]$DocumentType,
    [string]$NoticeType,
    [string]$SubjectCode,
    [switch]$Verbose
)

function KubernetesTokenIsValid {
    oc whoami 2>&1 | Out-Null
    return $?
}

function Create-Document {
    <#
        .SYNOPSIS
            Creates a new document in VIPS using the DF VI-IRP API.

        .DESCRIPTION
            Calls the DF VI-IRP API endpoint POST /v1/document/correlation endpoint to create a new VIPS document.

        .PARAMETER ServerUri
        The URI for the server. If omitted, will default to the DEV environment.

        .PARAMETER Environment
        The OpenShift environment to use: either DEV or TEST. If omitted, will default to the DEV environment.

        .PARAMETER PdfBase64
        A base64-encoded string from a PDF. If omitted, a small placeholder PDF will be used instead.

        .PARAMETER DocumentId
        An explicit document id to use for creation. If omitted, the next available document number will be used.

        .PARAMETER DocumentType
        The type of document to create.

        .PARAMETER NoticeType
        The type of notice to use when creating the document (ADP, IRP, UL, IMP).
    #>

    param(
        [string]$ServerUri,
        [string]$Environment,
        [string]$PdfBase64,
        [string]$DocumentType,
        [string]$NoticeType,
        [string]$SubjectCode,
        [switch]$Verbose
    )

    Begin {
        Set-Variable -Name "DefaultEnv" -Value "dev"
        Set-Variable -Name "OcNamespace" -Value "c220ad"
        Set-Variable -Name "OcUsernameSecret" -Value "DIGITALFORMS_BASICAUTH_USER"
        Set-Variable -Name "OcPasswordSecret" -Value "DIGITALFORMS_BASICAUTH_PASSWORD"
        Set-Variable -Name "ApiPath" -Value "v1/documents"
        Set-Variable -Name "Correlation" -Value "CreateDocument"

        if (-Not ${Environment}) {
            Set-Variable -Name "Environment" -Value ${DefaultEnv}
        }

        if (-Not ${ServerUri}) {
            Set-Variable -Name "ServerUri" -Value "https://digitalforms-viirp-api-${OcNamespace}-${Environment}.apps.silver.devops.gov.bc.ca/digitalforms-viirp/${ApiPath}/${Correlation}"
        } 

        if (-Not ${PdfBase64}) {
            Set-Variable -Name "PdfBase64" -Value "JVBERi0xLjIgCjkgMCBvYmoKPDwKPj4Kc3RyZWFtCkJULyAzMiBUZiggIFlPVVIgVEVYVCBIRVJFICAgKScgRVQKZW5kc3RyZWFtCmVuZG9iago0IDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJlbnQgNSAwIFIKL0NvbnRlbnRzIDkgMCBSCj4+CmVuZG9iago1IDAgb2JqCjw8Ci9LaWRzIFs0IDAgUiBdCi9Db3VudCAxCi9UeXBlIC9QYWdlcwovTWVkaWFCb3ggWyAwIDAgMjUwIDUwIF0KPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1BhZ2VzIDUgMCBSCi9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iagp0cmFpbGVyCjw8Ci9Sb290IDMgMCBSCj4+CiUlRU9G"
        }

        if (-Not ${DocumentType}) {
            Set-Variable -Name "DocumentType" -Value "RACE"
        }

        if (-Not ${NoticeType}) {
            Set-Variable -Name "NoticeType" -Value "IMP"
        }

        if (-Not ${SubjectCode}) {
            Set-Variable -Name "SubjectCode" -Value "PERS"
        }

        if (${Env:Headers} -eq $null) {
            if (KubernetesTokenIsValid)
            {
                # Retrieve secret values from OpenShift/Kubernetes. Must be logged in.
                $USERNAME64 = oc --namespace=${OcNamespace}-${Environment} get secret digitalforms-api -o jsonpath="{.data.${OcUsernameSecret}}"
                $PASSWORD64 = oc --namespace=${OcNamespace}-${Environment} get secret digitalforms-api -o jsonpath="{.data.${OcPasswordSecret}}"
                # Build header with calculated Auth token
                $USERNAME   = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(${USERNAME64}))
                $PASSWORD   = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(${PASSWORD64}))
                $Headers    = @{ Authorization = "Basic {0}" -f [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes(("{0}:{1}" -f "${USERNAME}","${PASSWORD}"))) }

            }
            else {
                Write-Host "OpenShift/Kubernetes token has expired. Cannot retrieve API credentials."
                exit 1
            }
        }
    }

    Process {
        $Payload = @{
            "type_code" = "${DocumentType}"
            "mime_sub_type" = "pdf"
            "mime_type" = "application"
            "file_object" = "${TINY_PDF_BASE64}"
            "notice_type_code" = "${NoticeType}"
            "notice_subject_code" = "${SubjectCode}"
            "pageCount" = 1
        }
        $PayloadJson = ($Payload|ConvertTo-Json)

        if (${Verbose}) { 
            Write-Host "Calling:      ${ServerUri}"
            Write-Host "POST payload: ${PayloadJson}"
        }

        try {
            $Response = Invoke-WebRequest -UseBasicParsing -Method POST -ContentType "application/json" -Headers $Headers -Body ${PayloadJson} ${ServerUri}
            return ${Response}.StatusCode, $Response.Content
        }
        catch {
            $ReturnCode = $_.Exception.Response.StatusCode.Value__
            $Error = $_.ErrorDetails.Message
            return ${ReturnCode}, ${Error}
        }
    }
}

# Invoke function with or without Verbose switch
if (${Verbose}) {
    $StatusCode, $Response = Create-Document -ServerUri ${ServerUri} -Environment ${Environment} -PdfBase64 ${PdfBase64} -DocumentId ${DocumentId} -DocumentType ${DocumentType} -NoticeType ${NoticeType} -NoticeCode ${NoticeCode} -Verbose
}
else {
    $StatusCode, $Response = Create-Document -ServerUri ${ServerUri} -Environment ${Environment} -PdfBase64 ${PdfBase64} -DocumentId ${DocumentId} -DocumentType ${DocumentType} -NoticeType  -NoticeCode ${NoticeCode} ${NoticeType}
}
 
Write-Host ${Response}

if (${StatusCode} -ne 200) {
    if (${Verbose}) {
        Write-Host "HTTP ${StatusCode}: unsuccessful."
    }
    exit ${StatusCode}
}

if (${Verbose}) {
    Write-Host "HTTP 200: successful."
}
