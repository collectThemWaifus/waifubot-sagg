
FROM python:3.7-slim-buster

WORKDIR /app

COPY . /app
RUN apt update &&   apt-get install python3-dev default-libmysqlclient-dev build-essential -y

RUN pip3 install --user poetry
RUN python3 -m poetry install

RUN pip3 install waitress
CMD ["python3", "-m", "poetry", "run", "python3", "/app/src/backend.py"] 
 