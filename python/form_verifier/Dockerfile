FROM python:3.7.3-stretch

COPY form_verifier/requirements.txt ${APP_ROOT}/src/
RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

COPY __init__.py ${APP_ROOT}/src/python/
COPY common/*.py ${APP_ROOT}/src/python/common/
COPY form_verifier/*.py ${APP_ROOT}/src/python/form_verifier/

CMD [ "python", "python/form_verification/listener.py" ]
