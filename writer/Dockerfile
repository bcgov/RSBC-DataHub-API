FROM python:3.7.3-stretch

COPY requirements.txt ${APP_ROOT}/src/
USER root
RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    yum -y update && \
    yum -y install unixODBC && \
    curl https://packages.microsoft.com/config/rhel/8/prod.repo > /etc/yum.repos.d/mssql-release.repo && \
    export ACCEPT_EULA=Y && \
    yum install msodbcsql17 && \
    yum -y localinstall unixODBC-devel && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

WORKDIR ${APP_ROOT}/src/

COPY *.py ${APP_ROOT}/src/
COPY mapper.json ${APP_ROOT}/src/

CMD [ "python", "./listener.py" ]
