FROM python:3.8.6-buster

WORKDIR /app

ADD . /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

CMD gunicorn -c gunicorn.py -k uvicorn.workers.UvicornWorker main:app