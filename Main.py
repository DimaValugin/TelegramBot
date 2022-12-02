from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from Functions import scan_id, nakrutka, my_profile, support_client, my_orders, is_number, add_check, \
    get_check, User_money, Set_money, delete_check, new_history, my_history, Start_order, handle_services_id, \
    handle_phone, Services_DB, delete_bad_check
from Config import TOKEN, Qiwi_Token
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from pyqiwip2p import QiwiP2P
import random
import Markups
from datetime import datetime

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,
                storage=storage)
p2p = QiwiP2P(auth_key=Qiwi_Token)


class OrderStatesGroup(StatesGroup):
    phone = State()
    link = State()


class Money(StatesGroup):
    start_refill = State()
    refill = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await scan_id(message, message.from_user.id)


@dp.message_handler(commands=['money'], state=None)
async def start_message(message: types.Message):
    await bot.send_message(message.from_user.id, text='Введите сумму для пополнения')
    await Money.start_refill.set()


@dp.message_handler(commands=['cancel'], state='*')
async def cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.answer('Заказ отменен',
                         reply_markup=Markups.MainMenu)


@dp.message_handler(content_types=['text'])
async def bot_message(message: types.Message):
    if message.text == 'Накрутка':
        await nakrutka(message)

    elif message.text == 'Мой профиль':
        await my_profile(message.from_user.id)

    elif message.text == 'Пополнить баланс':
        await bot.send_message(message.from_user.id, 'Для пополнения баланса напишите команду /money')

    elif message.text == 'Поддержка':
        await support_client(message)

    elif message.text == 'История пополнений':
        await my_history(message, message.from_user.id)

    elif message.text == 'Мои заказы':
        await my_orders(message, message.from_user.id)


@dp.message_handler(content_types=['photo', 'audio', 'document', 'sticker', 'video', 'voice'])
async def get_pictures(message):
    await bot.send_message(message.chat.id, text='Неккоректный запрос')


@dp.message_handler(state=Money.start_refill)
async def bot_message(message: types.Message, state: FSMContext):
    if message.chat.type == "private":
        if is_number(message.text):
            message_money = int(message.text)
            if message_money >= 5:
                comment = str(message.from_user.id) + "-" + str(random.randint(1000, 9999))
                bill = p2p.bill(amount=message_money, lifetime=15, comment=comment)

                add_check(message.from_user.id, message_money, bill.bill_id)

                await bot.send_message(message.from_user.id, f"Вам нужно отправить {message_money} руб. на наш "
                                                             f"Qiwi\nСсылку: {bill.pay_url}\nУказав комментарий к"
                                                             f" оплате: {comment}",
                                       reply_markup=Markups.buy_menu(url=bill.pay_url, bill=bill.bill_id))
                await bot.send_message(message.from_user.id,
                                       'Чтобы продолжить работу бота завершите/прекратите процесс пополнения')
                await Money.next()

            else:
                await bot.send_message(message.from_user.id, 'Минимальная сумма для оплаты')

        else:
            await bot.send_message(message.from_user.id, 'Нужно ввести число')


@dp.callback_query_handler(text='add_money_qiwi')
async def add_money_qiwi(callback: types.CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, "Введите сумму для пополнения")


@dp.callback_query_handler(text_contains='check_', state=Money.refill)
async def answer(callback: types.CallbackQuery, state: FSMContext):
    bill = str(callback.data[6:])
    info = get_check(callback.from_user.id)
    if info is not False:
        if str(p2p.check(bill_id=bill).status) == "PAID":
            user_money = User_money(callback.from_user.id)
            money = int(info[2])
            date = str(datetime.now().strftime("%d-%m-%Y %H:%M"))
            Set_money(callback.from_user.id, user_money + money)
            new_history(callback.from_user.id, money, date)
            delete_check(bill)
            await bot.send_message(callback.from_user.id, text='Ваш счет пополнен!\n'
                                                               'Для проверки баланса нажмите кнопку "Мой профиль"')
            await state.finish()

        else:
            await bot.send_message(callback.from_user.id, text='Вы не оплатили счет!',
                                   reply_markup=Markups.buy_menu(False, bill=bill))
    else:
        await bot.send_message(callback.from_user.id, text='Счет не найден')


@dp.callback_query_handler(text='stop_money', state=Money.refill)
async def stop_money(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    delete_bad_check(callback.message.chat.id)
    await bot.send_message(callback.from_user.id, text='Процесс оплаты прекращен')


@dp.callback_query_handler(text_contains='SN_')
async def answer(callback: types.CallbackQuery):
    if callback.data == 'SN_youtube':
        await bot.send_message(callback.message.chat.id, 'Выберите категорию услуги для YouTube',

                               reply_markup=Markups.YouTube_inline
                               )

    elif callback.data == 'SN_telegram':
        await bot.send_message(callback.message.chat.id, 'Выберите категорию услуги для Telegram',
                               reply_markup=Markups.Telegram_inline
                               )


@dp.callback_query_handler(text='list_of_services')
async def answer(callback: types.CallbackQuery):
    await bot.send_message(callback.message.chat.id, '📈 Выберите сервис для накрутки',

                           reply_markup=Markups.Service_Name_inline
                           )


@dp.callback_query_handler(text_contains='YouTube_')
async def services(callback: types.CallbackQuery):
    if callback.data == 'YouTube_like':
        await Services_DB(callback.message, id=1)

    elif callback.data == 'YouTube_sub':
        await Services_DB(callback.message, id=2)


@dp.callback_query_handler(text_contains='Telegram_')
async def answer(callback: types.CallbackQuery):
    if callback.data == 'Telegram_sub':
        await Services_DB(callback.message, id=3)

    elif callback.data == 'Telegram_view':
        await Services_DB(callback.message, id=4)


@dp.callback_query_handler(text='You_111')
async def order_111(callback: types.CallbackQuery, state: FSMContext):
    await Start_order(callback, state, id=1)


@dp.callback_query_handler(text='You_121')
async def order_121(callback: types.CallbackQuery, state: FSMContext):
    await Start_order(callback, state, id=2)


@dp.callback_query_handler(text='Tel_221')
async def order_221(callback: types.CallbackQuery, state: FSMContext):
    await Start_order(callback, state, id=3)


@dp.callback_query_handler(text='Tel_231')
async def order_231(callback: types.CallbackQuery, state: FSMContext):
    await Start_order(callback, state, id=4)


@dp.message_handler(state=OrderStatesGroup.phone)
async def Youtube_order_phone1(message: types.Message, state: FSMContext):
    await handle_services_id(message, state)


@dp.message_handler(state=OrderStatesGroup.link)
async def Youtube_order_link1(message: types.Message, state: FSMContext):
    await handle_phone(message, state)


executor.start_polling(dp, skip_updates=True)
