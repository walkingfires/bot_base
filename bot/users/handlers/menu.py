from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.session_maker import connection
from bot.users.keybords.keyboards import menu_keyboard, consultation_keyboard
from bot.users.dao import UserDAO
from bot.users.schemas import UserModel

router = Router()


@router.message(Command("start"))
@connection(commit=True)
async def cmd_start(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    try:
        user_info = await UserDAO.find_one_or_none(session=session, filters=UserModel(telegram_id=user_id))

        if user_info:
            await cmd_menu(message)
        else:
            values = UserModel(telegram_id=user_id)
            await UserDAO.add(session=session, values=values)
            await message.answer('Hello')
            await start_menu(message)

    except Exception as e:
        logger.error(f"Ошибка при выполнении команды /start для пользователя {user_id}: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")


@router.message(Command("menu"))
@connection(commit=False)
async def cmd_menu(message: Message, session: AsyncSession):
    user_id = message.from_user.id
    try:
        user_info = await UserDAO.find_one_or_none(session=session, filters=UserModel(telegram_id=user_id))

        if user_info:
            await message.answer(
                "Выберите действие",
                reply_markup=menu_keyboard()
            )
        else:
            await message.answer(
                "Для входа используйте /start"
            )

    except Exception as e:
        logger.error(f"Ошибка при выполнении команды /menu для пользователя {user_id}: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")


async def cb_menu(message: Message):
    await message.edit_text(
        "Выберите действие",
        reply_markup=menu_keyboard()
    )


async def start_menu(message: Message):
    await message.answer(
        "Выберите действие",
        reply_markup=menu_keyboard()
    )


async def cb_consultation(message: Message):
    await message.edit_text(
        "Форма обратной связи",
        reply_markup=consultation_keyboard()
    )
