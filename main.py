import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeDefault

from config import TOKEN
from handlers import router
from commands import set_commands


ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query', 'inline_query', 'channel_post', ]


async def start():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(await set_commands(), BotCommandScopeDefault())

    try:
        await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    except Exception as ex:
        print(f"Warning exception: {ex}")

if __name__ == '__main__':
    asyncio.run(start())
