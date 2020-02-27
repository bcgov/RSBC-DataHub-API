FROM python:3.7.3-stretch

COPY requirements.txt ${APP_ROOT}/src/
RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

COPY *.py ${APP_ROOT}/src/

#TODO - Add worker processes to gunicorn below 
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "wsgi" ]
