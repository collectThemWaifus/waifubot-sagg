
FROM python:3.7-slim-buster

WORKDIR /app

COPY . .
RUN pip3 install --user poetry

RUN apt update &&  apt-get install default-mysql-client -y

CMD ["python3", "-m", "poetry", "run", "python3", "/app/src/bot.py"] 
