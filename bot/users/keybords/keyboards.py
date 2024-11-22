from typing import List
from datetime import date
from bot.users.schemas import ButtonsCallbackFactory, ArticleCallbackFactory, WikiCallbackFactory, \
    CalendarCallbackFactory, ControlCallbackFactory
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.config import consultation_url
from bot.users.utils import calendar_flipper, get_month_info, pack_date


def calendar_keyboard(date_data: date):
    month_info = get_month_info(date_data)
    builder = InlineKeyboardBuilder()

    builder.button(text='ᐸ', callback_data=CalendarCallbackFactory(date=pack_date(calendar_flipper(date_data=date_data,
                                                                                                   backward=True)),
                                                                   day=False))
    month_year_text = f"{month_info['month_name_ru']} '{str(month_info['year'])[-2:]}"
    builder.button(text=month_year_text, callback_data=ButtonsCallbackFactory(section="menu", action="ignore"))
    builder.button(text='ᐳ', callback_data=CalendarCallbackFactory(date=pack_date(calendar_flipper(date_data=date_data,
                                                                                                   backward=False)),
                                                                   day=False))
    for day in range(1, 36):
        if day <= month_info['num_days']:
            day_date = date(month_info['year'], month_info['month'], day)
            builder.button(text=f'{day}', callback_data=CalendarCallbackFactory(date=pack_date(day_date), day=True))
        else:
            builder.button(text=' ', callback_data=ButtonsCallbackFactory(section="menu", action="ignore"))

    builder.button(text='ᐸ', callback_data=ButtonsCallbackFactory(section="menu", action="simptoms"))
    builder.adjust(3, 7, 7, 7, 7, 7, 1)
    return builder.as_markup()


def calendar_page_keyboard(date_data: date):
    builder = InlineKeyboardBuilder()
    builder.button(text='ᐸ', callback_data=CalendarCallbackFactory(date=pack_date(date_data), day=False))
    return builder.as_markup()


def control_keyboard(questions_data: List[dict]):
    builder = InlineKeyboardBuilder()
    for question in questions_data:
        builder.button(text=question['question_subject'],
                       callback_data=ControlCallbackFactory(question_id=question['id'], answer=None))
    builder.button(text='ᐸ', callback_data=ButtonsCallbackFactory(section="menu", action="simptoms"))
    builder.adjust(1)
    return builder.as_markup()


def control_subject_keyboard(question_data: dict):
    builder = InlineKeyboardBuilder()
    for answer in question_data['answers']:
        builder.button(text=answer, callback_data=ControlCallbackFactory(question_id=question_data['id'],
                                                                         answer=answer))
    builder.button(text='ᐸ', callback_data=ButtonsCallbackFactory(section="simptoms", action="today"))
    builder.adjust(1)
    return builder.as_markup()


def control_error_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='ᐸ', callback_data=ButtonsCallbackFactory(section="simptoms", action="today"))
    builder.adjust(1)
    return builder.as_markup()


def consultation_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Форма обратной связи', url=consultation_url)
    builder.button(text='ᐸ', callback_data=ButtonsCallbackFactory(section="menu", action="comeback"))
    builder.adjust(1)
    return builder.as_markup()


def menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Полезная информация', callback_data=ButtonsCallbackFactory(section="menu", action="wiki"))
    builder.button(text='Контроль симптомов', callback_data=ButtonsCallbackFactory(section="menu", action="simptoms"))
    builder.button(text='Запрос на консультацию', callback_data=ButtonsCallbackFactory(section="menu",
                                                                                       action='consultation'))
    builder.button(text='ᐱ', callback_data=ButtonsCallbackFactory(section="menu", action="roll"))
    builder.adjust(1)
    return builder.as_markup()


def simptoms_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text='Внести показания', callback_data=ButtonsCallbackFactory(section="simptoms", action="today"))
    builder.button(text='Предыдущие показания', callback_data=ButtonsCallbackFactory(section="simptoms",
                                                                                     action="calendar"))
    builder.button(text='ᐸ', callback_data=ButtonsCallbackFactory(section="menu", action="comeback"))
    builder.adjust(1)
    return builder.as_markup()


def questionnaire_keyboard(url):
    builder = InlineKeyboardBuilder()
    builder.button(text='Ссылка на опросник', url=url)
    return builder.as_markup()


def wiki_keyboard(pages_data: List[dict], left_page: int, current_page: int, right_page: int):
    builder = InlineKeyboardBuilder()
    for page in pages_data:
        builder.button(text=page['name'], callback_data=ArticleCallbackFactory(page=current_page,
                                                                               article_id=page['id']))
    builder.button(text='ᐸ', callback_data=WikiCallbackFactory(page=left_page))
    builder.button(text='ᐱ', callback_data=ButtonsCallbackFactory(section='menu', action='comeback'))
    builder.button(text='ᐳ', callback_data=WikiCallbackFactory(page=right_page))
    builder.adjust(1, 1, 1, 1, 1, 3)
    return builder.as_markup()


def wiki_page_keyboard(current_page: int):
    builder = InlineKeyboardBuilder()
    builder.button(text='ᐸ', callback_data=WikiCallbackFactory(page=current_page))
    return builder.as_markup()


def url_keyboard(button_text: str, url_string: str):
    builder = InlineKeyboardBuilder()
    builder.button(text=button_text, url=url_string)
    return builder.as_markup()
