from aiogram import Router, F
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.config import admins, bot
from bot.dao.session_maker import connection
from bot.users.dao import UserDAO

router = Router()


@router.message(Command("mailing"), F.from_user.id.in_(admins))
@connection(commit=False)
async def mailing_to_all_users(
        message: Message,
        command: CommandObject,
        session: AsyncSession,
        important: bool = False
):
    users = await UserDAO.find_all_by_field(session=session, field="telegram_id")
    # TODO: check type
    mailing_text = command.args
    for user in users:
        try:
            await bot.send_message(
                user,
                mailing_text
            )
        except TelegramForbiddenError as e:
            logger.error(f"Пользователь {user} запретил отправку сообщений: {e}")
            if important:
                for admin_id in admins:
                    try:
                        await bot.send_message(admin_id, f"Пользователь {user} запретил отправку сообщений")
                    except Exception as e:
                        logger.error(f"Ошибка при отправке сообщения админу {admin_id}: {e}")
    await message.answer("Рассылка отправлена")


# @connection(commit=False)
# async def mailing_url_to_all_users(
#         message: Message,
#         command: CommandObject,
#         session: AsyncSession,
#         important: bool = False
# ):
#     users = await UserDAO.find_all_by_field(session=session, field="telegram_id")
#     # TODO: check type
#     mailing_text = command.args
#     for user in users:
#         try:
#             await bot.send_message(
#                 user,
#                 mailing_text
#             )
#         except TelegramForbiddenError as e:
#             logger.error(f"Пользователь {user} запретил отправку сообщений: {e}")
#             if important:
#                 for admin_id in admins:
#                     try:
#                         await bot.send_message(admin_id, f"Пользователь {user} запретил отправку сообщений")
#                     except Exception as e:
#                         logger.error(f"Ошибка при отправке сообщения админу {admin_id}: {e}")
#     await message.answer("Рассылка отправлена")
#
#
#
#
# async def cb_consultation(message: Message):
#     await message.edit_text(
#         "Форма обратной связи",
#         reply_markup=consultation_keyboard()
#     )
