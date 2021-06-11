from database import databaseSetup, getWaifu
from flask import Flask, render_template
from colorama import Fore


app = Flask(__name__)

databaseSetup()
print(Fore.GREEN + "PROCESS:\t" + Fore.MAGENTA + "SQL tables ready!")

@app.route('/inventory/<userID>')
def hello_world(userID=None):
    listOfPlayerWaifu = getWaifu(userID)
    if(not listOfPlayerWaifu ):
        return "no inventory :C"
    
    return render_template("inventory.html", listOfWaifu=listOfPlayerWaifu)
#TODO: /getWaifu/USERID

