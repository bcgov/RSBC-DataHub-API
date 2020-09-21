FROM python:3.7.3-stretch

COPY hold_processor/requirements.txt ${APP_ROOT}/src/
RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

COPY __init__.py ${APP_ROOT}/src/python/
COPY common/*.py ${APP_ROOT}/src/python/common/
COPY hold_processor/*.py ${APP_ROOT}/src/python/hold_processor/
