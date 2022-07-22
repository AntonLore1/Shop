from aiogram import types

TOKEN = '5577256502:AAFGz0lyhXGaBXlSJ-e99kIWbDjvKOLSKtk'
access_token = 'vk1.a.z0FBiWRvLPY69U7dSOcfqyiaWPXe6gmt1ukM_JDZRfP4NVaTrM2yufz7LyNAJH3xOGYFBuSCJ2MU2l4TMGXLb8pbjPYz3KFrUqhyXqE5LovY1Gow2cP_oE2rJbUeqGpD_sUUl8w2089d_yTUVsE8fP42kEJTEy6m3RrxfUTHfSDC1SCDQkQhoect2mOuJ6YD'
owner_id = '-124544144'
v = '5.131'

button = ["basket", "buy", "vk", "delete", "buy", "order", "add_in_order"]
basket = types.InlineKeyboardButton("Корзина", callback_data='basket')
order = types.InlineKeyboardButton("Заказ", callback_data='order')
vk = types.InlineKeyboardButton("VK Store", url="https://vk.com/koshoshop")
delete = types.InlineKeyboardButton("Убрать с корзины", callback_data="delete")
buy = types.InlineKeyboardButton("Оформить заказ", callback_data="buy")
add_in_order = types.InlineKeyboardButton("Добавить в корзину", callback_data="add_in_order")
select_categories = types.InlineKeyboardButton("Выбрать категорию", callback_data="select_categories")

main = types.InlineKeyboardMarkup(row_width=3)
main.add(basket, order, vk)
basket_item = types.InlineKeyboardMarkup(row_width=2)
basket_item.add(delete)
categories = types.InlineKeyboardMarkup(row_width=1)
categories.add(select_categories)
select_order = types.InlineKeyboardMarkup(row_width=1)
select_order.add(add_in_order)
buy_order = types.InlineKeyboardMarkup(row_width=1)
buy_order.add(buy)