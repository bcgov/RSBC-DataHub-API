# PowerShell script to start a local web server using WebServer:
# https://github.com/MScholtes/WebServer
#
# Install with:
# > Install-Module WebServer

# Start server with:
# > Start-Webserver

Write-Output "Access content with local URL. For example:"
Write-Output " - http://localhost:8088/rsf-view.js"
Write-Output ""

Write-Output "Stop server by accessing '/quit' URI: http://localhost:8088/quit"
Write-Output "More information: https://github.com/MScholtes/WebServer"
Write-Output ""

Start-Webserver "http://127.0.0.1:8088/"