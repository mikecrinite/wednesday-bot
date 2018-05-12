FROM python:3.6

ADD / /

RUN pip install -r requirements.txt --no-index --find-links file:///tmp/packages

CMD [ "bash", "./run" ]