
FROM python:3.7-slim-buster

WORKDIR /app

COPY src/* /app
RUN pip3 install --user poetry
RUN pip3 install waitress
RUN poetry install

RUN ["python3", "bot.py"]
CMD [ "python3", "-m" , "waitress-serve", "--call", "'flaskr:create_app'"]