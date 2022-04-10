import os
from pickle import TRUE
from smtplib import SMTPServerDisconnected
from typing import List
from sqlalchemy.engine import Engine
from sqlalchemy.sql.expression import text
from data.basemodels import Waifu, User
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine.url import URL


def getEngine() -> Engine:

    dbUser = os.getenv("DBUSER")
    dbPass = os.getenv("DBPASS")
    dbHost = os.getenv("DBHOST")
    dbPort = os.getenv("DBPORT")
    dbDatabase = os.getenv("DBDATABASE")
    if (dbUser is None or dbPass is None or dbHost is None):  # is testing
        return create_engine('sqlite:///waifuUser.db')
    if (dbPort is None):
        dbPort = '3306'
    if (dbDatabase is None):
        dbDatabase = 'sagginwaifubot'
    return create_engine(URL(
        "mysql",
        username=dbUser,
        password=dbPass,
        host=dbHost,
        database=dbDatabase))


def databaseSetup():
    sql_waifuUserTable = '''
        CREATE TABLE IF NOT EXISTS userWaifu (
            userid CHAR(38) NOT NULL,
            name VARCHAR(100) NOT NULL,
            imageURL VARCHAR(100) NOT NULL,
            favourites MEDIUMINT NOT NULL,
            time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            serverid VARCHAR(18),
            PRIMARY KEY (userid, serverid, time)
        );
    '''
    sql_UserTable = '''
        CREATE TABLE IF NOT EXISTS userTable (
            userid CHAR(38) NOT NULL,
            totalpoints BIGINT,
            serverid VARCHAR(18),
            PRIMARY KEY (userid, serverid) 
        );
    '''
    createList = [sql_waifuUserTable, sql_UserTable]
    with getEngine().connect() as connection:
        for sql in createList:
            connection.execute(text(sql))
    print("Tables Ready!")

def updateUser(waifu : Waifu, userid : int):
    sql_addUser = """
    INSERT INTO userTable (userid, totalpoints, serverid)
        VALUES (:userid, :totalpoints, :serverid)
    """
    sql_updateUser = """
    UPDATE INTO userTable (totalpoints)
        VALUES ( :totalpoints )
        WHERE userid = :userid AND serverid = :serverid
    """
    sqlQuery = sql_addUser
    valueOfUser = waifu.favourites
    user = getUserFromId(userid)
    if (user is not None):
        sqlQuery = sql_updateUser
        valueOfUser += user.totalValue
    getEngine().execute(text(sqlQuery),
        {"userid":userid, "totalpoints":valueOfUser, "serverid": user.serverid} ) 
def storeWaifu(waifu: Waifu, userid: str):
    updateUser(waifu, userid)
    sql_storeWaifu = """
    INSERT INTO userWaifu (userid, name, imageURL , favourites, serverid)
        VALUES (:userid, :name, :imageURL, :favourites, :serverid)
    """
    getEngine().execute(text(sql_storeWaifu), {
        "userid": userid, "name": waifu.name, "imageURL": waifu.imageURL, "favourites": waifu.favourites, "serverid":waifu.serverid})


def getWaifu(userid: str, serverid: int) -> List[Waifu]:
    sql_storeWaifu = "SELECT name, imageURL, favourites, serverid FROM userWaifu WHERE userid = :userid"
    result = getEngine().execute(
        text(sql_storeWaifu), {"userid": userid, "serverid": serverid}).all()
    listOfWaifu = []
    for value in result:
        newWaifu = Waifu(imageURL=value[1], name=value[0], favourites=value[2])
        listOfWaifu.append(newWaifu)
    if (result is None):
        return False
    return listOfWaifu


def checkWaifuDuplicate(name: str, serverid: int) -> bool:
    sql_checkWaifuDuplicate = "SELECT * FROM userWaifu WHERE name = :name AND serverid :serverid"
    result = getEngine().execute(text(sql_checkWaifuDuplicate),
                                 {"name": name, "serverid": serverid}).one_or_none()
    if (result is None):
        return False
    return True


def getAllUsers(serverid: int) -> List[User]:
    sql_getUsers = """SELECT DISTINCT userid, SUM(favourites) 
                    FROM userWaifu WHERE serverid=:serverid GROUP BY userid ORDER BY SUM(favourites) DESC"""
    result = getEngine().execute(text(sql_getUsers), {"serverid": serverid})
    listOfUsers = []
    for value in result.all():
        userId = value[0]
        newUser = getUserFromId(userId)
        listOfUsers.append(newUser)
    if (result is None):
        return False
    return listOfUsers


def getUserFromId(userid: int, serverid : int) -> User:
    sql_getUsers = "SELECT SUM(favourites) FROM userWaifu WHERE userid=:userid AND serverid=:serverid ORDER BY SUM(favourites) DESC"
    result = getEngine().execute(text(sql_getUsers), {"userid": userid, "serverid": serverid}).one()
    return User(userId=userid, totalValue=result[0])


def getValuedWaifu(desc: bool, limit: int) -> List[Waifu]:
    if (desc):
        sql_getMostValuedWaifu = "SELECT name, imageURL, favourites, userid FROM userWaifu ORDER BY favourites DESC LIMIT :limit"
    else:
        sql_getMostValuedWaifu = "SELECT name, imageURL, favourites, userid FROM userWaifu ORDER BY favourites ASC LIMIT :limit"
    result = getEngine().execute(
        text(sql_getMostValuedWaifu), {"limit": limit}).all()
    listOfWaifu = []
    for value in result:
        newWaifu = Waifu(imageURL=value[1], name=value[0], favourites=value[2])
        newWaifu.claimerId = getUserFromId(value[3]).userId
        newWaifu.claimerUser = getUserFromId(value[3])
        listOfWaifu.append(newWaifu)
    return listOfWaifu