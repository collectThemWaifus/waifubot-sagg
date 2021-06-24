
FROM python:3.7-slim-buster

WORKDIR /app

COPY . .
RUN pip3 install --user poetry
RUN ["python3", "-m", "poetry", "install"]
RUN ["chmod +r /app/src/"]
CMD ["python3", "-m", "poetry", "run", "/app/src/bot.py"]
 
