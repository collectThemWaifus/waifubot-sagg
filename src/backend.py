from typing import List
from data.basemodels import User, Waifu
from data.database import databaseSetup, getAllUsers, getValuedWaifu, getWaifu
from flask import Flask, render_template, redirect, url_for
from colorama import Fore
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask_caching import Cache
import os
from waitress import serve

template_dir = os.path.abspath('./web/templates')
static_dir = os.path.abspath('./web/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

databaseSetup()
print(Fore.GREEN + "PROCESS:\t" + Fore.MAGENTA + "SQL tables ready!")
serve(app, listen='*:5200')