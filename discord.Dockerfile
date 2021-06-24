
FROM python:3.7-slim-buster

WORKDIR /app

COPY . .
RUN pip3 install --user poetry
RUN ["python3", "-m", "poetry", "install"]
CMD ["python3", "/app/src/bot.py"]
 
