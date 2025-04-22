import logging
import asyncio
import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TOKEN, moto_db
from handlers import router
from commands import set_commands
from utils import updating_db_from_xml


ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query', 'inline_query', 'channel_post', ]


def start_bot():

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    running_loop = asyncio.get_event_loop()
    tasks = [
        running_loop.create_task(start_polling_bot(bot=bot, dp=dp)),
        running_loop.create_task(start_scheduler_update_db(bot=bot))
    ]
    running_loop.run_until_complete(asyncio.wait(tasks))
    running_loop.close()


async def start_polling_bot(bot: Bot, dp: Dispatcher):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(await set_commands(), BotCommandScopeDefault())
    try:
        await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    except Exception as ex:
        print(f"Warning exception: {ex}")


async def update_database(bot: Bot):
    categories = [("Запчасти", ), ("Мотоциклы", ), ("Велосипеды", ), ("Экипировка", )]
    async with moto_db:
        await moto_db.make_db()
        cat_db_data = await moto_db.get_categories()
    if len(cat_db_data) == 0:
        async with moto_db:
            if await moto_db.insert_categories(categories=categories) is None:
                print("Ошибка при передаче категорий для записи")
    #  Процедура парсинга xml и внесения изменений в базу данных
    text = await updating_db_from_xml(bot=bot)

    print(f"text = {text}")
    date_of_update = datetime.datetime.now().strftime("%x %X")
    await bot.send_message(chat_id=-1002227083175, text=f"Дата обновления:\n{date_of_update}")


async def start_scheduler_update_db(bot: Bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=update_database, trigger="interval", minute=30, args=[bot, ])
    scheduler.start()

    print(f"Scheduler running!")
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print(f"Scheduler stopped!")


if __name__ == '__main__':
    start_bot()
