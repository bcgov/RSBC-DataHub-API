#!/usr/bin/env bash
export WORKON_HOME=${HOME}/.virtualenv
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source ${HOME}/.local/bin/virtualenvwrapper.sh
workon tfapi
robot --exclude bi ${1} ${2}  --outputdir results dfttfws.robot
