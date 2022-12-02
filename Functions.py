import sqlite3
from Config import NAME_DB
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, types
from Config import TOKEN
from aiogram.dispatcher import FSMContext
import Markups
from fpdf import FPDF

bot = Bot(token=TOKEN)
pdf = FPDF()


class OrderStatesGroup(StatesGroup):
    phone = State()
    link = State()


async def start(message):
    await scan_id(message)


async def support_client(message):
    await bot.send_message(message.chat.id, '⚙Если возникли проблемы при работе с ботом,\n'
                                            ' можете обратиться в службу поддержки.\n\n'
                                            'Контактная информация:\n'
                                            'Телефон: +7 643 267 4568\n'
                                            'E-mail: testtest@mail.ru\n')


async def nakrutka(message):
    await bot.send_message(message.chat.id, '📈 Выберите сервис для накрутки',
                           reply_markup=Markups.Service_Name_inline
                           )


async def scan_id(message, id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    connect.commit()
    user_money = 0
    cursor.execute(f"SELECT id FROM login_id WHERE id = ?", (id,))
    data = cursor.fetchone()
    if data is None:
        user_data = [message.chat.id, message.from_user.first_name, message.from_user.last_name, user_money]

        cursor.execute("INSERT INTO login_id VALUES(?,?,?,?);", user_data)
    await bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!'.format(message.from_user),
                           reply_markup=Markups.MainMenu)
    connect.commit()
    connect.close()


async def my_profile(id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM login_id WHERE id = ?", (id,))
    records = cursor.fetchall()
    for row in records:
        await bot.send_message(id, '👤 Мой профиль\n\n'
                                   f'ID: {row[0]}\n'
                                   f'Имя: {row[1]}\n'
                                   f'Фамилия: {row[2]}\n'
                                   f'Баланс: {row[3]}\n',
                               reply_markup=Markups.MainMenu
                               )
    connect.commit()


async def new_create_orders(state, message):
    async with state.proxy() as data:
        data['user_id'] = message.chat.id
        data['status'] = 'В процессе'
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
    order = cursor.execute('INSERT INTO orders (user_id, services_id, amount, money, phone, link, status)'
                           ' VALUES(?, ?, ?, ?, ?, ?, ?)',
                           (data['user_id'], data['services_id'], data['amount'], data['money'],
                            data['phone'], data['link'], data['status']))
    connect.commit()
    return order


async def my_orders(message, id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    try:
        cursor.execute(f"SELECT * FROM orders WHERE user_id = ?", (id,))
        records = cursor.fetchall()
        if not records:
            await bot.send_message(message.chat.id, 'Заказов нет')
        else:
            await bot.send_message(message.chat.id, '👤 Мои заказы\n\n')
        for row in records:
            await bot.send_message(message.chat.id, f'ID заказа: {row[0]}\n'
                                                    f'ID услуги: {row[2]}\n'
                                                    f'Количество: {row[3]}\n'
                                                    f'Цена: {row[4]}\n'
                                                    f'Телефон: {row[5]}\n'
                                                    f'Ссылка: {row[6]}\n'
                                                    f'Статус: {row[7]}\n',
                                   reply_markup=Markups.MainMenu
                                   )
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if connect:
            connect.close()


def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False


def User_exists(user_id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    result = cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?'", (user_id,)).fetchall()
    return bool(len(result))


def User_money(id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    result = cursor.execute(f"SELECT money FROM 'login_id' WHERE id = ?", (id,)).fetchmany(1)
    return int(result[0][0])


def Set_money(id, money):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    money_check = cursor.execute(f"UPDATE 'login_id' SET 'money' = ?  WHERE id = ?", (money, id,))
    connect.commit()
    return money_check


def add_check(user_id, money, bill_id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    cursor.execute("INSERT INTO 'check' ('user_id', 'money', 'bill_id') VALUES (?,?,?)", (user_id, money, bill_id,))
    connect.commit()


def get_check(user_id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    result = cursor.execute(f"SELECT * FROM 'check' WHERE user_id = ?", (user_id,)).fetchmany(1)
    print(result)
    if not bool(len(result)):
        return False
    else:
        return result[0]


def delete_check(bill_id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    check_delete = cursor.execute("DELETE FROM 'check' WHERE bill_id = ?", (bill_id,))
    connect.commit()
    return check_delete


def delete_bad_check(user_id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    check_bad_delete = cursor.execute("DELETE FROM 'check' WHERE user_id = ?", (user_id,))
    connect.commit()
    return check_bad_delete


def new_history(user_id, money, date):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    cursor.execute("INSERT INTO 'history' ('user_id', 'money', 'date') VALUES (?,?,?)", (user_id, money, date,))
    connect.commit()


async def my_history(message, id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    try:
        cursor.execute(f"SELECT * FROM history WHERE user_id = ?", (id,))
        records = cursor.fetchall()
        if not records:
            await bot.send_message(message.chat.id, 'История пополнений отсутсвует')
        else:
            await bot.send_message(message.chat.id, '💸История пополнений\n\n')
        for row in records:
            await bot.send_message(message.chat.id, f'Система: Qiwi\n'
                                                    f'Сумма: {row[2]}\n'
                                                    f'Дата: {row[3]}\n',
                                   reply_markup=Markups.MainMenu
                                   )
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if connect:
            connect.close()


async def Services_DB(message, id):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    try:
        cursor.execute(f"SELECT * FROM services WHERE id = ?", (id,))
        records = cursor.fetchall()
        if id == 1:
            for row in records:
                await bot.send_message(message.chat.id, f'🔥 {row[3]}\n'
                                                        f'🆔 ID услуги: {row[4]}\n'
                                                        f'⬇ Количество: {row[5]}\n'
                                                        f'💸 Цена: {row[6]}р.\n'
                                                        f'Описание: {row[7]}\n',
                                       reply_markup=Markups.Youtube_buy_like111
                                       )
        elif id == 2:
            for row in records:
                await bot.send_message(message.chat.id, f'🔥 {row[3]}\n'
                                                        f'🆔 ID услуги: {row[4]}\n'
                                                        f'⬇ Количество: {row[5]}\n'
                                                        f'💸 Цена: {row[6]}р.\n'
                                                        f'Описание: {row[7]}\n',
                                       reply_markup=Markups.Youtube_buy_sub121
                                       )
        elif id == 3:
            for row in records:
                await bot.send_message(message.chat.id, f'🔥 {row[3]}\n'
                                                        f'🆔 ID услуги: {row[4]}\n'
                                                        f'⬇ Количество: {row[5]}\n'
                                                        f'💸 Цена: {row[6]}р.\n'
                                                        f'Описание: {row[7]}\n',
                                       reply_markup=Markups.Telegram_inline_221
                                       )
        elif id == 4:
            for row in records:
                await bot.send_message(message.chat.id, f'🔥 {row[3]}\n'
                                                        f'🆔 ID услуги: {row[4]}\n'
                                                        f'⬇ Количество: {row[5]}\n'
                                                        f'💸 Цена: {row[6]}р.\n'
                                                        f'Описание: {row[7]}\n',
                                       reply_markup=Markups.Telegram_inline_231
                                       )
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if connect:
            connect.close()


async def Start_order(callback: types.CallbackQuery, state: FSMContext, id) -> None:
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    cursor.execute(f"SELECT * FROM services WHERE id = ?", (id,))
    records = cursor.fetchall()
    user_money = User_money(callback.from_user.id)
    for row in records:
        if user_money >= row[6]:
            await callback.message.answer('Отправь свой телефон',
                                          reply_markup=Markups.Get_cancel_kb)
            async with state.proxy() as data:
                data['services_id'] = row[4]
                data['amount'] = row[5]
                data['money'] = row[6]
            await OrderStatesGroup.phone.set()
        else:
            await bot.send_message(callback.from_user.id,
                                   text='На балансе недостаточно средств. Пополните свой баланс и повторите попытку!')


async def handle_services_id(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['phone'] = message.text
    await message.reply('Отправь ссылку на сервис')
    await OrderStatesGroup.next()


async def handle_phone(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['link'] = message.text
    await new_create_orders(state, message)
    await bot.send_message(message.from_user.id, text='Ваш заказ успешно создан!',
                           reply_markup=Markups.MainMenu)
    user_money = User_money(message.from_user.id)
    Set_money(message.from_user.id, user_money - data['money'])
    await state.finish()

