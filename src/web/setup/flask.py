from os import getenv
from os import environ
from backend import app
from flask_discord.client import DiscordOAuth2Session

app.secret_key = getenv("FLASK_SECRET_KEY")
if ( app.secret_key is None):
    app.secret_key = open(f"/run/secrets/FLASK_SECRET_KEY").read()

if (getenv("FLASK_ENV") == "development"):
    environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.
