try:
	import MySQLdb
except:
	import pymysql as MySQLdb
import os
import psycopg2
import pymssql
import sqlite3

# 不好意思，DB_CONNECTIONS has to be reinitialized, hence defined in user.py

TERMINAL_TOKENS = {
	'psql': ["'", '$$'],
	'mssql': ["'"]
}
