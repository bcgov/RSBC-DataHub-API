FROM python:3.7.3-stretch

COPY form_verification/requirements.txt ${APP_ROOT}/src/
RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

COPY __init__.py ${APP_ROOT}/src/python/
COPY common/*.py ${APP_ROOT}/src/python/common/
COPY form_verification/*.py ${APP_ROOT}/src/python/form_verification/

CMD [ "python", "python/form_verification/listener.py" ]
