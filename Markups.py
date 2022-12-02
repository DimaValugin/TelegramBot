from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

# Кнопки главного меню
Wrapping = KeyboardButton('Накрутка')
MyProfile = KeyboardButton('Мой профиль')
MyOrders = KeyboardButton('Мои заказы')
Support = KeyboardButton('Поддержка')
TopUpBalance = KeyboardButton('Пополнить баланс')
History = KeyboardButton('История пополнений')

MainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(Wrapping).add(TopUpBalance).add(MyOrders, History).add(Support,MyProfile)

########################################################################################################################

# Меню социальных сетей
YouTube_button = InlineKeyboardButton(text='YouTube', callback_data='SN_youtube')
Telegram_button = InlineKeyboardButton(text='Telegram', callback_data='SN_telegram')

Service_Name_inline = InlineKeyboardMarkup()
Service_Name_inline.add(YouTube_button, Telegram_button)

# Услуги для YouTube
YouTube_Like_button = InlineKeyboardButton(text='Лайки', callback_data='YouTube_like')
YouTube_Sub_button = InlineKeyboardButton(text='Подписчики', callback_data='YouTube_sub')

YouTube_inline = InlineKeyboardMarkup()
YouTube_inline.add(YouTube_Like_button, YouTube_Sub_button)

# Услуги для Telegram
Telegram_Sub_button = InlineKeyboardButton(text='Подписчики', callback_data='Telegram_sub')
Telegram_View_button = InlineKeyboardButton(text='Просмотры', callback_data='Telegram_view')

Telegram_inline = InlineKeyboardMarkup()
Telegram_inline.add(Telegram_Sub_button, Telegram_View_button)

########################################################################################################################

Youtube_buy_like_111 = InlineKeyboardButton(text='Купить', callback_data='You_111')
Youtube_buy_like111 = InlineKeyboardMarkup()
Youtube_buy_like111.add(Youtube_buy_like_111)

Youtube_buy_sub_121 = InlineKeyboardButton(text='Купить', callback_data='You_121')
Youtube_buy_sub121 = InlineKeyboardMarkup()
Youtube_buy_sub121.add(Youtube_buy_sub_121)

Button_221 = InlineKeyboardButton(text='Купить', callback_data='Tel_221')
Telegram_inline_221 = InlineKeyboardMarkup()
Telegram_inline_221.add(Button_221)

Button_231 = InlineKeyboardButton(text='Купить', callback_data='Tel_231')
Telegram_inline_231 = InlineKeyboardMarkup()
Telegram_inline_231.add(Button_231)

########################################################################################################################
#                                           Кнопка для отмены заказа

Cancel_button = KeyboardButton('/cancel')

Get_cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(Cancel_button)

Add_money_button = InlineKeyboardButton(text='Пополнить баланс', callback_data='add_money')

Add_money = InlineKeyboardMarkup()
Add_money.add(Add_money_button)

###########################################################################################
#                           Кнопки для пополнения баланса qiwi

Add_money = InlineKeyboardButton(text='Пополнить баланс', callback_data='add_money_qiwi')
Delete_Chek = InlineKeyboardButton(text='Прекратить процесс оплаты', callback_data='stop_money')

Add_money_qiwi = InlineKeyboardMarkup()
Add_money_qiwi.add(Add_money)


def buy_menu(isUrl=True, url="", bill=""):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQiwi = InlineKeyboardMarkup(text="Ссылка на оплату", url=url)
        qiwiMenu.insert(btnUrlQiwi)

    btnCheckQiwi = InlineKeyboardMarkup(text="Проверить оплату", callback_data="check_" + bill)
    qiwiMenu.insert(btnCheckQiwi)
    qiwiMenu.insert(Delete_Chek)
    return qiwiMenu

