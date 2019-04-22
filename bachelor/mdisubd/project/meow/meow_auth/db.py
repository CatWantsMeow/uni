import cx_Oracle
from base64 import b64encode
from time import time

from meow_main.db import get_connection


def generate_token(username, password):
    return b64encode("{}:{}:{}".format(username, password, time()))


def login(username, password):
    connection = get_connection('default')
    cursor = connection.cursor()
    token = generate_token(username, password)
    user_id = cursor.callfunc('login', cx_Oracle.NUMBER, [username, password, token])
    cursor.close()
    return user_id, token


def logout(token):
    connection = get_connection('default')
    cursor = connection.cursor()
    cursor.callproc('logout', [token])
    cursor.close()


def register_landlord(data):
    fields = [
        None,
        None,
        data.get('username', None),
        data.get('password', None),
        data.get('first_name', None),
        data.get('middle_name', None),
        data.get('last_name', None),
        data.get('email', None),
        data.get('phone', None),
        data.get('organization_name', None),
        data.get('description', None),
    ]

    connection = get_connection('default')
    cursor = connection.cursor()
    try:
        cursor.callfunc('create_or_update_landlord', cx_Oracle.NUMBER, fields)
        cursor.close()
        return True
    except cx_Oracle.DatabaseError as e:
        return False
    finally:
        connection.commit()


def register_tenant(data):
    fields = [
        None,
        None,
        data.get('username', None),
        data.get('password', None),
        data.get('first_name', None),
        data.get('middle_name', None),
        data.get('last_name', None),
        data.get('email', None),
        data.get('phone', None),
        data.get('requisites', None),
    ]

    connection = get_connection('default')
    cursor = connection.cursor()
    try:
        cursor.callfunc('create_or_update_tenant', cx_Oracle.NUMBER, fields)
        cursor.close()
        return True
    except cx_Oracle.DatabaseError as e:
        return False
    finally:
        connection.commit()


def get_landlords():
    connection = get_connection('default')
    cursor = connection.cursor()
    data = cursor.callfunc('get_landlords', cx_Oracle.CURSOR, [])
    cursor.close()
    return list(data)


def get_tenant_id(token):
    connection = get_connection('default')
    cursor = connection.cursor()
    id = cursor.callfunc('get_tenant_id', cx_Oracle.NUMBER, [token])
    cursor.close()
    return id


def get_landlord_id(token):
    connection = get_connection('default')
    cursor = connection.cursor()
    id = cursor.callfunc('get_landlord_id', cx_Oracle.NUMBER, [token])
    cursor.close()
    return id