import time
from Functions import *
import Markups
from Config import TOKEN


bot = telebot.TeleBot(TOKEN)
tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))


@bot.message_handler(commands=['start'])
def start(message):
    scan_id(message)


# @bot.message_handler()
# async def refill(message: types.Message):
#     bot.send_message(message.from_user.id, "Введите сумму")
#     if message.chat.type == 'private':
#         if is_number(message.text):
#             message_money = int(message.text)
#             if message_money >= 5:
#                 pass
#             else:
#                 await bot.send_message(message.from_user.id, "Минимальная сумма для пополнения 5 руб.")
#         else:
#             await bot.send_message(message.from_user.id, "Введите число")


@bot.message_handler(commands=['money'])
def money(message):
    bot.send_message(message.chat.id, text='Введите сумму для пополнения')
    set_money(money)


# @bot.message_handler(commands=['orders'])
# def send_services_id(message):
#     msg = bot.send_message(message.chat.id, "Введите id услуги")
#     bot.register_next_step_handler(msg, send_amount)
#
#
# def send_amount(message):
#     msg = bot.send_message(message.chat.id, "Введите количество")
#     bot.register_next_step_handler(msg, send_phone)
#
#
# def send_phone(message):
#     msg = bot.send_message(message.chat.id, "Введите количество")
#     bot.register_next_step_handler(msg, send_link)
#
#
# def send_link(message):
#     msg = bot.send_message(message.chat.id, "Введите количество")
#     bot.register_next_step_handler(msg, exit)
#
#
# def exit(message):
#     connect = sqlite3.connect(NAME_DB)
#     cursor = connect.cursor()
#
#     cursor.execute('INSERT INTO orders (services_id, amount, phone, link) VALUES(?, ?, ?, ?)', (services_id, amount,
#                                                                                                 phone, link))
#     connect.commit()


@bot.message_handler(content_types=['photo', 'audio', 'document', 'sticker', 'video', 'voice'])
def get_pictures(message):
    bot.send_message(message.chat.id, text='Неккоректный запрос')


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.text == 'Накрутка':
        nakrutka(message)

    elif message.text == 'Мой профиль':
        my_profile(message)

    elif message.text == 'Пополнить баланс':
        bot.send_message(message.from_user.id, "Введите сумму")

    elif message.text == 'Поддержка':
        support_client(message)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'SN_youtube':
        bot.send_message(call.message.chat.id, 'Выберите категорию услуги',

                         reply_markup=Markups.SE_inline
                         )
    elif call.data == 'SN_telegram':
        bot.send_message(call.message.chat.id, 'Выберите категорию услуги',
                         reply_markup=Markups.SE_inline
                         )


bot.polling(none_stop=True)
