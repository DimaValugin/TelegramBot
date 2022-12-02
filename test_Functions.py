import sqlite3
from Config import NAME_DB
from unittest import main, TestCase


class BD_login_id_Test(TestCase):
    def test_DB_login_id_positive1(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 329158519
        cursor.execute(f"SELECT first_name FROM login_id WHERE id = {telegram_id}")
        user_first_name = cursor.fetchone()
        user_first_name = user_first_name[0]
        print(user_first_name)
        self.assertEqual(user_first_name, "Aleksandr")

    def test_DB_login_id_positive2(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 329158519
        cursor.execute(f"SELECT last_name FROM login_id WHERE id = {telegram_id}")
        user_last_name = cursor.fetchone()
        user_last_name = user_last_name[0]
        print(user_last_name)
        self.assertEqual(user_last_name, "Posokhov")

    def test_DB_login_id_positive3(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 329158519
        cursor.execute(f"SELECT money FROM login_id WHERE id = {telegram_id}")
        user_money = cursor.fetchone()
        user_money = user_money[0]
        self.assertEqual(user_money, 0)

    def test_DB_login_id_negative1(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 329158519
        cursor.execute(f"SELECT first_name FROM login_id WHERE id = {telegram_id}")
        user_first_name = cursor.fetchone()
        user_first_name = user_first_name[0]
        print(user_first_name)
        self.assertNotEqual(user_first_name, "Дмитрий")

    def test_DB_login_id_negative2(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 329158519
        cursor.execute(f"SELECT last_name FROM login_id WHERE id = {telegram_id}")
        user_last_name = cursor.fetchone()
        user_last_name = user_last_name[0]
        print(user_last_name)
        self.assertNotEqual(user_last_name, "Валугин")

    def test_DB_login_id_negative3(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 329158519
        cursor.execute(f"SELECT money FROM login_id WHERE id = {telegram_id}")
        user_money = cursor.fetchone()
        user_money = user_money[0]
        print(user_money)
        self.assertNotEqual(user_money, 1000)


class BD_orders_Test(TestCase):
    def test_DB_orders_positive1(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT services_id FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, '311')

    def test_DB_orders_positive2(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT amount FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, '100')

    def test_DB_orders_positive3(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT phone FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, '89516754545')

    def test_DB_orders_positive4(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT link FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, 'https://vk.com/id338134482?z=photo338134482_457239876%2Falbum338134482_00%2Frev')

    def test_DB_orders_positive5(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT status FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, 'В процессе')

    def test_DB_orders_negative1(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT services_id FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, '112')

    def test_DB_orders_negative2(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT amount FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, '100000')

    def test_DB_orders_negative3(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT phone FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, '89517889532')

    def test_DB_orders_negative4(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT link FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, 'https://vk.com/id338134482')

    def test_DB_orders_negative5(self):
        connect = sqlite3.connect(NAME_DB)
        cursor = connect.cursor()
        connect.commit()

        telegram_id = 1683052818
        cursor.execute(f"SELECT status FROM orders WHERE user_id = {telegram_id}")
        user_services_id = cursor.fetchone()
        user_services_id = user_services_id[0]
        self.assertEqual(user_services_id, 'Завершен')


if __name__ == '__main__':
    main()
