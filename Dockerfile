FROM python:3.6

ADD / /

RUN pip install -r requirements.txt
RUN alias logs='tail -F logs/wednesday.log'

CMD [ "python3", "wednesday.py" ]