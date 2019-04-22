import cx_Oracle
from django.conf import settings


def e(string):
    return string.encode('utf-8')


def get_connection(user_group):
    connection_pool = getattr(settings, 'CONNECTION_POOL', None)
    if not connection_pool:
        raise RuntimeError("Connection pool does not exist")
    connection = connection_pool.get(user_group, None)
    return connection


def has_privilege(user_token, privilege_name):
    connection = get_connection('default')
    cursor = connection.cursor()
    result = cursor.callfunc('can_execute', cx_Oracle.NUMBER, [user_token, privilege_name])
    print user_token, privilege_name, bool(result)
    cursor.close()
    return bool(result)