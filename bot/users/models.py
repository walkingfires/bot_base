from datetime import date

from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bot.database import Base, uniq_str_an, array_or_none_an


class Article(Base):
    name: Mapped[str]
    text: Mapped[str]
    link_bool: Mapped[bool]


class SymptomControl(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    question_id: Mapped[int] = mapped_column(ForeignKey('symptomquestions.id'))
    date: Mapped[date]
    answer: Mapped[str]

    user: Mapped["User"] = relationship(
        "User",
        back_populates="symptom_controls")

    question: Mapped["SymptomQuestion"] = relationship(
        "SymptomQuestion",
        back_populates="symptom_controls"
    )


class SymptomQuestion(Base):
    question: Mapped[str]
    question_subject: Mapped[uniq_str_an]
    answers: Mapped[array_or_none_an]

    symptom_controls: Mapped[list["SymptomControl"]] = relationship(
        "SymptomControl",
        back_populates="question",
        cascade="all, delete-orphan",
    )


class User(Base):
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)

    symptom_controls: Mapped[list["SymptomControl"]] = relationship(
        "SymptomControl",
        back_populates="user",
        cascade="all, delete-orphan",
    )

# class Mailing(Base):
#     mailing_type: Mapped[MailingEnum]
#     text: Mapped[str]
#     link_bool: Mapped[bool]
#     mailing_date: Mapped[datetime]
