FROM registry.access.redhat.com/rhscl/python-36-rhel7:latest
ARG VERSION
ENV VERSION=$VERSION

COPY writer/requirements.txt ${APP_ROOT}/src/
USER root

RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    yum -y update && \
    yum -y install unixODBC && \
    curl https://packages.microsoft.com/config/rhel/8/prod.repo > /etc/yum.repos.d/mssql-release.repo && \
    export ACCEPT_EULA=Y && \
    yum -y install msodbcsql17 && \
    yum -y install mssql-tools && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
    yum -y install unixODBC-devel && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

COPY __init__.py ${APP_ROOT}/src/python/
COPY common/*.py ${APP_ROOT}/src/python/common/
COPY writer/*.py ${APP_ROOT}/src/python/writer/
COPY writer/mapper.json ${APP_ROOT}/src/python/writer/

ADD writer/entrypoint.sh .
RUN chmod 766 /etc/passwd
RUN chmod 754 ${APP_ROOT}/src/entrypoint.sh

ENTRYPOINT ${APP_ROOT}/src/entrypoint.sh