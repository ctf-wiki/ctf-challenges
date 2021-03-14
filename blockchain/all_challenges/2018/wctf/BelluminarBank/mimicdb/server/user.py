# ~*~ coding: utf-8 ~*~
from config import *

from collections import Counter
from random import choice

try:
    from flask.ext.login import UserMixin
except:
    from flask_login import UserMixin

class UserNotFoundError(Exception):
    pass

class User(UserMixin):

    id = None
    password = None

    def is_active(self):
        return True

    def query(self, query, driver):
        try:
            conn = self.DB_CONNECTIONS[driver]
            c = conn.cursor()
            c.execute(query)
            r = tuple(c.fetchall())
            return r
        except Exception, e:
            return ()

    def find_user(self, username, driver):
        quote = choice(TERMINAL_TOKENS.get(driver, ["'", '"']))
        # 我知道这不太好
        query = '''select * from users where username=%s%s%s;''' % (quote, username, quote)
        return self.query(query, driver)

    def __init__(self, username):
        self.DB_CONNECTIONS = {
              'mssql': pymssql.connect('127.0.0.1', 'belluminar', 'this-wctf2018-pwd', 'belluminar'),
              'mysql': MySQLdb.connect(host='localhost', user='belluminar', passwd='', db='belluminar'),
              'psql': psycopg2.connect("dbname='belluminar' user='belluminar' host='localhost' password='this-wctf2018-pwd'"),
              'sqlite': sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '/../belluminar.sqlite3'),
        }
        result = [self.find_user(username, driver) for driver in self.DB_CONNECTIONS]
        common = Counter(result).most_common()[0]
        user = () if common[1] < len(result) - 1 else common[0]
        if not user:
            raise UserNotFoundError()
        self._id = user[0][0]
        self.username = user[0][1]
        self.id = self.username # 我们需要用这个
        self.password = user[0][2]

    @classmethod
    def get(self_class, username):
        try:
            return self_class(username)
        except UserNotFoundError:
            return None
