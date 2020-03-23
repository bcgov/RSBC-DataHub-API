FROM python:3.7.3-stretch

COPY validator/requirements.txt ${APP_ROOT}/src/
RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

COPY common/*.py ${APP_ROOT}/src/python/common/
COPY validator/*.py ${APP_ROOT}/src/python/validator/
COPY validator/schemas.json ${APP_ROOT}/src/python/validator/

WORKDIR ${APP_ROOT}/src

CMD [ "python", "python/validator/listener.py" ]
