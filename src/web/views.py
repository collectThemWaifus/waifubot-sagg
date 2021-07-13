from backend import app
from data.database import getWaifu
from flask import render_template, redirect, url_for
from flask_discord import  requires_authorization
from utility import getAllValuedWaifu, getLeaderboardUsers

discord = app.config['discord']

@app.route("/")
def home():
    listValuedWaifu = getAllValuedWaifu()
    listOfAllPlayerInventory = getLeaderboardUsers()
    if (not discord.authorized):

        return render_template("index.html",
            authorized=discord.authorized,
            listPlayers = listOfAllPlayerInventory,
            listWaifus=listValuedWaifu)
    return render_template("index.html",
                    user=discord.fetch_user(),
                    authorized=discord.authorized,
                    listPlayers = listOfAllPlayerInventory,
                    listWaifus=listValuedWaifu)
    


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
