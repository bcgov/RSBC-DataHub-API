# DFAPI intuitive test script

A semi-automated test script for use with Visual Studio Code with the REST Client plug-in. It only works in VSCode with REST Client. But it makes it very easy to make calls to the DFAPI from a remote shell on a pod in the DEV or TEST namespace.

Right-click a REST call in Visual Studio and select "Copy CURL command" from the context menu. Paste it into the remote shell and review the response in the console.

To set up DEV and TEST environments, use this template to create environment variables in settings.json. For more information and examples, see the "Environment Variables" section of the [documentation for REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

    "rest-client.environmentVariables": {

        "$shared": {
            "TESTER_EMAIL_ADDRESS": "YOUR_EMAIL_HERE, SO YOU RECEIVE NOTIFICATIONS",
            "FAX_NO": "",
            "PHONE_NO": "",
            "FIRST_GIVEN_NAME": "",
            "SECOND_GIVEN_NAME": "",
            "SURNAME": "",
            "FORM_DATA": "BASE64_ENCODED_FORM_STRING",
            "MANUAL_ENTRY": "",
            "NOTICE_SUBJECT": ""
        },
        "DFAPI-DEV": {
            // NOTE: Prohibitions created in DFAPI DEV environment DO NOT show up in VIPS DEV environment, and vice-versa.
            "ORDS_DELETE_APPLICATION_URL": "",
            "ORDS_DELETE_APPLICATION_AUTH": "",
            "ORDS_DELETE_REVIEW_TIME_URL": "",
            "DFAPI_URL": "",
            "CREDENTIALS": "",

            // ADP (uncomment to use)
            // -------------------------------------------------------------
            "FORM_TYPE": "ADP",
            "NOTICE_NUMBER": "",
            "PROHIBITION_ID": "",
            "application_id": "",
            "PRESENTATION_TYPE": "", 
            "REVIEW_ROLE_TYPE": "",
            "DOCUMENT_ID": ""

            // IRP (uncomment to use)
            // -------------------------------------------------------------
            //"FORM_TYPE": "IRP",
            // "NOTICE_NUMBER": "",
            // "PROHIBITION_ID": "",
            // "application_id": "",
            // "PRESENTATION_TYPE": "", 
            // "REVIEW_ROLE_TYPE": "",
            // "DOCUMENT_ID": ""

            // UL (uncomment to use)
            // -------------------------------------------------------------
            // "FORM_TYPE": "UL",
            // "NOTICE_NUMBER": "",
            // "PROHIBITION_ID": "",
            // "application_id": "",
            // "PRESENTATION_TYPE": "", 
            // "REVIEW_ROLE_TYPE": "",
            // "DOCUMENT_ID": ""
        },
        "DFAPI-TEST": {

            "ORDS_DELETE_APPLICATION_URL": "",
            "ORDS_DELETE_APPLICATION_AUTH": "",
            "ORDS_DELETE_REVIEW_TIME_URL": "",
            "DFAPI_URL": "",
            "CREDENTIALS": "",

            // ADP (uncomment to use)
            // -------------------------------------------------------------
            "FORM_TYPE": "ADP",
            "NOTICE_NUMBER": "",
            "PROHIBITION_ID": "",
            "DOCUMENT_ID": "",
            "application_id": "",
            "PRESENTATION_TYPE": "", 
            "REVIEW_ROLE_TYPE": "",


            // IRP (uncomment to use)
            // -------------------------------------------------------------
            // "FORM_TYPE": "IRP",
            // "NOTICE_NUMBER": "",
            // "PROHIBITION_ID": "",
            // "DOCUMENT_ID": "",
            // "application_id": "",
            // "PRESENTATION_TYPE": "", 
            // "REVIEW_ROLE_TYPE": "",

            // UL (uncomment to use)
            // -------------------------------------------------------------
            // "FORM_TYPE": "UL",
            // "NOTICE_NUMBER": "",
            // "PROHIBITION_ID": "",
            // "DOCUMENT_ID": "",
            // "application_id": "",
            // "PRESENTATION_TYPE": "", 
            // "REVIEW_ROLE_TYPE": "",
        },
