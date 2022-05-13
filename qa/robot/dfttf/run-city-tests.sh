#!/usr/bin/env bash
export WORKON_HOME=${HOME}/.virtualenv
VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source ${HOME}/.local/bin/virtualenvwrapper.sh
workon tfapi
robot ${1} ${2}  --outputdir results-cities dfttf-cities.robot
