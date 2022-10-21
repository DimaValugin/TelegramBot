from telebot import types

#Кнопки главного меню
Wrapping = types.KeyboardButton('Накрутка')
MyProfile = types.KeyboardButton('Мой профиль')
MyOrders = types.KeyboardButton('Мои заказы')
Support = types.KeyboardButton('Поддержка')
TopUpBalance = types.KeyboardButton('Пополнить баланс')

MainMenu = types.ReplyKeyboardMarkup(resize_keyboard=True)
MainMenu.add(Wrapping).add(MyOrders, MyProfile).add(Support, TopUpBalance)


#Меню социальных сетей
YouTube_button = types.InlineKeyboardButton(text='YouTube', callback_data='SN_youtube')
Telegram_button = types.InlineKeyboardButton(text='Telegram', callback_data='SN_telegram')
VK_button = types.InlineKeyboardButton(text='VK', callback_data='SN_vk')

SN_inline = types.InlineKeyboardMarkup()
SN_inline.add(YouTube_button, Telegram_button, VK_button)

Like_button = types.InlineKeyboardButton(text='Лайки', callback_data='SE_like')
Sub_button = types.InlineKeyboardButton(text='Подписчики', callback_data='SE_sub')

SE_inline = types.InlineKeyboardMarkup()
SE_inline.add(Like_button, Sub_button)

