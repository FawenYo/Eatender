FROM python:3.8.6-buster

WORKDIR /app

ADD . /app

RUN pip3 install -r requirements.txt

# Heroku can't bind port
# CMD ["gunicorn", "main:app"]

# GCP / Local
CMD ["gunicorn", "--config", "gunicorn.py", "main:app"]