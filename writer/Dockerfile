FROM python:3.7.3-stretch

COPY requirements.txt ${APP_ROOT}/src/
USER root
RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    yum -y update && \
    yum -y install unixODBC && \
    wget https://packages.microsoft.com/rhel/8/prod/unixODBC-devel-2.3.7-1.rh.x86_64.rpm && \
    yum -y localinstall unixODBC-devel-2.3.7-1.rh.x86_64.rpm && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

WORKDIR ${APP_ROOT}/src/

COPY *.py ${APP_ROOT}/src/
COPY mapper.json ${APP_ROOT}/src/

CMD [ "python", "./listener.py" ]
