from os import getenv
from os import environ
from backend import app

app.secret_key = getenv("FLASK_SECRET_KEY")
if (app.secret_key is None):
    app.secret_key = open("/run/secrets/FLASK_SECRET_KEY").read()

if (getenv("FLASK_ENV") == "development"):
    # !! Only in development environment.
    environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
