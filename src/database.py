from os import statvfs_result
import sqlite3
from typing import List

from flask_discord.client import DiscordOAuth2Session
from flask_discord.models import user
from basemodels import Waifu, User
def databaseSetup():
    sql_waifuUserTable = '''
        CREATE TABLE IF NOT EXISTS userWaifu (
            userid char(38) NOT NULL,
            name VARCHAR(100) NOT NULL,
            imageURL VARCHAR(100) NOT NULL,
            favourites MEDIUMINT NOT NULL,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            sacrificed INT DEFAULT 0,
            PRIMARY KEY (userid, time)
        );
    '''
    con = sqlite3.connect('waifuUser.db')
    con.execute(sql_waifuUserTable)
    con.commit()
    print("Tables Ready!")
def storeWaifu(waifu : Waifu, userid : str):
    sql_storeWaifu = "INSERT INTO userWaifu (userid, name, imageURL , favourites) VALUES (?, ?, ?, ?)"
    sql_vals = (userid, waifu.name , waifu.imageURL, waifu.favourites)
    con = sqlite3.connect('waifuUser.db')
    con.execute(sql_storeWaifu, sql_vals)
    con.commit()

def getWaifu(userid: str) -> List[Waifu]:
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

def checkWaifuDuplicate(name : str) -> bool:
    sql_checkWaifuDuplicate = "SELECT * FROM userWaifu WHERE name = ?"
    con = sqlite3.connect('waifuUser.db')
    result = con.execute(sql_checkWaifuDuplicate, (name,)).fetchone()
    if (result is None):
        return False
    return True
def getAllUsers(bot_request: DiscordOAuth2Session.bot_request) -> List[User]:
    sql_getUsers =  "SELECT DISTINCT userid, SUM(favourites) FROM userWaifu GROUP BY userid ORDER BY SUM(favourites) DESC"
    con = sqlite3.connect('waifuUser.db')
    cursor = con.execute(sql_getUsers)
    result = cursor.fetchall()
    listOfUsers = []
    for value in result:
        userId = value[0]
        newUser = getUserFromId(userId)
        listOfUsers.append(newUser)
    if ( result is None):
        return False
    return listOfUsers

def getUserFromId(userid: int, bot_request : DiscordOAuth2Session.bot_request) -> User:
    sql_getUsers =  "SELECT SUM(favourites) FROM userWaifu WHERE userid=? ORDER BY SUM(favourites) DESC"
    con = sqlite3.connect('waifuUser.db')
    cursor = con.execute(sql_getUsers, (userid,))
    result = cursor.fetchone()
    userObject = bot_request(f"/users/{userid}")
    avatarHash = userObject["avatar"]
    return User(userId=userid, totalValue=result[0], name=userObject["username"], avatarURL=(f"https://cdn.discordapp.com/avatars/{userid}/{avatarHash}.png"))

def getValuedWaifu(desc : bool, limit: int) -> List[Waifu]:
    con = sqlite3.connect('waifuUser.db')
    if (desc):
        sql_getMostValuedWaifu = "SELECT name, imageURL, favourites, userid FROM userWaifu ORDER BY favourites DESC LIMIT ?"
    else:
        sql_getMostValuedWaifu = "SELECT name, imageURL, favourites, userid FROM userWaifu ORDER BY favourites ASC LIMIT ?"
    cursor = con.execute(sql_getMostValuedWaifu, (limit,))
    result = cursor.fetchall()
    listOfWaifu = []
    for value in result:
        newWaifu = Waifu(imageURL=value[1], name=value[0], favourites=value[2])
        listOfWaifu.append(newWaifu)
    return listOfWaifu
