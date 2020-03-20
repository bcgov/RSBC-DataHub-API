FROM python:3.7.3-stretch

COPY requirements.txt ${APP_ROOT}/src/
CMD [ "echo" , "requirements copied" ]

RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

CMD [ "echo" , "requirements installed" ]
RUN [ "pwd" ]
RUN [ "ls" ]

COPY *.py ${APP_ROOT}/src/python/ingestor/

CMD [ "echo" , "python files copied" ]
RUN [ "ls" ]

#TODO - Add worker processes to gunicorn below 
CMD [ "gunicorn", "--error-logfile", "-", "--bind", "0.0.0.0:5000", "--pythonpath", "${APP_ROOT}/src/python/ingestor", "wsgi" ]
