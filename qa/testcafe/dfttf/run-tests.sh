#!/usr/bin/env bash

# Wrapper script for calling the Digital Forms 12/24 web app front-end tests with TestCafe in Bash.

if [ -f .env ]; then
    source .env
else
    echo "No .env file found. Please copy .env-template to .env, add values, and re-run ${0}."
    exit 1
fi

echo Using ${SSO_BCEID2_USERNAME} to log in...

if [ -z "${1}" ]; then
    # Default to using Chrome browser, as it is fastest
    npm run test:chrome,test:firefox
    
else
    # npm run test:firefox
    # npm run test:chrome-debug
    # npm run test:headless
    npm run ${1}
fi
