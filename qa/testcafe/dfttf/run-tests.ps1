# Wrapper script for calling the Digital Forms 12/24 web app front-end tests with TestCafe in PowerShell.

# Set environvment variables for the test script here. For example, 
# the URL of the server being tested, and test usernames and passwords.
Set-Variable -Name EnvironmentVariablesFile -Value .env.ps1

# Command to start the TestCafe script
Set-Variable -Name RunTestCafeCommand -Value "npm run test:edge"

# Ensure environment variables for user accounts and URLs are configured
if (-Not(Test-Path -Path $EnvironmentVariablesFile)) {
    Write-Host "Could not find $EnvironmentVariablesFile environment variables. Please copy $EnvironmentVariablesFile-template to $EnvironmentVariablesFile, configure it, and re-run this script."
    Exit 1
}

$EnvironmentVariablesFile
npm run test:edge
