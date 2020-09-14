FROM python:3.7.3-stretch
RUN [ "pwd" ]
RUN [ "ls", "-R" ]

COPY paybc_api/requirements.txt ${APP_ROOT}/src/
CMD [ "echo" , "requirements copied" ]

RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

CMD [ "echo" , "requirements installed" ]
RUN [ "pwd" ]
RUN [ "ls", "-R" ]

COPY common/*.py ${APP_ROOT}/src/python/common/
COPY common/templates/*.html ${APP_ROOT}/src/python/common/templates/
COPY common/templates/partials/*.html ${APP_ROOT}/src/python/common/templates/partials/
COPY paybc_api/*.py ${APP_ROOT}/src/python/paybc_api/
COPY paybc_api/*.json ${APP_ROOT}/src/python/paybc_api/
COPY paybc_api/website/*.py ${APP_ROOT}/src/python/paybc_api/website/

RUN [ "mkdir", "-p", "/var/lib/sqlite" ]
RUN [ "chmod", "u+w", "/var/lib/sqlite" ]

CMD [ "echo" , "python files copied" ]
RUN [ "pwd" ]
RUN [ "ls", "-R" ]

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "--pythonpath", "python/paybc_api", "wsgi:create_app()" ]

