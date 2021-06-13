from os import statvfs_result
import sqlite3

from flask_discord.client import DiscordOAuth2Session
from basemodels import Waifu, User
def databaseSetup():
    sql_waifuUserTable = '''
        CREATE TABLE IF NOT EXISTS userWaifu (
            userid char(38) NOT NULL,
            name VARCHAR(100) NOT NULL,
            imageURL VARCHAR(100) NOT NULL,
            favourites MEDIUMINT NOT NULL,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (userid, time)
        );
    '''
    con = sqlite3.connect('waifuUser.db')
    con.execute(sql_waifuUserTable)
    con.commit()
    print("Tables Ready!")

def storeWaifu(waifu : Waifu, userid : str):
    sql_storeWaifu = "INSERT INTO userWaifu (userid, name, imageURL , favourites) VALUES (?, ?, ?, ?)"
    sql_vals = (userid, waifu.name , waifu.imageURL, waifu.favourites )
    con = sqlite3.connect('waifuUser.db')
    con.execute(sql_storeWaifu, sql_vals)
    con.commit()

def getWaifu(userid: str):
    sql_storeWaifu = "SELECT name, imageURL, favourites FROM userWaifu WHERE userid = ?"
    con = sqlite3.connect('waifuUser.db')
    cursor = con.execute(sql_storeWaifu, (userid,))
    result = cursor.fetchall()
    listOfWaifu = []
    for value in result:
        newWaifu = Waifu(imageURL=value[1], name=value[0], favourites=value[2])
        listOfWaifu.append(newWaifu)
    if ( result is None):
        return False
    return listOfWaifu

def getAllUsers(bot_request: DiscordOAuth2Session.bot_request):
    sql_getUsers =  "SELECT DISTINCT userid, SUM(favourites) FROM userWaifu ORDER BY SUM(favourites) DESC"
    con = sqlite3.connect('waifuUser.db')
    cursor = con.execute(sql_getUsers)
    result = cursor.fetchall()
    listOfUsers = []
    for value in result:
        userId = value[0]
        userObject = bot_request(f"/users/{userId}")
        avatarHash = userObject["avatar"]
        newUser = User(userId=userId, totalValue=value[1], name=userObject["username"], avatarURL=(f"https://cdn.discordapp.com/avatars/{userId}/{avatarHash}.png"))
        listOfUsers.append(newUser)
    if ( result is None):
        return False
    return listOfUsers
