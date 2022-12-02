FROM registry.access.redhat.com/rhscl/python-36-rhel7:latest

COPY validator/requirements.txt ${APP_ROOT}/src/
RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

COPY __init__.py ${APP_ROOT}/src/python/
COPY common/*.py ${APP_ROOT}/src/python/common/
COPY validator/*.py ${APP_ROOT}/src/python/validator/
COPY validator/schema.json ${APP_ROOT}/src/python/validator/

CMD [ "python", "python/validator/listener.py" ]
