import os
from typing import List
from sqlalchemy.engine import Engine
from sqlalchemy.sql.expression import text
from basemodels import Waifu, User

from flask_discord.client import DiscordOAuth2Session
from sqlalchemy.engine import create_engine, result

from sqlalchemy.engine.url import URL

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
    return create_engine(URL("mysql", username=dbUser, password=dbPass, host=dbHost, database=dbDatabase))    
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
    sql_storeWaifu = "INSERT INTO userWaifu (userid, name, imageURL , favourites) VALUES (:userid, :name, :imageURL, :favourites)"
    getEngine().execute(text(sql_storeWaifu), {"userid":userid, "name":waifu.name, "imageURL" : waifu.imageURL, "favourites": waifu.favourites})

def getWaifu(userid: str) -> List[Waifu]:
    sql_storeWaifu = "SELECT name, imageURL, favourites FROM userWaifu WHERE userid = :userid"
    result = getEngine().execute(text(sql_storeWaifu), {"userid": userid}).all()
    listOfWaifu = []
    for value in result:
        newWaifu = Waifu(imageURL=value[1], name=value[0], favourites=value[2])
        listOfWaifu.append(newWaifu)
    if ( result is None):
        return False
    return listOfWaifu

def checkWaifuDuplicate(name : str) -> bool:
    sql_checkWaifuDuplicate = "SELECT * FROM userWaifu WHERE name = :name"
    result = getEngine().execute(text(sql_checkWaifuDuplicate), {"name": name}).one_or_none()
    if (result is None):
        return False
    return True
def getAllUsers() -> List[User]:
    sql_getUsers =  "SELECT DISTINCT userid, SUM(favourites) FROM userWaifu GROUP BY userid ORDER BY SUM(favourites) DESC"
    result = getEngine().execute(text(sql_getUsers))
    listOfUsers = []
    for value in result.all():
        userId = value[0]
        newUser = getUserFromId(userId)
        listOfUsers.append(newUser)
    if ( result is None):
        return False
    return listOfUsers

def getUserFromId(userid: int) -> User:
    sql_getUsers =  "SELECT SUM(favourites) FROM userWaifu WHERE userid=:userid ORDER BY SUM(favourites) DESC"
    result = getEngine().execute(text(sql_getUsers), {"userid" : userid}).one()
    return User(userId=userid, totalValue=result[0])

def getValuedWaifu(desc : bool, limit: int) -> List[Waifu]:
    if (desc):
        sql_getMostValuedWaifu = "SELECT name, imageURL, favourites, userid FROM userWaifu ORDER BY favourites DESC LIMIT :limit"
    else:
        sql_getMostValuedWaifu = "SELECT name, imageURL, favourites, userid FROM userWaifu ORDER BY favourites ASC LIMIT :limit"
    result = getEngine().execute(text(sql_getMostValuedWaifu), {"limit": limit}).all()
    listOfWaifu = []
    for value in result:
        newWaifu = Waifu(imageURL=value[1], name=value[0], favourites=value[2])
        newWaifu.claimerId = getUserFromId(value[3]).userId
        listOfWaifu.append(newWaifu)
    return listOfWaifu
