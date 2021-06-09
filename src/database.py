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
    sql_storeWaifu = "INSERT INTO userWaifu (userid, imageURL, name, favourites) VALUES (?, ?, ?, ?)"
    sql_vals = (userid, waifu.female, waifu.name, waifu.age )
    con = sqlite3.connect('waifuUser.db')
    con.execute(sql_storeWaifu, sql_vals)
    con.commit()

def getWaifu(userid: str):
    sql_storeWaifu = "SELECT name FROM userWaifu WHERE userid = ?"
    con = sqlite3.connect('waifuUser.db')
    cursor = con.execute(sql_storeWaifu, (userid,))
    result = cursor.fetchone()
    if ( result is None):
        return False
    return result
waifu = Waifu(female = True, name = "Sagiri", age = 14)
user = "testUserId"
storeWaifu(waifu=waifu, userid=user)
result = getWaifu(user)
print (result)
