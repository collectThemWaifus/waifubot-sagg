
FROM python:3.7-slim-buster

WORKDIR /app

COPY . /app
RUN pip3 install --user poetry
RUN pip3 install waitress

RUN apt-get update && apt-get install -y mysql-client && rm -rf /var/lib/apt
RUN ["python3", "-m", "poetry", "install"]

CMD ["python3", "-m", "poetry", "run", "python3", "/app/src/backend.py"] 
 