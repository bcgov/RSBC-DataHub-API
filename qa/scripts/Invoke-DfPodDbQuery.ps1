<#
.SYNOPSIS
Query BI database pod. Requires SqlServer module. Returns results in an object: System.Data.DataRow so you can
pipe the results to CmdLets like Format-Wide, Format-List, Format-Table, or process with ForEach-Object.

.DESCRIPTION
Runs a query on the BI datbase pod and returns results.
Note: Must be logged in to OpenShift to ensure script can connect to pod and retrieve API credentials.

.PARAMETER Sql
Structure Query Language query. For example "\d" or "select * from vph_interfaces".

.PARAMETER Environment
The OpenShift environment to use: either DEV or TEST. If omitted, will default to the TEST environment.

.PARAMETER Verbose
Print details about what the script is doing.

.LINK
None

.EXAMPLE
PS> Invoke-BiDbQuery.ps1 "select * from etk.agencies;"

.EXAMPLE
PS> Invoke-BiDbQuery.ps1 "select * from etk.issuances where ticket_number like 'EZ020%' and submit_date = '2022-11-24'" -Verbose

.EXAMPLE
PS> .\Invoke-BiDbQuery.ps1 "select * from etk.agencies;" | Format-Table

.EXAMPLE
PS> .\Invoke-BiDbQuery.ps1 "select * from etk.agencies;" | ForEach-Object { "$($_.enforcement_jurisdiction_code.ToString()), $($_.enforcement_jurisdiction_name.ToString())"}

.EXAMPLE
PS> $Result = .\Invoke-BiDbQuery.ps1 "select * from etk.agencies;"
    $Result.enforcement_jurisdiction_name

.EXAMPLE
PS> $Result = .\Invoke-BiDbQuery.ps1 "select * from etk.agencies"
foreach($row in $Result){Write-Host $row.enforcement_jurisdiction_code.ToString(), $row.enforcement_jurisdiction_name.ToString()}

.EXAMPLE
PS> .\Invoke-BiDbQuery.ps1 2022-11-17

.EXAMPLE
PS> .\Invoke-BiDbQuery.ps1 EZ02005044
#>

param(
    [string]$Sql,
    [string]$Environment,
    [switch]$Verbose
)

function KubernetesTokenIsValid {
    oc whoami 2>&1 | Out-Null
    return $?
}

function Invoke-DfPodDbQuery {
    param(
        [string]$Sql,
        [string]$Environment
    )

    Begin {
        Set-Variable -Name "DefaultEnv" -Value "dev"
        Set-Variable -Name "OcNamespace" -Value "be78d6" # OpenShift project licence plate

        if (-Not ${Environment}) {
            Set-Variable -Name "Environment" -Value ${DefaultEnv}
            Set-Variable -Name "OcSecret" -Value "rsbc-dh-prohibition-web-svc-${Environment}"
        }


        # Ensure OpenShift token is valid
        if (!(KubernetesTokenIsValid))
        {
            if (Get-Command aili)
            {
                aili
            }
            else
            {
                Write-Host "OpenShift/Kubernetes token has expired. Cannot retrieve database credentials."
                exit 1
            }
        }

        $Namespace = "${OcNamespace}-${Environment}"
    }

    Process {
        if (${Verbose})
        {
            Write-Host "oc exec --namespace=$Namespace svc/rsbc-dh-prohibition-web-svc-${Environment} -- /usr/bin/sqlite3 /var/lib/sqlite/sqlite.db '${Sql}'"
        }

        oc exec --namespace=$Namespace svc/rsbc-dh-prohibition-web-svc-${Environment} -- /usr/bin/sqlite3 /var/lib/sqlite/sqlite.db "${Sql}"
    }
}

function Print-QueryResults {
    param(
        [string]$QueryName,
        [string]$Sql,
        [string]$Format
    )

    $Results = Invoke-BiDbQuery -Sql "$Sql" -Environment $Environment
    Write-Host "${QueryName}: " ${Results}.count

    if (${Format} -eq "list") {
        ${Results} | Format-List
    }
    elseif (${Format} -eq "table") {
        ${Results} | Format-Table
    }
    elseif (${Format} -eq "wide") {
        ${Results} | Format-Wide
    }
}


function Make-Df-Summary {
    param(
        [string]$FormNumber
    )

    $Issuance = Invoke-DfPodDbQuery -Sql "select * from form where id = '${FormNumber}'" -Environment $Environment
    Write-Host ""
    $Issuance
}


# Print help if no parameter was given
if (-Not ${Sql}){
   Get-Help $MyInvocation.MyCommand -Examples
   exit 1
}

# If it's a form number, show form information
if ($Sql.StartsWith('JZ') -Or $Sql.StartsWith('VZ') -Or $Sql.StartsWith('99')) {
    Make-Df-Summary ${Sql}
    exit 0
}
# Just a regular SQL query
else {
    Invoke-DfPodDbQuery -Sql $Sql -Environment $Environment
}

