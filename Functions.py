import sqlite3
import telebot
import Markups
from Config import TOKEN, NAME_DB
from aiogram import types
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

bot = telebot.TeleBot(TOKEN)


def start(message):
    scan_id(message)
    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!'.format(message.from_user),
                     reply_markup=Markups.MainMenu)


def support_client(message):
    bot.send_message(message.chat.id, '⚙Если возникли проблемы при работе с ботом,\n'
                                      ' можете обратиться в службу поддержки.\n\n'
                                      'Контактная информация:\n'
                                      'Телефон: +7 643 267 4568\n'
                                      'E-mail: testtest@mail.ru\n')


def nakrutka(message):
    bot.send_message(message.chat.id, '📈 Выберите сервис для накрутки',
                     reply_markup=Markups.SN_inline
                     )


def scan_id(message):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    connect.commit()
    user_money = 0
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        user_data = [message.chat.id, message.from_user.first_name, message.from_user.last_name, user_money]

        cursor.execute("INSERT INTO login_id VALUES(?,?,?,?);", user_data)
    bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}!'.format(message.from_user),
                     reply_markup=Markups.MainMenu)
    connect.commit()
    connect.close()


def set_money(money):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    connect.commit()
    return cursor.execute("UPDATE login_id SET money = ?", (money,))


def my_profile(message):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    connect.commit()
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    user_id = cursor.fetchone()
    user_id = user_id[0]
    people_first_name = message.chat.id
    cursor.execute(f"SELECT first_name FROM login_id WHERE id = {people_first_name}")
    user_first_name = cursor.fetchone()
    user_first_name = user_first_name[0]
    people_last_name = message.chat.id
    cursor.execute(f"SELECT last_name FROM login_id WHERE id = {people_last_name}")
    user_last_name = cursor.fetchone()
    user_last_name = user_last_name[0]
    people_money = message.chat.id
    cursor.execute(f"SELECT money FROM login_id WHERE id = {people_money}")
    people_money = cursor.fetchone()
    people_money = people_money[0]
    bot.send_message(message.chat.id, '👤 Мой профиль\n\n'
                                      f'ID: {user_id}\n'
                                      f'Имя: {user_first_name}\n'
                                      f'Фамилия: {user_last_name}\n'
                                      f'Баланс: {people_money}\n',
                     reply_markup=Markups.MainMenu
                     )
    connect.commit()


def create_orders(services_id, amount, phone, link):
    connect = sqlite3.connect(NAME_DB)
    cursor = connect.cursor()
    cursor.execute('INSERT INTO orders (services_id, amount, phone, link) VALUES(?, ?, ?, ?)', (services_id, amount,
                                                                                                phone, link))
    connect.commit()


# async def refill(message: types.Message):
#     if message.chat.type == 'private':
#         if is_number(message.text):
#             message_money = int(message.text)
#             if message_money >= 5:
#                 pass
#             else:
#                 await bot.send_message(message.from_user.id, "Минимальная сумма для пополнения 5 руб.")
#         else:
#             await bot.send_message(message.from_user.id, "Введите число")


# def is_number(_str):
#     try:
#         int(_str)
#         return True
#     except ValueError:
#         return False
