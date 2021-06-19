
FROM python:3.7-slim-buster

WORKDIR /app

COPY ../../* /app
RUN pip3 install --user poetry
RUN poetry install

RUN ["python3", "bot.py"]
