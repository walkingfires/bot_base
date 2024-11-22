from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from pydantic import create_model
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from bot.dao.session_maker import connection
from bot.users.keybords.keyboards import simptoms_keyboard, calendar_keyboard, calendar_page_keyboard, \
    control_keyboard, control_subject_keyboard, control_error_keyboard
from bot.users.dao import SymptomControlDAO, SymptomQuestionDAO, UserDAO
from bot.users.schemas import SymptomControlModel, SymptomQuestionModel

router = Router()


async def cb_calendar(message: Message, date_data: date = date.today()):
    if date_data.year > 2023:
        await message.edit_text(
            'Выберите дату',
            reply_markup=calendar_keyboard(date_data=date_data)
        )
    else:
        return


@connection(commit=False)
async def cb_calender_page(message: Message, session: AsyncSession, date_data: date):
    user_id = message.chat.id
    try:
        FilterModel = create_model(
            'FilterModel',
            telegram_id=(int, ...),
            date=(date, ...)
        )
        answers = await SymptomControlDAO.find_user_symptomcontrol_answers_or_none(session=session,
                                                                                   filters=FilterModel(
                                                                                       telegram_id=user_id,
                                                                                       date=date_data))
        date_text = f'{date_data.day}.{date_data.month}.{date_data.year}\n'
        subjects = await SymptomQuestionDAO.find_all_by_field(session=session, field='question_subject')

        if answers and subjects:
            for subject in subjects:
                date_text += f"{subject}: {answers.get(subject, '-')}\n"
        else:
            date_text += f'\nДанные не найдены'

        await message.edit_text(
            date_text,
            reply_markup=calendar_page_keyboard(date_data=date_data)
        )
    except Exception as e:
        logger.error(f"Ошибка при выполнении команды callback wiki_page для пользователя {user_id}: {e}")
        await message.edit_reply_markup()
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")


async def cb_simptoms(message: Message):
    await message.edit_text(
        "Выберите действие",
        reply_markup=simptoms_keyboard()
    )


@router.message(Command("simptoms"))
async def cmd_simptoms(message: Message):
    await message.answer(
        "Выберите действие",
        reply_markup=simptoms_keyboard()
    )


@connection(commit=False)
async def cb_control(message: Message, session: AsyncSession):
    user_id = message.chat.id
    try:
        questions = await SymptomQuestionDAO.find_all(session=session)

        if questions:
            questions_data = [SymptomQuestionModel.model_validate(i).model_dump() for i in questions]
            await message.edit_text(
                "Выберите Субъект",
                reply_markup=control_keyboard(questions_data=questions_data)
            )
        else:
            return

    except Exception as e:
        logger.error(f"Ошибка при выполнении команды callback control для пользователя {user_id}: {e}")
        await message.edit_reply_markup()
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")


@connection(commit=True)
async def cb_control_save_answer(message: Message, session: AsyncSession, question_id: int, answer: str):
    user_id = message.chat.id
    try:
        inner_user_id = await UserDAO.find_id_by_telegram_id(session=session, telegram_id=user_id)
        if not await SymptomControlDAO.find_control_by_question_id(session=session,
                                                                   user_id=inner_user_id,
                                                                   question_id=question_id):
            values = SymptomControlModel(user_id=inner_user_id,
                                         question_id=question_id, date=date.today(), answer=answer)
            await SymptomControlDAO.add(session=session, values=values)
            await cb_control(message)
        else:
            await message.edit_text(
                'Запись субъекта сегодня уже была произведена',
                reply_markup=control_error_keyboard()
            )
    except Exception as e:
        logger.error(f"Ошибка при выполнении команды callback control save answer для пользователя {user_id}: {e}")
        await message.edit_reply_markup()
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")


@connection(commit=False)
async def cb_control_subject(message: Message, session: AsyncSession, question_id: int):
    user_id = message.chat.id
    try:
        if not await SymptomControlDAO.find_control_by_question_id(session=session,
                                                                   user_id=await UserDAO.find_id_by_telegram_id(
                                                                       session=session,
                                                                       telegram_id=user_id),
                                                                   question_id=question_id):
            question = await SymptomQuestionDAO.find_one_or_none_by_id(session=session, data_id=question_id)

            if question:
                question_data = SymptomQuestionModel.model_validate(question).model_dump()
                await message.edit_text(
                    f'{question_data['question']}',
                    reply_markup=control_subject_keyboard(question_data=question_data)
                )
            else:
                return

        else:
            await message.edit_text(
                'Запись субъекта сегодня уже была произведена',
                reply_markup=control_error_keyboard()
            )

    except Exception as e:
        logger.error(f"Ошибка при выполнении команды callback control subject для пользователя {user_id}: {e}")
        await message.edit_reply_markup()
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")
