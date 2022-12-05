<#
.SYNOPSIS
    Creates a new prohibition prohibition in VIPS using the DF VI-IRP API.

.DESCRIPTION
    Calls the DF VI-IRP API endpoint POST /v1/prohibitions/correlation endpoint to create a new VIPS prohibition.

.PARAMETER ServerUri
The URI for the server. If omitted, will default to the DEV environment.

.PARAMETER Environment
The OpenShift environment to use: either DEV or TEST. If omitted, will default to the DEV environment.

.PARAMETER TemplateFile
JSON payload template file path.

.PARAMETER ProhibitionType
The type of prohibition to create (ADP, IRP, UL).

.PARAMETER Verbose
Print details about what the script is doing.

.EXAMPLE
PS> .\Create-Prohibition.ps1 -ProhibitionType irp

.EXAMPLE
PS> .\Create-Prohibition.ps1 -environment dev -verbose
#>

param(
    [string]$ServerUri,
    [string]$Environment,
    [string]$TemplateFile,
    [string]$ProhibitionType,
    [switch]$Verbose
)

function KubernetesTokenIsValid {
    oc whoami 2>&1 | Out-Null
    return $?
}

function Create-Prohibition {
    param(
        [string]$ServerUri,
        [string]$Environment,
        [string]$TemplateFile,
        [string]$ProhibitionType,
        [switch]$Verbose
    )

    Begin {
            Set-Variable -Name "DefaultEnv" -Value "dev"
            Set-Variable -Name "OcNamespace" -Value "c220ad"
            Set-Variable -Name "OcUsernameSecret" -Value "DIGITALFORMS_BASICAUTH_USER"
            Set-Variable -Name "OcPasswordSecret" -Value "DIGITALFORMS_BASICAUTH_PASSWORD"
            Set-Variable -Name "ApiPath" -Value "v1/prohibitions"
            Set-Variable -Name "Correlation" -Value "CreateProhibition"
            Set-Variable -Name "DefaultProhibitionType" -Value "ADP"
            
        if (-Not ${ProhibitionType}) {
            Set-Variable -Name "ProhibitionType" -Value ${DefaultProhibitionType}
        }

        # Ensure prohibition type is one of: ADP, IRP, UL
        if (-Not ((${ProhibitionType}.ToUpper() -eq "ADP") -Or 
            (${ProhibitionType}.ToUpper() -eq "IRP") -Or
            (${ProhibitionType}.ToUpper() -eq "UL"))) {
            Write-Host "The -ProhibitionType parameter must be one of 'ADP', 'IRP', or 'UL', not:"${ProhibitionType}.ToUpper()
            exit 3
        }

        if (-Not ${Environment}) {
            Set-Variable -Name "Environment" -Value ${DefaultEnv}
        }

        if (-Not ${ServerUri}) {
            Set-Variable -Name "ServerUri" -Value "https://digitalforms-viirp-api-${OcNamespace}-${Environment}.apps.silver.devops.gov.bc.ca/digitalforms-viirp/${ApiPath}/${Correlation}"
        } 

        if (-Not ${TemplateFile}) {
            Set-Variable -Name "TemplateFile" -Value "${HOME}\Sync\Projects\df\RSBC-DataHub-API\qa\ntt-vi-irp-api\robot\lib\new-prohibition-payload-example.json"
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
        $NextNumber = .\Get-NextProhibition.ps1 ${ProhibitionType}
        #$NextNumber = "00197575"
        Write-Host "Submitting prohibition" ${ProhibitionType}.ToUpper() "${NextNumber}..."
        $Payload = Get-Content -Raw -Path ${TemplateFile} | ConvertFrom-Json
        $Payload.vipsProhibitionCreate.prohibitionNoticeNo = ${NextNumber}
        $Payload.vipsProhibitionCreate.incidentDtm = Get-Date -UFormat "%Y-%m-%dT00:00:00.000%Z:00"
        $Payload.vipsProhibitionCreate.effectiveDt = Get-Date -UFormat "%Y-%m-%dT00:00:00.000%Z:00"
        $Payload.vipsProhibitionCreate.noticeServedDt = Get-Date -UFormat "%Y-%m-%dT00:01:23.100%Z:00"
        $Payload.vipsRegistrationCreate.vipsLicenceCreateObj.birthDt = "1975-07-05T00:00:00.000-07:00"
        $Payload.vipsProhibitionCreate.noticeTypeCd = ${ProhibitionType}.ToUpper()

        $PayloadJson = ${Payload} | ConvertTo-Json -Compress -Depth 5

        if (${Verbose}) { 
            Write-Host "Calling:      ${ServerUri}"
            Write-Host "POST payload: ${PayloadJson}"
        }
    }

    End {
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
    $StatusCode, $Response = Create-Prohibition -ServerUri ${ServerUri} -Environment ${Environment} -ProhibitionType ${ProhibitionType} -TemplateFile ${TemplateFile} -Verbose
}
else {
    $StatusCode, $Response = Create-Prohibition -ServerUri ${ServerUri} -Environment ${Environment} -ProhibitionType ${ProhibitionType} -TemplateFile ${TemplateFile} 
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
