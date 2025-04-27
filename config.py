import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv, find_dotenv
from database import RolizMotoDB

load_dotenv(find_dotenv())

TOKEN = os.getenv("bot_token")
tmp = os.getenv("admin_id").split(",")
ADMIN_ID = []
for i in tmp:
    if i != '':
        ADMIN_ID.append(int(i))
PATH_DB = os.getenv("path_db")
moto_db = RolizMotoDB(path=PATH_DB)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
PRIVATE_CHAT_ID = os.getenv("PRIVATE_CHAT_ID")
