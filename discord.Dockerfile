
FROM python:3.7-slim-buster

WORKDIR /app

COPY . /app
RUN pip3 install --user poetry
RUN ["python3", "-m", "poetry", "install"]

CMD ["python3", "-m", "poetry", "run", "/app/src/bot.py"]
 