import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from loguru import logger
from aiogram import F

from config import bot, admins, dp
from users.handlers import symptom_control, mailing, callbacks, menu


# Функция, которая настроит командное меню (дефолтное для всех пользователей)
async def set_commands():
    commands = [
        BotCommand(command='start', description='Старт'),
        BotCommand(command='menu', description='Меню'),
        BotCommand(command='simptoms', description='Контроль симптомов')
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


# Функция, которая выполнится когда бот запустится
async def start_bot():
    await set_commands()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, f'Я запущен🥳.')
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения админу {admin_id}: {e}")
    logger.info("Бот успешно запущен.")


# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения админу {admin_id}: {e}")
    logger.error("Бот остановлен!")


async def main():
    dp.message.filter(F.chat.type == "private")
    # регистрация функций
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.include_routers(menu.router, callbacks.router, symptom_control.router, mailing.router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
