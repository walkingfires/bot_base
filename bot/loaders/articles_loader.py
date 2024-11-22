import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.session_maker import connection
from bot.dao.dao import ArticleDAO
from bot.schemas import ArticleModel

articles = [
    ArticleModel(name='Фильм 1', text='https://www.kinopoisk.ru/film/1229683/', link_bool=True),
    ArticleModel(name='Фильм 2', text='https://www.kinopoisk.ru/film/1229684/', link_bool=True),
    ArticleModel(name='Фильм 3', text='https://www.kinopoisk.ru/film/926540/', link_bool=True),
    ArticleModel(name='Фильм 4', text='https://www.kinopoisk.ru/film/678549/', link_bool=True),
    ArticleModel(name='Фильм 5', text='https://www.kinopoisk.ru/film/472362/', link_bool=True),
    ArticleModel(name='Фильм 6', text='https://www.kinopoisk.ru/film/9552/', link_bool=True),
    ArticleModel(name='Фильм 7', text='https://www.kinopoisk.ru/film/3447/', link_bool=True),
    ArticleModel(name='Фильм 8', text='https://www.kinopoisk.ru/film/3961/', link_bool=True),
    ArticleModel(name='Фильм 9', text='https://www.kinopoisk.ru/film/1236063/', link_bool=True),
    ArticleModel(name='Фильм 10', text='https://www.kinopoisk.ru/film/447301/', link_bool=True),
    ArticleModel(name='Фильм 11', text='https://www.kinopoisk.ru/film/335/', link_bool=True),
    ArticleModel(name='Фильм 12', text='https://www.kinopoisk.ru/film/430/', link_bool=True),
    ArticleModel(name='Фильм 13', text='https://www.kinopoisk.ru/film/5273/', link_bool=True),
    ArticleModel(name='Фильм 14', text='https://www.kinopoisk.ru/film/84020/', link_bool=True),
    ArticleModel(name='Фильм 15', text='https://www.kinopoisk.ru/film/271806/', link_bool=True),
]

@connection(commit=True)
async def load_articles(session: AsyncSession) -> None:
    try:
        await ArticleDAO.add_many(session, articles)
    except Exception as e:
        print(f'Не удалось загрузить статьи\n{e}')

if __name__ == '__main__':
    asyncio.run(load_articles())
