
FROM python:3.7-slim-buster

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home /app \
    app
USER app

WORKDIR /app

COPY . .
RUN pip3 install --user poetry
RUN ["python3", "-m", "poetry", "install"]

CMD ["python3", "-m", "poetry", "run", "/app/src/bot.py"]
 
