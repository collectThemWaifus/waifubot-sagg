
FROM python:3.7-slim-buster

WORKDIR /app

COPY . .
RUN pip3 install --user poetry

RUN apt update &&   apt-get install python3-dev default-libmysqlclient-dev build-essential -y
RUN python3 -m poetry install
CMD ["python3", "-m", "poetry", "run", "python3", "/app/Discord/bot.py"] 
