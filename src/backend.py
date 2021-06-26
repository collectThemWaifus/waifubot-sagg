from typing import List
from basemodels import User, Waifu
from database import databaseSetup, getAllUsers, getValuedWaifu, getWaifu
from flask import Flask, render_template, redirect, url_for
from colorama import Fore
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import os
from waitress import serve
app = Flask(__name__)

envList = ["DISCORD_CLIENT_SECRET", "DISCORD_BOT_TOKEN", "DISCORD_REDIRECT_URI", "DISCORD_CLIENT_ID"]

for env in envList:
    if (os.getenv(env) is None): # Use Discord Secrets as backup (this is not elgant, Too Bad!)
        app.config[env] = open(f"/run/secrets/{env}").read()
    else :
        app.config[env] = os.getenv(env)

app.secret_key = os.getenv("FLASK_SECRET_KEY")
if ( app.secret_key is None):
    app.secret_key = open(f"/run/secrets/FLASK_SECRET_KEY").read()

if (os.getenv("FLASK_ENV") == "development"):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

discord = DiscordOAuth2Session(app) 
databaseSetup()
print(Fore.GREEN + "PROCESS:\t" + Fore.MAGENTA + "SQL tables ready!")

def completeBackendUser(incomplete: User) -> User:
    userObject = discord.bot_request(f"/users/{incomplete.userId}")
    if (incomplete.name is None):
        incomplete.name = userObject["username"]
    if (incomplete.avatarURL is None):
        avatarHash = userObject["avatar"]
        incomplete.avatarURL = (f"https://cdn.discordapp.com/avatars/{incomplete.userId}/{avatarHash}.png")

def completeAllBackendUser (listOfIncomplete : List[User]):
    for incompleteUser in listOfIncomplete:
        completeBackendUser(incompleteUser)

def completeAllWaifu ( listOfIncomplete : List[Waifu]):
    for waifu in listOfIncomplete:
        completeBackendUser(waifu.claimerUser) 

@app.route("/")
def home():
    listValuedWaifu = getValuedWaifu(True, 10)
    completeAllWaifu(listValuedWaifu)
    
    listOfAllPlayerInventory = getAllUsers()
    completeAllBackendUser(listOfAllPlayerInventory)
    return render_template("index.html",
        listPlayers = listOfAllPlayerInventory,
        listWaifus=listValuedWaifu)
    if (not discord.authorized):

        return render_template("index.html",
            user=discord.fetch_user(),
            authorized=discord.authorized,
            listPlayers = listOfAllPlayerInventory,
            listWaifu=listValuedWaifu)
    return render_template("index.html",
                    user=discord.fetch_user(),
                    authorized=discord.authorized,
                    listPlayers = listOfAllPlayerInventory,
                    listWaifu=listValuedWaifu)
    


@app.route('/inventory/<userID>')
def hello_world(userID=None):
    listOfPlayerWaifu = getWaifu(userID)
    if(not listOfPlayerWaifu ):
        return "no inventory :C"
    
    return render_template("inventory.html",listOfWaifu=listOfPlayerWaifu)



@app.route("/login/")
def login():
    return discord.create_session()

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for(".home"))

	
@app.route("/me/")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""

serve(app, listen='*:5200')
#TODO: /getWaifu/USERID

