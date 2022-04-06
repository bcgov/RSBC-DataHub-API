#!/usr/bin/env bash
#
# Digital Forms API (DFAPI) workflow test script
# 


# Set DEBUG_MODE to 'YES' to enable debug mode
DEBUG_MODE=YES

if [ "${DEBUG_MODE}" = YES ]; then
	echo "Running ${0} in debug mode..."
	# See https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html
	# for details of these settings and a full list of others.
	set -x   # Print trace of commands.
	set -e   # Exit if error detected.
fi


# --------------------------------------------------------------------- 
# Script variables
# --------------------------------------------------------------------- 

# The empty template used for creating environment files
TEMPLATE_ENV_FILE=template.env

# This file contains a list of files that MUST NOT be committed to version control
IGNORE_FILE=.gitignore

# Name of the environment to load the settings file for (e.g. dev, test)
ENVIRONMENT="${1}"


# --------------------------------------------------------------------- 
# Helper functions
# --------------------------------------------------------------------- 

# Helper fuction to ensure a file is listed in the git ignore file.
# Argument ${1}: a string (filename) to check for inside an ignore file.
# Script variable used: IGNORE_FILE, the name of the ignore file to check.
ensure_env_file_is_in_gitignore () {
  if [ -z "$(grep $1 $IGNORE_FILE)" ]; then
	while true; do  # Confirm that the file should be added to the git ignore list
		read -p "WARNING: '${1}' not found in ${IGNORE_FILE}. Do not commit ${1}! Add it to ${IGNORE_FILE} now? [y|n] " yn
		case ${yn} in
			[Yy]* ) echo ${1} >> ${IGNORE_FILE}
					echo "Added ${1} to ${IGNORE_FILE}."
					break;;
			[Nn]* ) break;;
			* ) echo "Please answer [y]es or [n]o. ";;
		esac
	done
  fi
}


# Check that JMeter is installed
ensure_jmeter_installed () {
	JMETER_PATH=$(which jmeter)
	if [ -z "${JMETER_PATH}" ]; then
	  echo "JMeter is not on your path. Install from https://jmeter.apache.org/download_jmeter.cgi and add to path." 
	  exit 1
	fi
}


# Check parameter for environment to use
load_env_file () {
	if [ -z "${ENVIRONMENT}" ]; then  # No parameters given
	  echo "Usage: ${0} <ENVIRONMENT>"
	  echo -n " ... where ENVIRONMENT corresponds to the environment you're using (eg. DEV, TEST, PROD). "
	  echo -n "This will load ENVIRONMENT.env from the current directory. Create an environment file by copying "
	  echo "${TEMPLATE_ENV_FILE} to a new file (eg. 'dev.env') and update it."
	  exit 1
	else  # Load environment file, if it exists
	  if [ -f "${ENVIRONMENT}.env" ]; then  # Environment file does exist
		if [ -z "$(diff ${ENVIRONMENT}.env ${TEMPLATE_ENV_FILE})" ]; then  # But has not been updated
			echo -n "Unable to continue: ${ENVIRONMENT}.env has been created from a template, but has not yet "
			echo -n "been updated from its template. Please update ${ENVIRONMENT}.env with environment "
			echo "credentials and URI."
			exit 2
		else  # Environment file exists, and has been updated
			source "${ENVIRONMENT}.env"
		fi
	  else  # No environment file, offer to create one
		while true; do  # Ask if we should create a new environment file
			read -p "No environment file '${ENVIRONMENT}.env' found. Create one from ${TEMPLATE_ENV_FILE}? [y|n] " yn
			case ${yn} in
				[Yy]* ) cp ${TEMPLATE_ENV_FILE} ${ENVIRONMENT}.env
						echo "Created ${ENVIRONMENT}.env. Add credentials and URLs and re-run ${0}."
						exit;;
				[Nn]* ) exit;;
				* ) echo "Please answer yes or no. ";;
			esac
		done
	  fi
	fi
}


# Delete any existing records using the ORDS endpoint (only for TEST and DEV environments)
clean_up_old_data_with_ords(){
    # Check to see if the WGSG gateway is accessible
    ping -c 1 -W 0.5 ${ORDS_HOST} > /dev/null 2>&1
    if [[ "${?}" != 0 ]]; then
        echo "Not connected to VPN -- skipping clean-up ORDS endpoint call."
        echo
        return
    fi
    
    if [ "${ENVIRONMENT}" == dev ]; then
        export ORDS_AUTH_STRING='DEV_AUTH_STRING'
    elif [ "${ENVIRONMENT}" == test ]; then
        export ORDS_AUTH_STRING='TEST_AUTH_STRING'
    fi
    set -x
    echo Cleaning up any previous record of ${PROHIB_TYPE} ${PROHIB_NUM}...
    curl --insecure \
        --request DELETE \
        --silent \
        --header "Authorization: Basic ${ORDS_AUTH_STRING}" \
        ${ORDS_URI}/digitalForm/prohibition/${PROHIB_ID}/111
    set +x
}   


# Invoke JMeter with all the parameters loaded from the given environment file
start_jmeter(){
    set -x
    jmeter -Jserver.rmi.ssl.disable=true \
        --jmeterproperty DFAPI_SERVER_SCHEME=${DFAPI_SERVER_SCHEME} \
        --jmeterproperty DFAPI_SERVER_HOST=${DFAPI_SERVER_HOST} \
        --jmeterproperty DFAPI_SERVER_PATH=${DFAPI_SERVER_PATH} \
        --jmeterproperty DFAPI_SERVER_BASE=${DFAPI_SERVER_BASE} \
        --jmeterproperty DFAPI_SERVER_USER=${DFAPI_SERVER_USER} \
        --jmeterproperty DFAPI_SERVER_PASS=${DFAPI_SERVER_PASS} \
        --jmeterproperty DFDH_SERVER_SCHEME=${DFDH_SERVER_SCHEME} \
        --jmeterproperty DFDH_SERVER_HOST=${DFDH_SERVER_HOST} \
        --jmeterproperty DFDH_SERVER_PORT=${DFDH_SERVER_PORT} \
		--jmeterproperty ORDS_AUTH=${ORDS_AUTH} \
        --jmeterproperty PROHIB_TYPE=${PROHIB_TYPE} \
        --jmeterproperty PROHIB_NUMBER=${PROHIB_NUM} \
        --jmeterproperty PROHIB_ID=${PROHIB_ID} \
        --jmeterproperty CORRELATION_ID=${CORRELATION_ID} \
        --jmeterproperty REVIEW_DATE=${PROHIB_REVIEW_DATE} \
        --jmeterproperty REVIEW_TYPE=${PROHIB_REVIEW_TYPE} \
        --jmeterproperty LOG_OUTPUT="${PWD}/${SERVER_HOST}-${PROHIB_TYPE}.log.xml" \
        --testfile ${TEST_PLAN}
   set +x  
}

# --------------------------------------------------------------------- 
# Script main section
# --------------------------------------------------------------------- 
ensure_jmeter_installed 
ensure_env_file_is_in_gitignore "${ENVIRONMENT}.env"
load_env_file "${ENVIRONMENT}.env"
#clean_up_old_data_with_ords
start_jmeter
