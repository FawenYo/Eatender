FROM python:3.8.6-buster

WORKDIR /app

ADD . /app

RUN pip3 install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:8001 -k uvicorn.workers.UvicornWorker main:app