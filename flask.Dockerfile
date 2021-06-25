
FROM python:3.7-slim-buster

WORKDIR /app

COPY . /app
RUN apt update &&  apt-get install default-mysql-client -y

RUN pip3 install --user poetry
RUN pip3 install waitress
CMD ["python3", "-m", "poetry", "run", "python3", "/app/src/backend.py"] 
 