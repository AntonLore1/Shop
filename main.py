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
        k = ['Koshō Car Collection | KCC', 'Оригинальные Японские издания', 'Все Цурикава | Tsurikawa', 'Постеры']
        order = types.ReplyKeyboardMarkup(resize_keyboard=True)
        order.add(*k)
        await bot_tg.send_message(query.from_user.id, "Выберите категорию товаров", reply_markup=order)
        await bot_tg.delete_message(query.message.chat.id, query.message.message_id + 1)
        await bot_tg.send_message(query.from_user.id, 'Товары категории "Постеры":')
        await bot_tg.send_photo(query.from_user.id,
                                "https://sun1.sibirix.userapi.com/impg/f5p-6FtfnCkbZmq4sz6JnesfgsS5unkdpNKfgw/d_QvwvPB_p4.jpg?size=520x0&quality=95&sign=eceab7ae197b0009fb513a2dccae0997",
                                caption="""Постер Warp Meet | Nissan GT-R R35 | A2
В наличии: 8 штук
Цена: 505₽""",
                                reply_markup=config.order_item)
    elif query.data == 'buy':
        await bot_tg.send_message(query.from_user.id, "Введите свое ФИО", )






# url = 'https://yamakasiwear.ru/collection/izvestnye-lichnosti?page=2'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('div', class_='empty-catalog-message')
# print(quotes)

if __name__ == '__main__':
    executor.start_polling(bot, skip_updates=True)