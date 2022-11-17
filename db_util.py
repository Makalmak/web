import math
import time

import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="web_shop",
            user="gabnasyrov",
            password="Makalmak",
            host="localhost",
        )
        self.cur = self.con.cursor()

    def addProd(self, name, price, describ, photo):
        try:
            binary = psycopg2.Binary(photo)
            tm = math.floor(time.time())
            self.cur.execute("INSERT INTO products(name, price, description, photo ,time) VALUES(%s, %s, %s, %s, %s)", (name, price, describ, binary ,tm))
            self.con.commit()

        except psycopg2.Error as e:
            print("Ошибка добавления товара в БД "+str(e))
            return False

        return True

    def getImg(self, postname):
        try:
            self.cur.execute(f"SELECT photo FROM products WHERE name = {postname} LIMIT 1")
            res = self.cur.fetchone()
            if res:
                return res[0]

        except psycopg2.Error as e:
            print("Ошибка получения товара из БД" + str(e))

        return (False, False)

    def getProdAnonce(self):
        try:
            self.cur.execute("SELECT id, name, price, description FROM products ORDER BY time DESC")
            res = self.cur.fetchall()
            if res:
                print(res)
                return res


        except psycopg2.Error as e:
            print("Ошибка получения товара из БД" + str(e))

        return []

    def addUser(self, name, email, login, hpsw):
        try:
            self.cur.execute(f"SELECT COUNT(*) as cnt FROM users WHERE email LIKE '{login}'")
            res = self.cur.fetchone()
            if res[0] > 0:
                print("Пользователь с таким login уже существует")
                return False


            self.cur.execute("INSERT INTO users(name, login, password, email, photo) VALUES(%s, %s, %s, %s, %s)", (name, login, hpsw, email))
            self.con.commit()

        except psycopg2.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res

        except psycopg2.Error as e:
            print("Ошибка"+ str(e))

        return False

    def getUserByLogin(self, login):
        try:
            self.cur.execute(f"SELECT * FROM users WHERE login = '{login}' LIMIT 1")
            res = self.cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res

        except psycopg2.Error as e:
            print("Ошибка получения данных из БД"+ str(e))

        return False

