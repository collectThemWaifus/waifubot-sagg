from os import statvfs_result
import sqlite3
from basemodels import Waifu
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
    databaseSetup()
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