from aiogram.types import BotCommand


async def set_commands():
    commands = [BotCommand(command='start', description='Запуск либо перезапуск бота'),]
    return commands
