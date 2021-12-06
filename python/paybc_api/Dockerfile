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

COPY common ${APP_ROOT}/src/python/common
COPY paybc_api ${APP_ROOT}/src/python/paybc_api

CMD [ "echo" , "python files copied" ]
RUN [ "pwd" ]
RUN [ "ls", "-R" ]

RUN ["python", "-m", "pytest", "python/paybc_api"]

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "--pythonpath", "python/paybc_api", "wsgi:create_app()" ]

