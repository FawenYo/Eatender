FROM python:3.8.6-buster

WORKDIR /app

ADD . /app

RUN pip3 install -r requirements.txt

CMD gunicorn -c gunicorn.py -k uvicorn.workers.UvicornWorker main:app