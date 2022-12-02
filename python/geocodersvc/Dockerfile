FROM registry.access.redhat.com/rhscl/python-36-rhel7:latest
RUN [ "pwd" ]
RUN [ "ls", "-R" ]

COPY geocodersvc/ ${APP_ROOT}/src/python/geocodersvc/
COPY common/ ${APP_ROOT}/src/python/common/
RUN [ "echo" , "repo source files copied" ]

RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/python/geocodersvc/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src/python/geocodersvc && pip install -r requirements.txt

RUN [ "echo" , "requirements installed" ]
WORKDIR ${APP_ROOT}/src/
RUN [ "pwd" ]
RUN [ "ls", "-R" ]

RUN ["python", "-m", "pytest", "python/geocodersvc/tests"]

#TODO - Add worker processes to gunicorn below
CMD [ "gunicorn", "--error-logfile", "-", "--bind", "0.0.0.0:5000", "--pythonpath", "python/geocodersvc", "wsgi" ]

