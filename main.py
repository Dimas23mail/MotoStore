import logging
import asyncio
import datetime
import multiprocessing

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeDefault
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import moto_db, bot
from handlers import router
from commands import set_commands
from utils import updating_db_from_xml


ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query', 'inline_query', 'channel_post', ]


def run_scheduler_process():

    async def run_scheduler():
        await update_database()
        scheduler = AsyncIOScheduler()
        # Добавляем задачу print_my_name, которая будет выполняться каждые 30 минут
        scheduler.add_job(update_database, 'interval', minutes=30)

        # Запускаем планировщик
        scheduler.start()
        try:
            while True:
                await asyncio.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            print("Планировщик остановлен")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Запускаем цикл событий с функцией keep_alive
        loop.run_until_complete(run_scheduler())
    except (KeyboardInterrupt, SystemExit):
        print("Получен сигнал остановки")
    finally:
        loop.close()
        print("Планировщик остановлен, цикл событий закрыт")


def run_bot_process():
    async def start_bot():
        dp = Dispatcher(storage=MemoryStorage())
        dp.include_router(router)

        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(await set_commands(), BotCommandScopeDefault())
        try:
            await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
        except Exception as ex:
            logging.error(f"Ошибка при работе бота: {ex}")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                        )

    try:
        loop.run_until_complete(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print(f"Процесс бота получил сигнал остановки")
    finally:
        loop.close()
        print(f"Процесс бота завершен")


async def update_database():
    try:
        categories = [("Запчасти", ), ("Мотоциклы", ), ("Велосипеды", ), ("Экипировка", )]
        async with moto_db:
            await moto_db.make_db()
            cat_db_data = await moto_db.get_categories()
        if len(cat_db_data) == 0:
            async with moto_db:
                if await moto_db.insert_categories(categories=categories) is None:
                    print("Ошибка при передаче категорий для записи")
        #  Процедура парсинга xml и внесения изменений в базу данных
        text = await updating_db_from_xml()
        print(f"text = {text}")
        date_of_update = datetime.datetime.now().strftime("%x %X")
        await bot.send_message(chat_id=-1002227083175, text=f"Дата обновления:\n{date_of_update}")
    except Exception as ex:
        logging.error(f"Ошибка при обновлении базы данных: {ex}")
        # Отправляем сообщение об ошибке
        try:
            await bot.send_message(chat_id=-1002227083175, text=f"Ошибка при обновлении базы данных:\n{str(ex)}")
        except Exception as msg_error:
            logging.error(f"Не удалось отправить сообщение об ошибке: {msg_error}")


def create_scheduler_process():
    #  Create process for scheduler
    scheduler_process = multiprocessing.Process(
        target=run_scheduler_process,
        name="SchedulerProcess"
    )

    scheduler_process.daemon = True
    scheduler_process.start()

    #  Create process for bot
    bot_process = multiprocessing.Process(
        target=run_bot_process,
        name="BotPollingProcess"
    )
    bot_process.daemon = True
    bot_process.start()
    try:
        while True:
            scheduler_process.join(timeout=1)
            bot_process.join(timeout=1)
            if not scheduler_process.is_alive() and not bot_process.is_alive():
                break
    except KeyboardInterrupt:
        print("Получен Ctrl+C в основном процессе")


if __name__ == '__main__':
    create_scheduler_process()
