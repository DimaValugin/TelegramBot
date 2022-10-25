from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, reply_keyboard, ReplyKeyboardMarkup

#Кнопки главного меню
Wrapping = KeyboardButton('Накрутка')
MyProfile = KeyboardButton('Мой профиль')
MyOrders = KeyboardButton('Мои заказы')
Support = KeyboardButton('Поддержка')
TopUpBalance = KeyboardButton('Пополнить баланс')

MainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(Wrapping).add(MyOrders, MyProfile).add(Support, TopUpBalance)

#Меню социальных сетей
YouTube_button = InlineKeyboardButton(text='YouTube', callback_data='SN_youtube')
Telegram_button = InlineKeyboardButton(text='Telegram', callback_data='SN_telegram')
VK_button = InlineKeyboardButton(text='VK', callback_data='SN_vk')

SN_inline = InlineKeyboardMarkup()
SN_inline.add(YouTube_button, Telegram_button, VK_button)

Like_button = InlineKeyboardButton(text='Лайки', callback_data='SE_like')
Sub_button = InlineKeyboardButton(text='Подписчики', callback_data='SE_sub')

SE_inline = InlineKeyboardMarkup()
SE_inline.add(Like_button, Sub_button)

