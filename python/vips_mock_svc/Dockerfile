FROM python:3.7.3-stretch

COPY vips_mock_svc/requirements.txt ${APP_ROOT}/src/

RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

COPY vips_mock_svc ${APP_ROOT}/src/python/vips_mock_svc

RUN ["python", "-m", "pytest", "python/vips_mock_svc"]

CMD [ "gunicorn", "--error-logfile", "-", "--bind", "0.0.0.0:5000", "--pythonpath", "python/vips_mock_svc", "vips_mock_svc.app:create_app()" ]

