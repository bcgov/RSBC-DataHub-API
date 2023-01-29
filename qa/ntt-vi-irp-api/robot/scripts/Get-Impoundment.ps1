# Get a impoundment record from DEV
<#
.SYNOPSIS
    Retrieve impoundment from VIPS using the DF VI-IRP API.

.DESCRIPTION
    Calls the DF VI-IRP API endpoint GET /v1/impoundments/correlation endpoint to retrieve a VIPS impoundment.

.PARAMETER ServerUri
The URI for the server. If omitted, will default to the DEV environment.

.PARAMETER Environment
The OpenShift environment to use: either DEV or TEST. If omitted, will default to the DEV environment.

.PARAMETER Verbose
Print details about what the script is doing.

.EXAMPLE
PS> .\Get-Impoundment.ps1 22197503

#>

param (
    [string] $ImpoundmentNumber,      # Example: 00197501
    [string] $Environment,
    [string] $ServerUri,
    [switch] $Format,
    [switch] $Verbose
)

function KubernetesTokenIsValid {
    oc whoami 2>&1 | Out-Null
    return $?
}

function Get-Impoundment {
    param (
        [string] $ImpoundmentNumber,      # Example: 00197501
        [string] $Environment,
        [string] $ServerUri,
        [switch] $Format,
        [switch] $Verbose
    )

    Begin {
            Set-Variable -Name "DefaultEnv" -Value "dev"
            Set-Variable -Name "OcNamespace" -Value "c220ad"
            Set-Variable -Name "OcUsernameSecret" -Value "DIGITALFORMS_BASICAUTH_USER"
            Set-Variable -Name "OcPasswordSecret" -Value "DIGITALFORMS_BASICAUTH_PASSWORD"
            Set-Variable -Name "ApiPath" -Value "v1/impoundments"
            Set-Variable -Name "Correlation" -Value "GetImpoundment"

        if (-Not ${Environment}) {
            Set-Variable -Name "Environment" -Value ${DefaultEnv}
        }

        if (-Not ${ServerUri}) {
            Set-Variable -Name "ServerUri" -Value "https://digitalforms-viirp-api-${OcNamespace}-${Environment}.apps.silver.devops.gov.bc.ca/digitalforms-viirp/${ApiPath}/${ImpoundmentNumber}/${Correlation}"
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

        if (${Verbose}) { 
            Write-Host "Calling:      ${ServerUri}"
        }
    }

    Process {
        try {
            $Response = Invoke-WebRequest -UseBasicParsing -Method GET -Headers $Headers ${ServerUri}
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
    $StatusCode, $Response = Get-Impoundment -ServerUri ${ServerUri} -Environment ${Environment} -ImpoundmentNumber ${ImpoundmentNumber} -Verbose
}
else {
    $StatusCode, $Response = Get-Impoundment -ServerUri ${ServerUri} -Environment ${Environment} -ImpoundmentNumber ${ImpoundmentNumber}
}

if (${StatusCode} -ne 200) {
    if (${Verbose}) {
        Write-Host "HTTP ${StatusCode}: unsuccessful."
    }
    exit ${StatusCode}
}

if (${Verbose}) {
    Write-Host "HTTP 200: successful."
}

return ${Response}
