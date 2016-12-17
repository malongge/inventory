

from django.core.management.base import BaseCommand
import sqlite3


class Command(BaseCommand):
    help = '数据库里的数据，同步到另一个数据库'

    def handle(self, *args, **options):
        user_info = 'password, is_superuser, first_name, email, last_name, date_joined, last_login, is_staff, is_active, username'
        cx = sqlite3.connect(r"D:\inventory\store-old.db")
        cu = cx.cursor()
        cu.execute("SELECT {} FROM auth_user".format(user_info))
        rows = cu.fetchall()
        _cx = sqlite3.connect(r"D:\inventory\store.db")
        _cu = _cx.cursor()
        for r in rows:
            m = ','.join(['?' for _ in range(len(r))])
            _cu.execute("insert into auth_user({}) values ({})".format(user_info, m), r)
        _cx.commit()
        # print(r.keys())