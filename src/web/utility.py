from backend import app
from data.basemodels import User, Waifu
from typing import List
from flask_caching import Cache
from flask_discord import DiscordOAuth2Session
from data.database import  getAllUsers, getValuedWaifu

discord: DiscordOAuth2Session  = app.config['discord']
cache: Cache.cache = app.config['cache'] 

def completeBackendUser(incomplete: User) -> User:
    userObject = discord.bot_request(f"/users/{incomplete.userId}")
    if (incomplete.name is None):
        incomplete.name = userObject["username"]
    if (incomplete.avatarURL is None):
        avatarHash = userObject["avatar"]
        incomplete.avatarURL = (f"https://cdn.discordapp.com/avatars/{incomplete.userId}/{avatarHash}.png")

def completeAllBackendUser (listOfIncomplete : List[User]):
    for incompleteUser in listOfIncomplete:
        completeBackendUser(incompleteUser)

def completeAllWaifu ( listOfIncomplete : List[Waifu]):
    for waifu in listOfIncomplete:
        completeBackendUser(waifu.claimerUser) 

@cache.cached(key_prefix='allValuedWaifu')
def getAllValuedWaifu () -> List[Waifu]:
    listValuedWaifu = getValuedWaifu(True, 10)
    completeAllWaifu(listValuedWaifu)
    return listValuedWaifu

@cache.cached(key_prefix='allLeaderboardUsers')
def getLeaderboardUsers() -> List[User]:
    listOfAllPlayerInventory = getAllUsers()
    completeAllBackendUser(listOfAllPlayerInventory)
    return listOfAllPlayerInventory
