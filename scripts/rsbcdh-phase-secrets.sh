#!/bin/bash

usage() {
  cat <<-EOF
  Usage: $0 [ -h -e ]

  OPTIONS:
  ========
    -h prints the usage for the script
    -e <environment> set the Openshift namespace/project 
    -p <phase> set the phase  

EOF
exit 1
}

# In case you wanted to check what variables were passed
# echo "flags = $*"
while getopts e:p:h FLAG; do
  case $FLAG in
    e ) export PF_ENV=$OPTARG ;;
    p ) export PF_PHASE=$OPTARG ;;
    h ) usage ;;
    \?) #unrecognized option - show help
      echo -e \\n"Invalid script option"\\n
      usage
      ;;
  esac
done

PROJECT="iowaey-${PF_ENV}"
echo "Connecting to $PROJECT"
oc project ${PROJECT}

echo "Deleting existing template secret template.rsbc-dh-${PF_PHASE}"
oc delete secret template.rsbc-dh-${PF_PHASE}

echo "Creating template secret template.rsbc-dh-${PF_PHASE}"
oc create secret generic template.rsbc-dh-${PF_PHASE} \
--from-literal=username="replace-with-real" \
--from-literal=password="replace-with-real" \
--from-literal=db-username="replace-with-real" \
--from-literal=db-password='replace-with-real'

echo "Complete"
