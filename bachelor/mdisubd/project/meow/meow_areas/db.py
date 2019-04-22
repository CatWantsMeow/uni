import cx_Oracle
from meow_main.db import get_connection


def get_shopping_malls():
    connection = get_connection('default')
    cursor = connection.cursor()
    data = cursor.callfunc('get_shopping_malls', cx_Oracle.CURSOR, [])
    data = [list(obj[:5]) + get_location(obj[5]) for obj in data]
    print list(data)
    cursor.close()
    return list(data)


def get_shopping_mall(mall_id):
    connection = get_connection('default')
    cursor = connection.cursor()
    data = list(cursor.callfunc('get_shopping_mall', cx_Oracle.CURSOR, [mall_id]))
    if len(data) == 0:
        return None
    data = list(data[0][:5]) + get_location(data[0][5])
    cursor.close()
    return data


def get_shopping_areas(mall_id):
    connection = get_connection('default')
    cursor = connection.cursor()
    data = cursor.callfunc('get_shopping_areas', cx_Oracle.CURSOR, [mall_id])
    data = [list(obj[:4]) + [get_landlord(obj[4])] + [get_price(obj[5])] for obj in data]
    cursor.close()
    return list(data)


def get_location(location_id):
    connection = get_connection('default')
    cursor = connection.cursor()
    data = cursor.callfunc('get_location', cx_Oracle.CURSOR, [location_id])
    cursor.close()
    return list(data)


def get_locations():
    connection = get_connection('default')
    cursor = connection.cursor()
    data = cursor.callfunc('get_locations', cx_Oracle.CURSOR, [])
    cursor.close()
    return list(data)


def get_landlord(landlord_id):
    connection = get_connection('default')
    cursor = connection.cursor()
    data = cursor.callfunc('get_landlord', cx_Oracle.CURSOR, [landlord_id])
    cursor.close()
    return list(data)[0]


def get_price(price_id):
    connection = get_connection('default')
    cursor = connection.cursor()
    data = cursor.callfunc('get_price', cx_Oracle.CURSOR, [price_id])
    cursor.close()
    return list(data)[0]


def create_shopping_mall(group_name, mall_id, data):
    data = [
        mall_id,
        data.get('location_id'),
        data.get('name'),
        data.get('description'),
        data.get('floors_number'),
        data.get('parking_size'),
    ]
    connection = get_connection(group_name)
    cursor = connection.cursor()
    try:
        cursor.callfunc('meow.create_or_update_shopping_mall', cx_Oracle.NUMBER, data)
        cursor.close()
        connection.commit()
        return True
    except cx_Oracle.DatabaseError:
        return False


def delete_shopping_mall(group_name, mall_id):
    connection = get_connection(group_name)
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.callproc('meow.delete_shopping_mall', [mall_id])
        cursor.close()
        connection.commit()
        return True
    except cx_Oracle.DatabaseError:
        return False


def get_prices():
    connection = get_connection('default')
    cursor = connection.cursor()
    data = cursor.callfunc('get_prices', cx_Oracle.CURSOR, [])
    cursor.close()
    return list(data)


def get_shopping_area(area_id):
    connection = get_connection('default')
    cursor = connection.cursor()
    data = list(cursor.callfunc('get_shopping_area', cx_Oracle.CURSOR, [area_id]))
    if len(data) == 0:
        return None
    cursor.close()
    return list(data)[0]


def create_shopping_area(group_name, area_id, mall_id, data):
    data = [
        area_id,
        data.get('landlord_id'),
        mall_id,
        data.get('price_id'),
        data.get('area'),
        data.get('description'),
    ]
    connection = get_connection(group_name)
    cursor = connection.cursor()
    try:
        cursor.callfunc('meow.create_or_update_shopping_area', cx_Oracle.NUMBER, data)
        cursor.close()
        connection.commit()
        return True
    except cx_Oracle.DatabaseError as e:
        return False


def delete_shopping_area(group_name, area_id):
    connection = get_connection(group_name)
    if connection is None:
        return False

    cursor = connection.cursor()
    try:
        cursor.callproc('meow.delete_shopping_area', [area_id])
        cursor.close()
        connection.commit()
        return True
    except cx_Oracle.DatabaseError:
        return False
