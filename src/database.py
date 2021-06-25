import os
from typing import List
from sqlalchemy.engine import Engine
from sqlalchemy.sql.expression import text
from basemodels import Waifu, User

from flask_discord.client import DiscordOAuth2Session
from sqlalchemy.engine import create_engine, result

def getEngine () -> Engine:

    dbUser = os.getenv("DBUSER")
    dbPass = os.getenv("DBPASS") 
    dbHost = os.getenv("DBHOST") 
    dbPort = os.getenv("DBPORT")
    dbDatabase =  os.getenv("DBDATABASE")
    if (dbUser is None or dbPass is None or dbHost is None): # is testing
        return create_engine('sqlite:///waifuUser.db')
    if (dbPort is None):
        dbPort = '3306'
    if (dbDatabase is None):
        dbDatabase = 'sagginwaifubot'
    return create_engine(f'mysql://{dbUser}:{dbPass}@{dbHost}:{dbPort}/{dbDatabase}')    

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
    with getEngine().connect() as connection:
        connection.execute(text(sql_waifuUserTable))
    print("Tables Ready!")
def storeWaifu(waifu : Waifu, userid : str):
    sql_storeWaifu = text("INSERT INTO userWaifu (userid, name, imageURL , favourites) VALUES (:userid, :name, :imageURL, :favourites)")
    getEngine().execute(sql_storeWaifu, {"userid":userid, "name":waifu.name, "imageURL" : waifu.imageURL, "favourites": waifu.favourites})

def getWaifu(userid: str) -> List[Waifu]:
    sql_storeWaifu = "SELECT name, imageURL, favourites FROM userWaifu WHERE userid = ?"
    result = getEngine().execute(sql_storeWaifu, (userid,))
    listOfWaifu = []
    for value in result:
        newWaifu = Waifu(imageURL=value[1], name=value[0], favourites=value[2])
        listOfWaifu.append(newWaifu)
    if ( result is None):
        return False
    return listOfWaifu

def checkWaifuDuplicate(name : str) -> bool:
    sql_checkWaifuDuplicate = "SELECT * FROM userWaifu WHERE name = ?"
    result = getEngine().execute(sql_checkWaifuDuplicate, (name,)).fetchone()
    if (result is None):
        return False
    return True
def getAllUsers(bot_request: DiscordOAuth2Session.bot_request) -> List[User]:
    sql_getUsers =  "SELECT DISTINCT userid, SUM(favourites) FROM userWaifu GROUP BY userid ORDER BY SUM(favourites) DESC"
    result = getEngine().execute(sql_getUsers)
    listOfUsers = []
    for value in result:
        userId = value[0]
        newUser = getUserFromId(userId, bot_request)
        listOfUsers.append(newUser)
    if ( result is None):
        return False
    return listOfUsers

def getUserFromId(userid: int, bot_request : DiscordOAuth2Session.bot_request) -> User:
    sql_getUsers =  "SELECT SUM(favourites) FROM userWaifu WHERE userid=? ORDER BY SUM(favourites) DESC"
    result = getEngine().execute(sql_getUsers, (userid,))
    userObject = bot_request(f"/users/{userid}")
    avatarHash = userObject["avatar"]
    return User(userId=userid, totalValue=result[0], name=userObject["username"], avatarURL=(f"https://cdn.discordapp.com/avatars/{userid}/{avatarHash}.png"))

def getValuedWaifu(desc : bool, limit: int, bot_request : DiscordOAuth2Session.bot_request) -> List[Waifu]:
    if (desc):
        sql_getMostValuedWaifu = "SELECT name, imageURL, favourites, userid FROM userWaifu ORDER BY favourites DESC LIMIT ?"
    else:
        sql_getMostValuedWaifu = "SELECT name, imageURL, favourites, userid FROM userWaifu ORDER BY favourites ASC LIMIT ?"
    result = getEngine().execute(sql_getMostValuedWaifu, (limit,))
    listOfWaifu = []
    for value in result:
        newWaifu = Waifu(imageURL=value[1], name=value[0], favourites=value[2])
        newWaifu.claimName = getUserFromId(value[3], bot_request).name
        listOfWaifu.append(newWaifu)
    return listOfWaifu
