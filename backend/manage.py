#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import create_db
import django
from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.utils import OperationalError

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
    # 确保在运行其他命令之前先创建数据库
    django.setup()
    db_name = settings.DATABASES['default']['NAME']
    try:
        # 尝试连接数据库
        connections[DEFAULT_DB_ALIAS].ensure_connection()
        print(f"Database '{db_name}' already exists.")
    except OperationalError:
        # 数据库不存在，创建数据库
        new_database = create_db
        new_database.create_database(db_name)
        print(f"Database '{db_name}' created successfully.")

    # 原来管理程序
    try:
        from django.core.management import execute_from_command_line
        # # 在运行命令之前，先创建数据库
        # import create_db
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
