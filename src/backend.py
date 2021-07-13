from data.database import databaseSetup
from flask import Flask
from colorama import Fore
import os
from waitress import serve

template_dir = os.path.abspath('./web/templates')
static_dir = os.path.abspath('./web/static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

databaseSetup()
print(Fore.GREEN + "PROCESS:\t" + Fore.MAGENTA + "SQL tables ready!")
serve(app, listen='*:5200')