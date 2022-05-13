# Digital Forms 12/24 web service tests in Robot Framework

Set up to run this script:

1. Log in to OpenShift. Select namespace -dev or -test. 
2. Forward a local port to the web service pod. For example, 5009:
   $ oc port-forward services/web-service-dev 5009:5000 -n abc123-dev
3. Set the Python virtual environment to one with Robot Framework and requests library.
   $ workon tfapi
4. Run this script with the wrapper:
   $ ./run-dfttfws-regression-test.robot

Example of calling the API manually with HTTPie:
    $ http :5009/api/v1/colors

Example of calling the API manually, with authentication credentials:
    $ http :5009/api/v1/colors --auth ${USERNAME}:${PASSWORD}

Example of calling the API using a KeyCloak bearer token harvested from browser developer tools:
    $ http :5009/api/v1/colors authorization:"${OFFICER_TOKEN}"


NOTES FOR THE FUTURE, 2021-12

1. HTTP response header includes gunicorn/20.0.4 (information disclosure vulnerability?)
2. HTTP OPTIONS shows that GET, POST, OPTIONS, HEAD are supported, but not all methods are successful.
3. Check non-existent page (404 error page).
4. 2021-12-22, POSTing with no body returns HTTP 500 error. Stack trace in log reports "document is missing"
   Example: http POST :5009/api/v1/admin/forms --auth ${USERNAME}:${PASSWORD}
5. Fuzz API inputs.
6. Creating a duplicate form returns an HTTP 500 instead of something more appropriate. Console log shows SQLite3 integrity error:
   2021-12-22 21:10:04,383::WARNING::root::{'form_id': 'steve1', 'form_type': 'IRP'}                        
   (Background on this error at: http://sqlalche.me/e/13/gkpj)                                              
   2021-12-22 21:10:04,409::WARNING::root::(sqlite3.IntegrityError) column id is not unique                 
   [SQL: INSERT INTO form (id, form_type, lease_expiry, printed_timestamp, username) VALUES (?, ?, ?, ?, ?)]
   [parameters: ('steve1', 'IRP', None, None, None)]             
7. Time zone shows as GMT in admin panel, but times shown in Pacific time:
   https://rsbc-dh-prohibition-web-app-dev.apps.silver.devops.gov.bc.ca/admin
8. Test what happens if the web service pod gets evicted or re-deployed. Does in-memory user database get erased?
9. /api/v1/admin/users/<username>/roles/<role> PATCH does not seem to make changes to the user roles.
10. /api/v1/admin/users/<username>/roles/<role> DELETE returns type text/html but body is "okay"
11. Server 500 error deleteing role that does not exist. Should be a 400-level error.
12. OPTIONS requests for does not include PATCH or DELETE.
13. HEAD requests return HTTP 500 error.
14. Check token not valid after signed out from forms UI.
15. Try GET requests where at item does not exist. Check for 404 or empty response.


## More documentation:

For Digital Forms 12/24 web service API documentation, see wiki page:
https://justice.gov.bc.ca/wiki/pages/viewpage.action?pageId=314671737
