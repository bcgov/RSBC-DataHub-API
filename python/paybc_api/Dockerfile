FROM registry.access.redhat.com/ubi8/python-38
#FROM registry.access.redhat.com/rhscl/python-36-rhel7:latest
ARG VERSION
ENV VERSION=$VERSION

RUN [ "pwd" ]
RUN [ "ls", "-R" ]

COPY paybc_api/requirements.txt ${APP_ROOT}/src/

RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

RUN [ "pwd" ]
RUN [ "ls", "-R" ]

COPY common ${APP_ROOT}/src/python/common
COPY paybc_api ${APP_ROOT}/src/python/paybc_api

RUN [ "pwd" ]
RUN [ "ls", "-R" ]

# ( Commenting Line 27 as pytest is not working with new python 311 image and removal of orbeaon forms)
RUN ["python", "-m", "pytest", "python/paybc_api"]

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "--pythonpath", "python/paybc_api", "wsgi:create_app()" ]