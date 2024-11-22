from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.users.handlers.menu import cb_consultation, cb_menu
from bot.users.handlers.wiki import cb_wiki, cb_wiki_page
from bot.users.handlers.symptom_control import cb_simptoms, cb_calendar, cb_calender_page, cb_control, cb_control_subject, \
    cb_control_save_answer
from bot.users.schemas import ButtonsCallbackFactory, WikiCallbackFactory, ArticleCallbackFactory, \
    CalendarCallbackFactory, ControlCallbackFactory
from bot.users.utils import unpack_date

router = Router()


@router.callback_query(ButtonsCallbackFactory.filter(F.section == "menu"))
async def callbacks_menu_fab(
        callback: CallbackQuery,
        callback_data: ButtonsCallbackFactory
):
    if callback_data.action == 'wiki':
        await cb_wiki(callback.message)
    if callback_data.action == 'consultation':
        await cb_consultation(callback.message)
    if callback_data.action == 'roll':
        await callback.message.edit_reply_markup(reply_markup=None)
    if callback_data.action == 'simptoms':
        await cb_simptoms(callback.message)
    if callback_data.action == 'comeback':
        await cb_menu(callback.message)
    await callback.answer()

@router.callback_query(ButtonsCallbackFactory.filter(F.section == "simptoms"))
async def callbacks_menu_fab(
        callback: CallbackQuery,
        callback_data: ButtonsCallbackFactory
):
    if callback_data.action == 'today':
        await cb_control(callback.message)
    if callback_data.action == 'calendar':
        await cb_calendar(callback.message)


@router.callback_query(WikiCallbackFactory.filter())
async def callbacks_article_pages_fab(
        callback: CallbackQuery,
        callback_data: WikiCallbackFactory
):
    await cb_wiki(callback.message, page=callback_data.page)

@router.callback_query(ArticleCallbackFactory.filter())
async def callbacks_article_pages_fab(
        callback: CallbackQuery,
        callback_data: ArticleCallbackFactory
):
    await cb_wiki_page(callback.message, page_data=callback_data)

@router.callback_query(CalendarCallbackFactory.filter(F.day))
async def callbacks_calendar_pages_fab(
        callback: CallbackQuery,
        callback_data: CalendarCallbackFactory
):
    await cb_calender_page(callback.message, date_data=unpack_date(callback_data.date))


@router.callback_query(CalendarCallbackFactory.filter())
async def callbacks_calendar_pages_fab(
        callback: CallbackQuery,
        callback_data: CalendarCallbackFactory
):
    await cb_calendar(callback.message, date_data=unpack_date(callback_data.date))

@router.callback_query(ControlCallbackFactory.filter(F.answer))
async def callbacks_control_pages_fab(
        callback: CallbackQuery,
        callback_data: ControlCallbackFactory
):
    await cb_control_save_answer(callback.message, question_id=callback_data.question_id, answer=callback_data.answer)


@router.callback_query(ControlCallbackFactory.filter())
async def callbacks_control_pages_fab(
        callback: CallbackQuery,
        callback_data: ControlCallbackFactory
):
    await cb_control_subject(callback.message, question_id=callback_data.question_id)
