from loguru import logger
from pydantic import BaseModel, create_model
from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.base import BaseDAO
from bot.users.models import User, SymptomControl, Article, SymptomQuestion


class ArticleDAO(BaseDAO[Article]):
    model = Article


class UserDAO(BaseDAO[User]):
    model = User

    @classmethod
    async def find_id_by_telegram_id(cls, session: AsyncSession, telegram_id: int):
        FilterModel = create_model(
            'FilterModel',
            telegram_id=(int, ...),
        )
        result = await cls.find_one_or_none(session=session, filters=FilterModel(telegram_id=telegram_id))
        if result:
            return result.id
        else:
            logger.error(f"Ошибка при поиске ID записи c значением {telegram_id}")
            return None


class SymptomControlDAO(BaseDAO[SymptomControl]):
    model = SymptomControl

    @classmethod
    async def find_control_by_question_id(cls, session: AsyncSession, user_id: int, question_id: int):
        FilterModel = create_model(
            'FilterModel',
            user_id=(int, ...),
            question_id=(int, ...),
            date=(date, ...)
        )
        record = await cls.find_one_or_none(session=session, filters=FilterModel(user_id=user_id,
                                                                                 question_id=question_id,
                                                                                 date=date.today()))
        return record

    @classmethod
    async def find_user_symptomcontrol_answers_or_none(cls, session: AsyncSession, filters: BaseModel):
        logger.info(f"Поиск одной записи {cls.model.__name__} по фильтрам: {filters.model_dump(exclude_unset=True)}")
        try:
            query = (
                select(
                    SymptomQuestionDAO.model.question_subject,
                    cls.model.answer
                )
                .join(cls.model,
                      cls.model.question_id == SymptomQuestionDAO.model.id)
                .join(UserDAO.model,
                      cls.model.user_id == UserDAO.model.id)
                .filter(cls.model.date == filters.date)
                .filter(UserDAO.model.telegram_id == filters.telegram_id)
            )
            results = await session.execute(query)
            result_dicts = {result[0]: result[1] for result in results.all()}

            if result_dicts:
                logger.info(f"Запись найдена по фильтрам: {filters.model_dump(exclude_unset=True)}")
                return result_dicts
            else:
                logger.info(f"Запись не найдена по фильтрам: {filters.model_dump(exclude_unset=True)}")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске ответов по фильтрам {filters.model_dump(exclude_unset=True)}: {e}")
            raise

class SymptomQuestionDAO(BaseDAO[SymptomQuestion]):
    model = SymptomQuestion
