from aiogram.types import Message
from aiogram.utils.markdown import hide_link
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
import numpy as np

from bot.dao.session_maker import connection
from bot.users.keybords.keyboards import wiki_keyboard, wiki_page_keyboard
from bot.users.dao import ArticleDAO
from bot.users.schemas import ArticleModel, ArticleCallbackFactory


@connection(commit=False)
async def cb_wiki(message: Message, session: AsyncSession, page: int = 1):
    user_id = message.from_user.id
    try:
        pages_list = np.arange(1, np.ceil(await ArticleDAO.count(session=session) / 5) + 1, dtype=int)

        pages = await ArticleDAO.paginate(session=session, page=page, page_size=5)
        pages_data = [ArticleModel.model_validate(i).model_dump() for i in pages]

        await message.edit_text(
            "Выберите article",
            reply_markup=wiki_keyboard(pages_data=pages_data,
                                       left_page=pages_list[page - 2],
                                       current_page=page,
                                       right_page=pages_list[page % len(pages_list)])
        )

    except Exception as e:
        logger.error(f"Ошибка при выполнении команды /wiki для пользователя {user_id}: {e}")
        await message.edit_reply_markup()
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")


@connection(commit=False)
async def cb_wiki_page(message: Message, session: AsyncSession, page_data: ArticleCallbackFactory):
    user_id = message.from_user.id
    try:
        article_info = await ArticleDAO.find_one_or_none_by_id(session=session, data_id=page_data.article_id)
        if article_info:
            article = ArticleModel.model_validate(article_info).model_dump()
            if article['link_bool']:
                await message.edit_text(
                    f"{hide_link(article['text'])}{article['name']}",
                    reply_markup=wiki_page_keyboard(current_page=page_data.page)
                )
            else:
                await message.edit_text(
                    f"{article['name']}\n{article['text']}",
                    reply_markup=wiki_page_keyboard(current_page=page_data.page)
                )
        # TODO: if else hole
    except Exception as e:
        logger.error(f"Ошибка при выполнении команды callback wiki_page для пользователя {user_id}: {e}")
        await message.edit_reply_markup()
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова позже.")