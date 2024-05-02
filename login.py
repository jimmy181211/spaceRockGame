import MySQLdb
from mainPage import MainPage
from util import lower_case
import re
import sys


class MainProgram:
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "1881415157Jimmy", "spaceRock", charset="utf8")
        self.table = "userinfo"
        self.cursor = self.db.cursor()
        self.cursor.execute(f"select* from {self.table}")
        self.data = self.cursor.fetchall()
        self.is_user = False
        print("enter 'quit' when you want to leave the game!")

    def call(self):
        is_valid=False
        while not is_valid:
            is_valid=True
            option = input("enter:1.register 2.login")
            if lower_case(option)=="quit":
                break
            if option == "1" or lower_case(option) == "register":
                self._register()
            elif option == "2" or lower_case(option) == "login":
                self._login()
            else:
                is_valid=False
                print("invalid input, please try again")

        self.db.close()

    @staticmethod
    def _input_format(field_name: str, check_func, invalid_desc="the {} is invalid"):
        while True:
            data = input(f"enter your {field_name}:")
            if data == "quit":
                print("see you next time!")
                sys.exit(0)
            # if the data passes the test
            if check_func(data):
                break
            else:
                print(invalid_desc.format(field_name))
        return data

    @staticmethod
    def _is_pwd_valid(pwd):
        return 0 < len(pwd) <= 20

    @staticmethod
    def _is_email_valid(email):
        email_format = re.compile(r"[^@]+@[^@]+\.[^@]+")
        return True if email_format.match(email) else False

    def _insert_items(self, sql_str, purpose: str, unsuccessful_desc: str = ""):
        try:
            # store the data into the database
            self.cursor.execute(sql_str)
            self.db.commit()
            print(f"{purpose} successful!")
        except Exception:
            print(unsuccessful_desc)
            print(f"{purpose} unsuccessful!")
            self.db.rollback()

    def _register(self):
        name = input("enter your name:")
        pwd = self._input_format("password", self._is_pwd_valid, "{} length must be: 0-20")
        email = self._input_format("email", self._is_email_valid)
        # upload the details into the table
        sql_str = "insert into {} values('{}','{}','{}',0,'L1',0,'L1')".format(self.table, name, pwd, email)
        self._insert_items(sql_str, "register", "account already exists or repeated username/password/email address")

        print("now let's login!")
        self.cursor.execute(f"select* from {self.table}")
        self.data = self.cursor.fetchall()
        self._login()

    def _login(self):
        while not self.is_user:
            # enter user info and obtain data from the database, initialising the game
            username = input("enter username:")
            pwd = input("enter password:")
            if username == "quit" or pwd == "quit":
                print("see you next time")
                break

            for info in self.data:
                if info[0] == username and info[1] == pwd:
                    self._game_logic(info)
                    self.is_user = True

            if not self.is_user:
                print("details entered are not correct, please try again!")

    def _game_logic(self, info):
        main_page = MainPage(info)
        main_page.main_loop()
        # update the user fortune
        fortune = main_page.user_fortune
        print(fortune)
        sql_str = f"insert into {self.table} (cointotal,bullettype,shieldnum,shieldtype) values({fortune['coin_num']},{fortune['bullet_type']},{fortune['shield_num']},{fortune['shield_type']})"
        self._insert_items(sql_str, "detail update")
