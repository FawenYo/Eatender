FROM python:3.8.6-buster

WORKDIR /app

ADD . /app

RUN apt update
RUN apt install screen -y
RUN pip3 install -r requirements.txt

CMD ["uwsgi", "config.ini"]