#!/usr/bin/env bash

DF_LICENCE_PLATE=abc123

# Check current project is a DF namespace
CURRENT_PROJECT=$(oc project)
if [[ "${CURRENT_PROJECT}" =~ "$DF_LICENCE_PLATE" ]]; then
  echo Not currently in a DF namespace.
  exit 1
fi

echo in DF namespace.
exit 0

# Create array of services in the RSBC namespace
SERVICES=($(kubectl get services | grep ^rsbc | awk '{print $1}'))
TODAYS_DATE=$(date '+%Y-%m-%d')

if [ ! -d "${TODAYS_DATE}" ]; then
	mkdir ${TODAYS_DATE}
fi

# Save the logs for each service pod
for pod in "${SERVICES[@]}"
do
	:
	echo Getting log for ${pod}...
	kubectl logs services/${pod} | ./filter-junk-lines.pl > ${TODAYS_DATE}/${pod}.log
done
