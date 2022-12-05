*** Settings ***
Documentation    Testing for NTT DF VI-IRP API
Library    JSONLibrary
Library      RequestsLibrary  # https://github.com/MarketSquare/robotframework-requests
Library      Collections      # Used to check header response from RequestsLibrary
Library      String           # https://robotframework.org/robotframework/latest/libraries/String.html
Library      Process          # https://robotframework.org/robotframework/latest/libraries/Process.html
Library      OperatingSystem  # https://robotframework.org/robotframework/latest/libraries/OperatingSystem.html
Library      DateTime         # https://robotframework.org/robotframework/latest/libraries/DateTime.html

Resource   lib/keywords.resource        # Keywords
Resource   lib/kw-requests.resource     # Keywords for server requests
Resource   lib/kw-responses.resource    # Keywords for server responses

Suite Setup     Create DF VI-IRP API sessions