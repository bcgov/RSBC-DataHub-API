# DFAPI regression testing


These scripts allow for fast and easy testing of the Digital Forms API. There are several scripts:

- [dfapi-intuitive.http](file://dfapi-intuitive.http): a "REST Client" script for intuitive, exploratory, semi-automated regression testing. See [dfapi-intuitive.md](file://dfapi-intuitive.md) for an overview.
- [dfapi.robot](file://dfapi.robot): a Robot Framework suite for fully automated regression testing.
- [remote-run.sh](file://remote-run.sh): a Bash wrapper to copy the Robot Framework script onto a pod, run the script, and retrive the logs.

More examples and information:
- Wiki for DFAPI testing:      https://justice.gov.bc.ca/wiki/pages/viewpage.action?pageId=257917165&src=contextnavpagetreemode
- Expected fields and values:  https://justice.gov.bc.ca/wiki/display/RDFP/DFAPI:+submission+fields+and+expected+values
- ORDS endpoint documentation: https://justice.gov.bc.ca/wiki/display/RDFP/Digital+Forms+API:+ORDS+helper+endpoints

When running this script, you need to set up a pod in the -DEV, -TEST, or -PROD environment. This is because the DFAPI is not accessible from outside the namespaces (from the internet). Its security rules allow only traffic from authorised Kubernetes namespaces only. See [this wiki page](https://justice.gov.bc.ca/wiki/display/RDFP/DFAPI%3A+only+accessible+from+inside+DEV+and+TEST+namespaces) for more information and examples.

## Install Robot Framework on OpenShift pod

See the wiki page for [Testing with OpenShift pods](https://justice.gov.bc.ca/wiki/display/RDFP/Testing+with+OpenShift+pods) for instructions on how to create a temporary pod in the DEV or TEST namespaces. You can then install Robot Framework and other tools for testing.

## Run Robot Framework script on OpenShift pod

You can manually sync the files in this folder with a pod like this:

    # Copy current folder to pod
    $ oc rsync . temporary-test-pod:

    # Run the script on the pod
    $ kubectl exec temporary-test-pod -- robot --loglevel DEBUG --debugfile dfapi.log --outputdir ./results ./dfapi.robot

    # Copy the results from your pod to the local machine
    oc rsync temporary-test-pod:./results .

Copy the test script from your local machine to the pod using the supplied script

    $ ./remote-run.sh

## Open results HTML in local browser from WSL with a URL like this:

Adjust the path to suite your environment. This example references a folder in WSL2.

- file://///wsl.localhost/Ubuntu/home/user/dfapi/results/log.html


## TODO list

In the .robot script, there are currently a few issues:
- Queries are not finding the "reviewFormSubmitted" field in responses.
- Document ids are currently hardcorded for the DEV environment. In TEST, this causes issues with documents not being found.
- Times from the API can switch between UTC -08:00 and -07:00 depending on daylight savings.
- Ensure original causes line up in the test data (e.g. ADP09412 on the form does not match ADP1941A in the expected response) because of differences in the records used in DEV and TEST.
