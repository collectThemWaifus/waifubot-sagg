from os import getenv
from backend import app
from flask_discord.client import DiscordOAuth2Session

envList = ["DISCORD_CLIENT_SECRET", "DISCORD_BOT_TOKEN",
           "DISCORD_REDIRECT_URI", "DISCORD_CLIENT_ID"]

for env in envList:
    if (getenv(env) is None):  # Use Discord Secrets as backup (this is not elgant, Too Bad!)
        app.config[env] = open(f"/run/secrets/{env}").read()
    else:
        app.config[env] = getenv(env)
discord = DiscordOAuth2Session(app)
app.config['discord'] = discord
