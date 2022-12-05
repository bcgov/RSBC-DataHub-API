# Functions module

# Useful stuff:
# Type Get-Module to show current modules
# Remove modules with Remove-Module
# See location with $Env:PSModulePath

function Test-LoggedInToOpenShift {
    ($me = oc whoami) | out-null
    if (-Not $me) {
        Write-Host "Not logged in to OpenShift. Cannot continue."
        exit 3
    }
    return $me
}

function Test-Installed {
    param (
        # Used to invoke command with CLI
        $CommandName,
        $FailureMessage
    )

    $Command = Get-Command $CommandName
    if (-Not $Command)
    {
        Write-Host "$Command is not installed. Cannot continue."
        if ($FailureMessage){
            Write-Host "Potential fix: $FailureMessage"
        }
        exit 1
    }
}

function Test-FilePresent
{
    param (
        $FilePath,
        $FailureMessage
    )

    $FileExists = Test-Path -Path $FilePath
    if (-Not $FileExists)
    {
        Write-Host "File $FilePath not found. Cannot continue."
        if ($FailureMessage){
            Write-Host "Potential fix: $FailureMessage"
        }
        exit 2
    }
}