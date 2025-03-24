import os
from dotenv import load_dotenv, find_dotenv
from database import BananichDB

load_dotenv(find_dotenv())

TOKEN = os.getenv("bot_token")
tmp = os.getenv("admin_id").split(",")
print(f"TOKEN = {TOKEN}, id = {tmp}")
ADMIN_ID = []
for i in tmp:
    if i != '':
        ADMIN_ID.append(int(i))
PATH_DB = os.getenv("path_db")
banan_db = BananichDB(path=PATH_DB)
