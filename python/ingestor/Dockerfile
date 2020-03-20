FROM python:3.7.3-stretch
RUN [ "pwd" ]
RUN [ "ls", "-R" ]

COPY ingestor/requirements.txt ${APP_ROOT}/src/
CMD [ "echo" , "requirements copied" ]

RUN source /opt/app-root/etc/scl_enable && \
    set -x && \
    pip install -U pip setuptools wheel && \
    sha256sum "${APP_ROOT}/src/requirements.txt" > ${APP_ROOT}/requirements.sha256  && \
    cd ${APP_ROOT}/src && pip install -r requirements.txt

CMD [ "echo" , "requirements installed" ]
RUN [ "pwd" ]
RUN [ "ls", "-R" ]

COPY *.py ${APP_ROOT}/src/python/ingestor/

CMD [ "echo" , "python files copied" ]
RUN [ "ls", "-R" ]

#TODO - Add worker processes to gunicorn below 
CMD [ "gunicorn", "--error-logfile", "-", "--bind", "0.0.0.0:5000", "--pythonpath", "${APP_ROOT}/src/python/ingestor", "wsgi" ]
