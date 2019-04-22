import os

os.environ['NLS_LANG'] = 'American_America.AL32UTF8'

import cx_Oracle


try:
    dsn = cx_Oracle.makedsn('meow', 1521, 'oracle')
    CONNECTION_POOL = {
        'default': cx_Oracle.connect('meow', 'nothingissomething', dsn),
        'admins': cx_Oracle.connect('ADMINS', 'ADMINS', dsn),
        'tenants': cx_Oracle.connect('TENANTS', 'TENANTS', dsn),
        'landlords': cx_Oracle.connect('LANDLORDS', 'LANDLORDS', dsn)
    }
except cx_Oracle.DatabaseError as e:
    print e.message
    exit(1)
