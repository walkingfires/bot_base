import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.session_maker import connection
from bot.users.dao import ArticleDAO
from bot.users.schemas import ArticleModel

articles = [
    ArticleModel(id=1,
                 name='Фильм 1',
                 text='https://www.kinopoisk.ru/film/1229683/',
                 link_bool=True),
    ArticleModel(id=2,
                 name='Фильм 2',
                 text='https://www.kinopoisk.ru/film/1229684/',
                 link_bool=True),
    ArticleModel(id=3,
                 name='Фильм 3',
                 text='https://www.kinopoisk.ru/film/926540/',
                 link_bool=True),
    ArticleModel(id=4,
                 name='Фильм 4',
                 text='https://www.kinopoisk.ru/film/678549/',
                 link_bool=True),
    ArticleModel(id=5,
                 name='Фильм 5',
                 text='https://www.kinopoisk.ru/film/472362/',
                 link_bool=True),
    ArticleModel(id=6,
                 name='Фильм 6',
                 text='https://www.kinopoisk.ru/film/9552/',
                 link_bool=True),
    ArticleModel(id=7,
                 name='Фильм 7',
                 text='https://www.kinopoisk.ru/film/3447/',
                 link_bool=True),
    ArticleModel(id=8,
                 name='Фильм 8',
                 text='https://www.kinopoisk.ru/film/3961/',
                 link_bool=True),
    ArticleModel(id=9,
                 name='Фильм 9',
                 text='https://www.kinopoisk.ru/film/1236063/',
                 link_bool=True),
    ArticleModel(id=10,
                 name='Фильм 10',
                 text='https://www.kinopoisk.ru/film/447301/',
                 link_bool=True),
    ArticleModel(id=11,
                 name='Фильм 11',
                 text='https://www.kinopoisk.ru/film/335/',
                 link_bool=True),
    ArticleModel(id=12,
                 name='Фильм 12',
                 text='https://www.kinopoisk.ru/film/430/',
                 link_bool=True),
    ArticleModel(id=13,
                 name='Фильм 13',
                 text='https://www.kinopoisk.ru/film/5273/',
                 link_bool=True),
    ArticleModel(id=14,
                 name='Фильм 14',
                 text='https://www.kinopoisk.ru/film/84020/',
                 link_bool=True),
    ArticleModel(id=15,
                 name='Фильм 15',
                 text='https://www.kinopoisk.ru/film/271806/',
                 link_bool=True),
]

@connection(commit=True)
async def load_articles(session: AsyncSession) -> None:
    try:
        await ArticleDAO.add_many(session, articles)
    except Exception as e:
        print(f'Не удалось загрузить статьи\n{e}')

if __name__ == '__main__':
    asyncio.run(load_articles())
