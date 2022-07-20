from aiogram import types

TOKEN = "5577256502:AAFGz0lyhXGaBXlSJ-e99kIWbDjvKOLSKtk"

button = ["basket", "buy", "vk", "delete", "buy", "order"]
basket = types.InlineKeyboardButton("Корзина", callback_data='basket')
order = types.InlineKeyboardButton("Заказ", callback_data='order')
vk = types.InlineKeyboardButton("VK Store", url="https://vk.com/koshoshop")
delete = types.InlineKeyboardButton("Убрать с корзины", callback_data="delete")
buy = types.InlineKeyboardButton("Оплатить товары", callback_data="buy")
add_in_order = types.InlineKeyboardButton("Добавить в корзину", callback_data="add_in_order")
select_categories = types.InlineKeyboardButton("Выбрать категорию", callback_data="select_categories")

main = types.InlineKeyboardMarkup(row_width=3)
main.add(basket, order, vk)
basket_item = types.InlineKeyboardMarkup(row_width=2)
basket_item.add(delete, buy)
categories = types.InlineKeyboardMarkup(row_width=1)
categories.add(select_categories)
select_order = types.InlineKeyboardMarkup(row_width=1)
select_order.add(add_in_order)