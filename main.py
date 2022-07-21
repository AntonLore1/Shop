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
access_token = 'vk1.a.0_uidx0Yt7cPKAuk0SR4nMF9iVoxMm3gQrXZxLFoJnJ_U4Z1s0YoA5RvPNZgEbcfj76p6-b8s3_L_Mnt56yR5BVquDSrXJhdLvxchpyPi4E0XRivLio_YoN1r1Fkk52-Q4shrPlDLRnkFWZvs8q28KL32Ydddl30CZZcZhxyaOiedUsFJtDbG8e5xAPEHSmT'
owner_id = '-124544144'
url_store = f'https://api.vk.com/method/market.getAlbums?owner_id={owner_id}&count=22&access_token={access_token}&v=5.131'

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
        for item in response.json()['response']['items']:
            categories.append(item.get('title'))
        order = types.ReplyKeyboardMarkup(resize_keyboard=True)
        order.add(*categories)
        await bot_tg.send_message(query.from_user.id, "Выберите категорию товаров", reply_markup=order)
        await Data.categories.set()
    elif query.data == 'buy':
        await bot_tg.send_message(query.from_user.id, "Введите свое ФИО", )

@bot.message_handler(content_types='text', state=Data.categories)
async def order_items(message: types.Message, state: FSMContext):
    await bot_tg.send_message(message.from_user.id, 'Wait...', reply_markup=types.ReplyKeyboardRemove())
    await bot_tg.delete_message(message.chat.id, message.message_id + 1)
    for item in response.json()['response']['items']:
        name = item.get('title')
        if name == message.text:
            album_id = item.get('id')
            album_count = item.get('count')
            if album_count > 200:
                l = [200 for x in range(album_count // 200)]
                l.append(album_count - (200 * (album_count // 200)))
                ind = 0
                for count in l:
                    if ind == len(l) - 1:
                        break
                    else:
                        response_album = requests.get(f'https://api.vk.com/method/market.get?owner_id=-124544144&album_id={album_id}&count={count}&offset={200*ind}&access_token=vk1.a.0_uidx0Yt7cPKAuk0SR4nMF9iVoxMm3gQrXZxLFoJnJ_U4Z1s0YoA5RvPNZgEbcfj76p6-b8s3_L_Mnt56yR5BVquDSrXJhdLvxchpyPi4E0XRivLio_YoN1r1Fkk52-Q4shrPlDLRnkFWZvs8q28KL32Ydddl30CZZcZhxyaOiedUsFJtDbG8e5xAPEHSmT&v=5.131')
                        for item in response_album.json()['response']['items']:
                            caption = f"{item.get('title')}\nЦена: {item.get('price').get('text')}"
                            await bot_tg.send_photo(message.from_user.id,
                                                    item.get('thumb_photo'),
                                                    caption=caption,
                                                    reply_markup=config.select_order,)
                    ind = ind + 1
            else:
                response_album = requests.get(f'https://api.vk.com/method/market.get?owner_id=-124544144&album_id={album_id}&count={album_count}&access_token=vk1.a.0_uidx0Yt7cPKAuk0SR4nMF9iVoxMm3gQrXZxLFoJnJ_U4Z1s0YoA5RvPNZgEbcfj76p6-b8s3_L_Mnt56yR5BVquDSrXJhdLvxchpyPi4E0XRivLio_YoN1r1Fkk52-Q4shrPlDLRnkFWZvs8q28KL32Ydddl30CZZcZhxyaOiedUsFJtDbG8e5xAPEHSmT&v=5.131')
                for item in response_album.json()['response']['items']:
                    caption = f"{item.get('title')}\nЦена: {item.get('price').get('text')}"
                    await bot_tg.send_photo(message.from_user.id,
                                            item.get('thumb_photo'),
                                            caption=caption,
                                            reply_markup=config.select_order)

    await state.finish()
    # for item in blocks:
    #     if str(item.find('div', class_='AlbumItemInfo__title').text) == message.text:
    #         id_categories = item.find('a', class_='AlbumItem al_album', href=True)
    #         url_categories = url_categories + id_categories['href']
    # response_categories = requests.get(url_categories)
    # content_categories = BeautifulSoup(response_categories.text, 'lxml')
    # await bot_tg.send_message(message.from_user.id, f'Товары категории "{message.text}":')
    # for item in content_categories.find_all('div', class_='MarketItems__card'):
    #     name = item.find('div', class_='MarketItemCard__name MarketItemCard__name--multiline').text
    #     price = item.find('div', class_='MarketItemCard__currentPrice').text
    #     caption = f'{name}\nЦена: {price}'
    #     await bot_tg.send_photo(message.from_user.id,
    #                             item.find('img').get('src'),
    #                             caption=caption,
    #                             reply_markup=config.select_order)




# url = 'https://yamakasiwear.ru/collection/izvestnye-lichnosti?page=2'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('div', class_='empty-catalog-message')
# print(quotes)

if __name__ == '__main__':
    executor.start_polling(bot, skip_updates=True)