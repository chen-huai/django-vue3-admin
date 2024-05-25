import sys
import django
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.utils import OperationalError

def create_database(database_name):
    # 获取数据库配置
    db_settings = settings.DATABASES['default']
    db_name = db_settings['NAME']
    db_user = db_settings['USER']
    db_password = db_settings['PASSWORD']
    db_host = db_settings['HOST']
    db_port = db_settings['PORT']

    # 创建连接字符串
    if 'postgresql' in db_settings['ENGINE']:
        import psycopg2
        conn = psycopg2.connect(dbname='postgres', user=db_user, password=db_password, host=db_host, port=db_port)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {database_name}")
        conn.close()
    elif 'mysql' in db_settings['ENGINE']:
        import pymysql
        conn = pymysql.connect(user=db_user, password=db_password, host=db_host, port=int(db_port))
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        conn.close()
    elif 'sqlite3' in db_settings['ENGINE']:
        # SQLite 在连接时会自动创建数据库文件
        pass
    elif 'oracle' in db_settings['ENGINE']:
        import cx_Oracle
        dsn = cx_Oracle.makedsn(db_host, db_port, sid=database_name)
        conn = cx_Oracle.connect(user=db_user, password=db_password, dsn=dsn)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM all_users WHERE username = '{db_user.upper()}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE USER {db_user} IDENTIFIED BY {db_password}")
            cursor.execute(f"GRANT ALL PRIVILEGES TO {db_user}")
        conn.close()
    elif 'sql_server' in db_settings['ENGINE']:
        import pyodbc
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={db_host},{db_port};UID={db_user};PWD={db_password}"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"IF NOT EXISTS (SELECT name FROM master.dbo.sysdatabases WHERE name = N'{database_name}') CREATE DATABASE [{database_name}]")
        conn.close()
    else:
        raise ValueError("This script only supports PostgreSQL, MySQL, SQLite, Oracle, and SQL Server.")

if __name__ == "__main__":
    django.setup()
    db_name = settings.DATABASES['default']['NAME']
    try:
        # 尝试连接数据库
        connections[DEFAULT_DB_ALIAS].ensure_connection()
        print(f"Database '{db_name}' already exists.")
    except OperationalError:
        # 数据库不存在，创建数据库
        create_database(db_name)
        print(f"Database '{db_name}' created successfully.")
