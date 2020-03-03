FROM python:3.7.3-stretch

COPY requirements.txt ${APP_ROOT}/src/
USER root
RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    cat /etc/redhat-release && \
    yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm && \
    yum -y update && \
    yum list | grep -i odbc && \
    yum -y install unixODBC && \
    yum -y install unixODBC-devel && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

WORKDIR ${APP_ROOT}/src/

COPY *.py ${APP_ROOT}/src/
COPY mapper.json ${APP_ROOT}/src/

CMD [ "python", "./listener.py" ]
