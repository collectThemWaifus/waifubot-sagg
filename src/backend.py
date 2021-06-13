from database import databaseSetup, getAllUsers, getWaifu
from flask import Flask, render_template, redirect, url_for
from colorama import Fore
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import os
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 526954549638856735    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("DISCORD_CLIENT_SECRET")           # Discord client secret.
app.config["DISCORD_BOT_TOKEN"] = os.getenv("DISCORD_BOT_TOKEN")   
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"


discord = DiscordOAuth2Session(app) 
databaseSetup()
print(Fore.GREEN + "PROCESS:\t" + Fore.MAGENTA + "SQL tables ready!")

@app.route('/leaderboard')
def listAllUsers() :
    listOfAllPlayerInventory = getAllUsers(discord.bot_request)

    return render_template("leaderboard.html", listPlayers=listOfAllPlayerInventory)

@app.route('/inventory/<userID>')
def hello_world(userID=None):
    listOfPlayerWaifu = getWaifu(userID)
    if(not listOfPlayerWaifu ):
        return "no inventory :C"
    
    return render_template("inventory.html", listOfWaifu=listOfPlayerWaifu)



@app.route("/login/")
def login():
    return discord.create_session()
	

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

	
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

#TODO: /getWaifu/USERID

