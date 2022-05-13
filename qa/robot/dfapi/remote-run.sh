#!/usr/bin/env bash
# Script to upload and run Robot Framework tests, then download the results.
#
# Create test pod in TEST environment:
# $ oc new-app python:3.8~https://github.com/sclorg/s2i-python-container.git --context-dir=3.8/test/setup-test-app/ --name=temporary-test-pod

# For details, see https://justice.gov.bc.ca/wiki/display/RDFP/Testing+with+OpenShift+pods
# 
# Remote shell onto test pod:
# $ oc rsh svc/temporary-test-pod
# 
# Run this script to copy the Robot Framework script to the pod, run it, and return the results
# $ ./remote_run.sh
#

# This is a unique string from the pod name that will be used to get the pod id
UNIQUE_POD_STRING=temporary-test-pod
POD=$(kubectl get pods | grep ${UNIQUE_POD_STRING} | awk '{print $1}')
LOCAL_FOLDER_SOURCE=.
REMOTE_FOLDER_DESTINATION=.
REMOTE_FOLDER_TO_COPY_BACK_TO_LOCAL=${REMOTE_FOLDER_DESTINATION}/results
SCRIPT_TO_RUN=${REMOTE_FOLDER_DESTINATION}/dfapi.robot

# Copy script to pod
oc rsync ${LOCAL_FOLDER_SOURCE} ${POD}:${REMOTE_FOLDER_DESTINATION}

# Run test script on pod, but STOP after an error or test failure.
#kubectl exec ${POD} -- robot --loglevel DEBUG --debugfile dfapi.log --outputdir ${REMOTE_FOLDER_TO_COPY_BACK_TO_LOCAL} --exitonfailure --exitonerror ${SCRIPT_TO_RUN}

# Run test script on pod, but CONTINUE after errors or failures.
kubectl exec ${POD} -- robot --loglevel DEBUG --debugfile dfapi.log --outputdir ${REMOTE_FOLDER_TO_COPY_BACK_TO_LOCAL} ${SCRIPT_TO_RUN}

# Copy results back to pod
oc rsync ${POD}:${REMOTE_FOLDER_TO_COPY_BACK_TO_LOCAL} .
