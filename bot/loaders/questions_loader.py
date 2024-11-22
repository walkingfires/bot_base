import asyncio
from typing import List

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.session_maker import connection
from bot.dao.dao import SymptomQuestionDAO
from bot.schemas import SymptomQuestionModel


@connection(commit=True)
async def load_questions(session: AsyncSession, instances: List[BaseModel]) -> None:
    try:
        await SymptomQuestionDAO.add_many(session, instances)
    except Exception as e:
        print(f'Не удалось загрузить статьи\n{e}')

if __name__ == '__main__':
    questions = [
        SymptomQuestionModel(id=1, question='Вопрос 1', question_subject='Субъект 1', answers=['Ответ 1', 'Ответ 2', 'Ответ 3', 'Ответ 4']),
        SymptomQuestionModel(id=2, question='Вопрос 2', question_subject='Субъект 2', answers=['Ответ 1', 'Ответ 2', 'Ответ 3', 'Ответ 4']),
        SymptomQuestionModel(id=3, question='Вопрос 3', question_subject='Субъект 3', answers=['Ответ 1', 'Ответ 2', 'Ответ 3', 'Ответ 4']),
        SymptomQuestionModel(id=4, question='Вопрос 4', question_subject='Субъект 4', answers=['Ответ 1', 'Ответ 2', 'Ответ 3', 'Ответ 4']),
        SymptomQuestionModel(id=5, question='Вопрос 5', question_subject='Субъект 5', answers=['Ответ 1', 'Ответ 2', 'Ответ 3', 'Ответ 4']),
    ]
    asyncio.run(load_questions(instances=questions))
