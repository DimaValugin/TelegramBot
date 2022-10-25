import sqlite3
import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from Functions import scan_id, set_money, is_number, nakrutka, my_profile, support_client, refill, create_orders
from Config import TOKEN, NAME_DB
import Markups

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))


@dp.message_handler(commands=['start'])
async def start(message):
    await scan_id(message)


# @dp.message_handler(commands=['orders'])
# async def orders_orders(message: types.Message):
#     await bot.send_message(message.chat.id, text='Введите данные')
#     await create_orders(message)
#
#
# @dp.message_handler(commands=['money'])
# async def money(message):
#     await bot.send_message(message.chat.id, text='Введите сумму для пополнения')
#     await set_money(money)


@dp.message_handler(content_types=['text'])
async def bot_message(message: types.Message):
    if message.text == 'Накрутка':
        await nakrutka(message)

    elif message.text == 'Мой профиль':
        await my_profile(message)

    elif message.text == 'Пополнить баланс':
        await refill(message)

    elif message.text == 'Поддержка':
        await support_client(message)


@dp.message_handler(content_types=['photo', 'audio', 'document', 'sticker', 'video', 'voice'])
async def get_pictures(message):
    await bot.send_message(message.chat.id, text='Неккоректный запрос')


@dp.callback_query_handler(text_contains='')
async def answer(callback: types.CallbackQuery):
    if callback.data == 'SN_youtube':
        await bot.send_message(callback.message.chat.id, 'Выберите категорию услуги',

                               reply_markup=Markups.SE_inline
                               )
    elif callback.data == 'SN_telegram':
        await bot.send_message(callback.message.chat.id, 'Выберите категорию услуги',
                               reply_markup=Markups.SE_inline
                               )


executor.start_polling(dp, skip_updates=True)
