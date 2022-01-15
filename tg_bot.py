import asyncio
import datetime
import json
from aiogram.dispatcher.filters import Text
from main import check_news_update
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import hbold, hlink
from config import BOT_TOKEN, USER_ID


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def get_fresh_news(message: types.Message):
    """Создаем кнопки"""

    start_buttons = ['Все новости', 'Последние 5 новостей', 'На повестке']
    keyword = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyword.add(*start_buttons)

    await message.answer('Лента новостей', reply_markup=keyword)


@dp.message_handler(Text(equals='Все новости'))
async def get_all_news(message: types.Message):
    """Получаем все новости из нащего спаршеного файла"""

    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)
    # Получаем, сортируем, наши новости и добавляем визуал parse_mode
    for k, v in sorted(news_dict.items()):
        news = f'{hbold(datetime.datetime.fromtimestamp(v["article_date_timestamp"]))}\n' \
               f'{hlink(v["article_title"], v["article_url"])}'
        await message.answer(news)


@dp.message_handler(Text(equals='Последние 5 новостей'))
async def get_last_five_news(message: types.Message):
    """Получаем все новости из нащего спаршеного файла"""

    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)
    # Получаем, сортируем, наши новости и добавляем визуал parse_mode
    for k, v in sorted(news_dict.items())[-5:]:
        news = f'{hbold(datetime.datetime.fromtimestamp(v["article_date_timestamp"]))}\n' \
               f'{hlink(v["article_title"], v["article_url"])}'

        await message.answer(news)


@dp.message_handler(Text(equals='На повестке'))
async def get_fresh_news(message: types.Message):
    """Получаем свежие новости"""

    fresh_news = check_news_update()

    if fresh_news is not None:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                   f"{hlink(v['article_title'], v['article_url'])}"

            await message.answer(news)
    else:

        await message.answer("Пока нет свежих новостей...")


async def news_every_minute():
    """Получаем свежие новости каждые n-минут"""
    while True:
        fresh_news = check_news_update()

        if fresh_news is not None:
            for k, v in sorted(fresh_news.items()):
                news = f"{hbold(datetime.datetime.fromtimestamp(v['article_date_timestamp']))}\n" \
                       f"{hlink(v['article_title'], v['article_url'])}"

                # get your id @userinfobot
                await bot.send_message(USER_ID, news, disable_notification=True)

        else:
            await bot.send_message(USER_ID, "Пока нет свежих новостей...", disable_notification=True)

        await asyncio.sleep(40)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)