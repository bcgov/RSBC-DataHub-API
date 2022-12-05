param(
    [switch]$DEV,
    [switch]$TEST,
    [switch]$PROD,
    [switch]$Verbose
)

$pathToOcCommand = "${HOME}\Sync\Apps\"
$pathToAili = "${HOME}\Sync\Projects\idir\aili.ps1"
$OcLicencePlate = "be78d6"

# Calls AILI script (AILI stands for "Am I logged in?")
function Get-New-Token-If-Needed {
    # If the auto log in script is present, call it
    if (Test-Path -Path ${pathToAili} -PathType Leaf) {
        Invoke-Expression ${pathToAili} | Out-Null
        # If script exited with an error, exit
        if (!${?}) {  
            Write-Host "${pathToAili} failed. Exiting..."
            exit 2
        }
    }
}

function Watch-DfSvcLog {
    param(
        [string]$Namespace,
        [string]$ServiceName
    )

    Begin {
        Set-Variable -Name "DefaultEnv" -Value "dev"
    }

    Process {
        oc --namespace=${Namespace} logs svc/${ServiceName} | Select-String -NotMatch -Pattern InsecureRequestWarning
    }    
}

if (${DEV}) {
    $Environment = "dev"
}
elseif (${TEST}) {
    $Environment = "test"
}
elseif (${PROD}) {
    $Environment = "prod"
}
else {
    Write-Host "Unknown environment. Use one of -DEV, -TEST, or -PROD."
    exit 2
}

Watch-DfSvcLog -Namespace "${OcLicencePlate}-${Environment}" -ServiceName "rsbc-dh-prohibition-web-app-${Environment}"

