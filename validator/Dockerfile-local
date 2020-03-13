FROM python:3.7.3-stretch

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY *.py /home/appuser/
COPY schemas.json /home/appuser/

CMD [ "python", "./listener.py" ]
