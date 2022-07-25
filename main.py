
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import config
import requests
from script import ScriptsBot
import re



logging.basicConfig(level=logging.INFO)
bot_tg = Bot(token=config.TOKEN)
bot = Dispatcher(bot_tg, storage=MemoryStorage())
database = ScriptsBot('shop.db')
url_store = f'https://api.vk.com/method/market.getAlbums?owner_id={config.owner_id}&count=100&access_token={config.access_token}&v={config.v}'
response = requests.get(url_store)


class Data(StatesGroup):
    categories = State()
    name = State()
    id = State()
    count = State()
    address = State()
    index = State()
    phone = State()
    img = State()
    price = State()
    tag = State()

@bot.message_handler(commands=['start'])
async def main(message: types.Message):
    caption = '<b>Косё</b> — бренд стикеров и аксессуаров, вдохновленный японской автомобильной культурой 80-90-х годов.'
    await bot_tg.send_photo(message.from_user.id, "https://sun9-25.userapi.com/impf/c857732/v857732109/22d94/CdyHGbDzhBo.jpg?size=1078x1080&quality=96&sign=83d21d7a417022c35b592af7c34eb734&type=album",
                         caption=caption,
                         reply_markup=config.main,
                         parse_mode='HTML')

@bot.callback_query_handler(text=config.button)
async def callback_inline(query: types.CallbackQuery, state: FSMContext):
    try:
        if query.data == 'basket':
            await bot_tg.send_message(query.from_user.id, "Список товаров в вашей корзине:")
            for item in database.get_info_item(query.from_user.id):
                await bot_tg.send_photo(query.from_user.id, f'{item[3]}',
                                        caption=f"""{item[1]}
Цена: {item[4]}₽
Количество: {item[2]}""",
                                        reply_markup=config.basket_item)
            await bot_tg.send_message(query.from_user.id, f"Общая стоимость товаров в вашей корзине: {database.get_price_items(query.from_user.id)}₽", reply_markup=config.buy_order)

        elif query.data == 'order':
            categories = []
            for item in response.json()['response']['items']:
                categories.append(item.get('title'))
            order = types.ReplyKeyboardMarkup(resize_keyboard=True)
            order.add(*categories)
            await bot_tg.send_message(query.from_user.id, "Выберите категорию товаров", reply_markup=order)
            await Data.categories.set()
        elif query.data == 'buy':
            await bot_tg.send_message(query.from_user.id, "Введите свое ФИО")
            await Data.name.set()
        elif query.data == 'add_in_order':
            await state.update_data(title=((query.message.caption).split('\n'))[0])
            await state.update_data(img=(query.message.photo)[0]['file_id'])
            await state.update_data(price=''.join(re.findall("\d+", ((query.message.caption).split('\n'))[1])))
            await bot_tg.send_message(query.from_user.id, "Введите кол-во товара")
            await Data.count.set()
        elif query.data == 'delete':
            database.delete_item(((query.message.caption).split('\n'))[0], query.from_user.id)
            await bot_tg.send_message(query.from_user.id, "Товар удален с корзины")
    except:
        print('Error in function callback_inline')
@bot.message_handler(content_types='text', state=Data.categories)
async def order_items(message: types.Message, state: FSMContext):
    try:
        await bot_tg.send_message(message.from_user.id, 'Wait...', reply_markup=types.ReplyKeyboardRemove())
        await bot_tg.delete_message(message.chat.id, message.message_id + 1)
        titles = [item.get('title') for item in response.json()['response']['items']]
        if message.text in titles:
            await bot_tg.send_message(message.from_user.id, f'Категория товаров "{message.text}"')
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
                                response_album = requests.get(f'https://api.vk.com/method/market.get?owner_id=-124544144&album_id={album_id}&count={count}&offset={200*ind}&access_token={config.access_token}&v={config.v}')
                                for item in response_album.json()['response']['items']:
                                    caption = f"{item.get('title')}\nЦена: {item.get('price').get('text')}"
                                    await bot_tg.send_photo(message.from_user.id,
                                                            item.get('thumb_photo'),
                                                            caption=caption,
                                                            reply_markup=config.select_order,)
                            ind = ind + 1
                    else:
                        response_album = requests.get(f'https://api.vk.com/method/market.get?owner_id=-124544144&album_id={album_id}&count={album_count}&access_token={config.access_token}&v={config.v}')
                        for item in response_album.json()['response']['items']:
                            caption = f"{item.get('title')}\nЦена: {item.get('price').get('text')}"
                            await bot_tg.send_photo(message.from_user.id,
                                                    item.get('thumb_photo'),
                                                    caption=caption,
                                                    reply_markup=config.select_order)
            await state.finish()
        else:
            categories = []
            for item in response.json()['response']['items']:
                categories.append(item.get('title'))
            order = types.ReplyKeyboardMarkup(resize_keyboard=True)
            order.add(*categories)
            await bot_tg.send_message(message.from_user.id, "Выберите категорию из предложенных", reply_markup=order)
    except:
        print('Error in function order_items')
@bot.message_handler(content_types='text', state=Data.name)
async def get_name(message: types.Message, state: FSMContext):
    try:
        name = message.text
        await state.update_data(name=name)
        await bot_tg.send_message(message.from_user.id, "Введите свой адрес")
        await Data.address.set()
    except:
        print('Error in function get_name')
@bot.message_handler(content_types='text', state=Data.address)
async def get_address(message: types.Message, state: FSMContext):
    try:
        address = message.text
        await state.update_data(address=address)
        await bot_tg.send_message(message.from_user.id, "Введите свой почтовый индекс")
        await Data.index.set()
    except:
        print('Error in function get_address')
@bot.message_handler(content_types='text', state=Data.index)
async def get_index(message: types.Message, state: FSMContext):
    try:
        index = message.text
        await state.update_data(index=index)
        await bot_tg.send_message(message.from_user.id, "Введите свой Telegram тэг")
        await Data.tag.set()
    except:
        print('Error in function get_index')
@bot.message_handler(content_types='text', state=Data.tag)
async def get_tag(message: types.Message, state: FSMContext):
    try:
        tag = message.text
        await state.update_data(tag=tag)
        await bot_tg.send_message(message.from_user.id, "Введите свой номер телефона для связи с Вами")
        await Data.phone.set()
    except:
        print('Error in function get_tag')

@bot.message_handler(content_types='text', state=Data.phone)
async def get_phone(message: types.Message, state: FSMContext):
    try:
        phone = message.text
        await state.update_data(phone=phone)
        info = await state.get_data()
        await bot_tg.send_message(message.from_user.id, 'Заказ успешно оформлен')
        await bot_tg.send_message(message.from_user.id, f"""<b>Заказ</b>
        
    <u>Товары:</u>
    {database.get_items(message.from_user.id)}
<u>Общая стоимость товаров:</u> {database.get_price_items(message.from_user.id)}₽
        
<u>ФИО:</u> {info['name']}
<u>Адрес:</u> {info['address']}
<u>Индекс:</u> {info['index']}
<u>Telegram тэг:</u> {info['tag']}
<u>Номер телефона:</u> {info['phone']}""",
        parse_mode='HTML')
        await state.finish()
    except:
        print('Error in function get_phone')

@bot.message_handler(content_types='text', state=Data.count)
async def get_count(message: types.Message, state: FSMContext):
    try:
        count = message.text
        if count.isdigit() == True:
            id = message.from_user.id
            info = await state.get_data()
            await state.finish()
            database.add_in_order(id, info['title'], count, info['img'], info['price'])
            await bot_tg.send_message(message.from_user.id, 'Товар добавлен в корзину')
        else:
            await bot_tg.send_message(message.from_user.id, 'Введите корректное количество')
    except:
        print('Error in function get_count')

if __name__ == '__main__':
    executor.start_polling(bot, skip_updates=True)