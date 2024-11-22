from typing import List

from pydantic import BaseModel, ConfigDict
from datetime import date
from aiogram.filters.callback_data import CallbackData


class ArticleModel(BaseModel):
    id: int
    name: str
    text: str
    link_bool: bool

    model_config = ConfigDict(from_attributes=True)


class SymptomControlModel(BaseModel):
    user_id: int
    question_id: int
    date: date
    answer: str | None

    model_config = ConfigDict(from_attributes=True)


class SymptomQuestionModel(BaseModel):
    id: int
    question: str
    question_subject: str
    answers: List[str] | None

    model_config = ConfigDict(from_attributes=True)

class UserModel(BaseModel):
    telegram_id: int

    model_config = ConfigDict(from_attributes=True)


class ButtonsCallbackFactory(CallbackData, prefix="fabbuttons"):
    section: str
    action: str

class CalendarCallbackFactory(CallbackData, prefix="fabcalendar"):
    date: str
    day: bool

class ControlCallbackFactory(CallbackData, prefix="fabcontrol"):
    question_id: int
    answer: str | None

class WikiCallbackFactory(CallbackData, prefix="fabwiki"):
    page: int

class ArticleCallbackFactory(CallbackData, prefix="fabpage"):
    page: int
    article_id: int
