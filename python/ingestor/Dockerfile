FROM registry.access.redhat.com/rhscl/python-36-rhel7:latest
ARG VERSION
ENV VERSION=$VERSION

RUN [ "pwd" ]
RUN [ "ls", "-R" ]

COPY ingestor/requirements.txt ${APP_ROOT}/src/

RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

RUN [ "pwd" ]
RUN [ "ls", "-R" ]

COPY common ${APP_ROOT}/src/python/common
COPY ingestor ${APP_ROOT}/src/python/ingestor

RUN [ "pwd" ]
RUN [ "ls", "-R" ]

RUN ["python", "-m", "pytest", "python/ingestor"]

#TODO - Add worker processes to gunicorn below
CMD [ "gunicorn", "--error-logfile", "-", "--bind", "0.0.0.0:5000", "--pythonpath", "python/ingestor", "wsgi" ]