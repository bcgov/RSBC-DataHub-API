*** Settings ***
Library  OperatingSystem
Library  SeleniumLibrary
Library  Process
Library  String

*** Variables ***
${FORMS_URL}       https://dev.jag.gov.bc.ca/roadside-forms/
${FORMS_USERNAME}  STest9
${FORMS_PASSWORD}  
${LOG_FOLDER}      logs

*** Test Cases ***
Log in to forms web app
	Start browser
    Log in with BCeID
    Wait until page contains  We'd welcome your suggestions for how to improve this app.  timeout=30
    Inject JavaScript
#    Close browser

*** Keywords ***

Inject JavaScript
    # Call Selenuim Api  
    Execute Javascript  window.document.getElementById('MV2634')
    # See examples of executing JavaScript: https://stackoverflow.com/a/62821648
    # Note that, by default, the code will be executed in the context of the Selenium object itself, so this will refer to the Selenium object. Use window to refer to the window of your application, e.g. window.document.getElementById('foo').
    Execute JavaScript  C:\Users\User\Sync\Projects\df\RSBC-DataHub-API\qa\roadside-forms\form-automation-js\rsf-model.js
    Execute JavaScript  C:\Users\User\Sync\Projects\df\RSBC-DataHub-API\qa\roadside-forms\form-automation-js\form-record-01.js
    Execute JavaScript  C:\Users\User\Sync\Projects\df\RSBC-DataHub-API\qa\roadside-forms\form-automation-js\form-record-02.js
    Execute JavaScript  C:\Users\User\Sync\Projects\df\RSBC-DataHub-API\qa\roadside-forms\form-automation-js\rsf-controller.js
    Execute JavaScript  C:\Users\User\Sync\Projects\df\RSBC-DataHub-API\qa\roadside-forms\form-automation-js\rsf-view.js
    Execute Javascript    alert(arguments[0]);    ARGUMENTS    123 


Start Browser
	[Documentation]  Invoke headless browser with a user profile for automation. The profile is set to proxy requests to localhost port ${PROXY_LISTEN_PORT}, and includes the BrowserMob certificate authority certificate, to man-in-the-middle TLS connections. This should also work with PhantomJS (support for which is deprecated in Robot Framework) and Chrome headless. Note that the window size needs to be quite wide (1080p width) in order not to have CSS controls obscured by overlays in the the Awair dashboard.
	Open Browser  ${FORMS_URL}  Edge  #headlessfirefox  ff_profile_dir=${FIREFOX_PROFILE}
	Set Window Size    1920    1080
    Wait until page contains  Welcome!  timeout=30
	Capture page screenshot  ${LOG_FOLDER}/01-landing-page.png

Log in with BCeID
    Wait Until Element Is Visible  link:Login
    Click Link  link:Login
    Wait Until Element Is Visible  link:Business BCeID
    Capture page screenshot  ${LOG_FOLDER}/02-authentication-type.png
    Click Link  link:Business BCeID
    Enter BCeID Credentials  ${FORMS_USERNAME}  ${FORMS_PASSWORD}

Enter BCeID credentials
	[Documentation]  Logs in to the dashboard using the supplied credentials. These xpaths may change as the dashboard is updated, so expect these to fail occasionally. We may want to submit a request to have the dashboard buttons tagged with ids.
	[Arguments]  ${username}  ${password}
    Wait until page contains  Register for a BCeID
	Input text  id=user  ${username}
	Input text  id=password  ${password}
	Capture page screenshot  ${LOG_FOLDER}/credentials-entered.png
	Click Button  Continue
	

