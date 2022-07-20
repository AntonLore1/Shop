from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import config
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
bot_tg = Bot(token=config.TOKEN)
bot = Dispatcher(bot_tg, storage=MemoryStorage())
url_store = 'https://vk.com/market-124544144'
response = requests.get(url_store)
content = BeautifulSoup(response.text, 'lxml')

class Data(StatesGroup):
    categories = State()

@bot.message_handler(commands=['start'])
async def main(message: types.Message):
    caption = 'Косё — бренд стикеров и аксессуаров, вдохновленный японской автомобильной культурой 80-90-х годов.'
    await bot_tg.send_photo(message.from_user.id, "https://sun9-25.userapi.com/impf/c857732/v857732109/22d94/CdyHGbDzhBo.jpg?size=1078x1080&quality=96&sign=83d21d7a417022c35b592af7c34eb734&type=album",
                         caption=caption,
                         reply_markup=config.main)

@bot.callback_query_handler(text=config.button)
async def callback_inline(query: types.CallbackQuery):
    if query.data == 'basket':
        await bot_tg.send_message(query.from_user.id, "Список товаров в вашей корзине:")
        await bot_tg.send_photo(query.from_user.id, "https://sun1.sibirix.userapi.com/impg/yPGSmp_UTaTj4N1ocJ6gZD1-rj387dfHo0ht7A/0LL2adX3gMk.jpg?size=520x0&quality=95&sign=546e513453509e102f55ab47175b2b4f",
                                caption="""Стикер Nissan Laurel C33 | KCC
                                Количество: 5
                                Цена: 99 ₽""",
                                reply_markup=config.basket_item)
    elif query.data == 'order':


        categories = []
        items = content.find_all('div', class_='AlbumItemInfo__title')
        for item in items:
            categories.append(item.text)
        order = types.ReplyKeyboardMarkup(resize_keyboard=True)
        order.add(*categories)
        await bot_tg.send_message(query.from_user.id, "Выберите категорию товаров", reply_markup=order)
        await Data.categories.set()




    elif query.data == 'buy':
        await bot_tg.send_message(query.from_user.id, "Введите свое ФИО", )

@bot.message_handler(content_types='text', state=Data.categories)
async def order_items(message: types.Message, state: FSMContext):
    url_categories = "https://vk.com/"
    blocks = content.find_all('div', class_='AlbumsBlock__album')
    for item in blocks:
        if str(item.find('div', class_='AlbumItemInfo__title').text) == message.text:
            id_categories = item.find('a', class_='AlbumItem al_album', href=True)
            url_categories = url_categories + id_categories['href']
    response_categories = requests.get(url_categories)
    content_categories = BeautifulSoup(response_categories.text, 'lxml')
    await bot_tg.send_message(message.from_user.id, f'Товары категории "{message.text}":')
    for item in content_categories.find_all('div', class_='MarketItems__card'):
        name = item.find('div', class_='MarketItemCard__name MarketItemCard__name--multiline').text
        price = item.find('div', class_='MarketItemCard__currentPrice').text
        caption = f'{name}\nЦена: {price}'
        await bot_tg.send_photo(message.from_user.id,
                                item.find('img').get('src'),
                                caption=caption,
                                reply_markup=config.select_order)




# url = 'https://yamakasiwear.ru/collection/izvestnye-lichnosti?page=2'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('div', class_='empty-catalog-message')
# print(quotes)

if __name__ == '__main__':
    executor.start_polling(bot, skip_updates=True)