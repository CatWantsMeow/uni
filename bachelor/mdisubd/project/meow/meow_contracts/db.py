import cx_Oracle

from meow_main.db import get_connection


def create_rent_request(tenant_id, area_id, description=''):
    connection = get_connection('tenants')
    cursor = connection.cursor()
    try:
        cursor.callproc('meow.create_rent_request', [tenant_id, area_id, description])
        cursor.close()
        connection.commit()
        return True
    except cx_Oracle.DatabaseError:
        return False


def create_rent_contract(rent_contract_id, area_id, tenant_id, landlord_id, form_data):
    data = [
        rent_contract_id,
        tenant_id,
        landlord_id,
        area_id,
        form_data.get('code'),
        form_data.get('start_date'),
        form_data.get('end_date'),
        form_data.get('price'),
        form_data.get('additional_payment'),
        form_data.get('discount'),
        form_data.get('checking_account'),
        form_data.get('requirements'),
    ]
    connection = get_connection('landlords')
    cursor = connection.cursor()
    try:
        cursor.callfunc('meow.create_or_update_contract', cx_Oracle.NUMBER, data)
        cursor.close()
        connection.commit()
        return True
    except cx_Oracle.DatabaseError as e:
        print e
        return False


def get_tenant_rent_requests(tenant_id):
    connection = get_connection('tenants')
    cursor = connection.cursor()
    data = list(cursor.callfunc('meow.get_rent_requests', cx_Oracle.CURSOR, [tenant_id]))
    cursor.close()
    return data


def get_tenant_rent_contracts(tenant_id):
    connection = get_connection('tenants')
    cursor = connection.cursor()
    data = list(cursor.callfunc('meow.get_tenant_rent_contracts', cx_Oracle.CURSOR, [tenant_id]))
    cursor.close()
    return data


def get_rent_contract(landlord_id, contract_id):
    connection = get_connection('landlords')
    cursor = connection.cursor()
    data = list(cursor.callfunc('meow.get_rent_contract', cx_Oracle.CURSOR, [landlord_id, contract_id]))
    cursor.close()
    if len(data) == 0:
        return None
    else:
        return data[0]


def get_landlord_rent_requests(landlord_id):
    connection = get_connection('landlords')
    cursor = connection.cursor()
    data = list(cursor.callfunc('meow.get_landlord_rent_requests', cx_Oracle.CURSOR, [landlord_id]))
    cursor.close()
    return data


def get_landlord_rent_contracts(landlord_id):
    connection = get_connection('landlords')
    cursor = connection.cursor()
    data = list(cursor.callfunc('meow.get_landlord_rent_contracts', cx_Oracle.CURSOR, [landlord_id]))
    cursor.close()
    return data


def delete_rent_contract(landlord_id, contract_id):
    connection = get_connection('landlords')
    cursor = connection.cursor()
    result = cursor.callfunc('meow.delete_rent_contract', cx_Oracle.NUMBER, [landlord_id, contract_id])
    cursor.close()
    return result


def delete_rent_request(tenant_id, area_id):
    connection = get_connection('landlords')
    cursor = connection.cursor()
    result = cursor.callfunc('meow.delete_rent_request', cx_Oracle.NUMBER, [tenant_id, area_id])
    cursor.close()
    return result


def is_active_rent_contract(contract_id):
    connection = get_connection('landlords')
    cursor = connection.cursor()
    result = cursor.callfunc('meow.is_active_rent_contract', cx_Oracle.BOOLEAN, [contract_id])
    cursor.close()
    return result


def start_rent(landlord_id, contract_id):
    connection = get_connection('landlords')
    cursor = connection.cursor()
    result = cursor.callfunc('meow.start_rent', cx_Oracle.NUMBER, [landlord_id, contract_id])
    cursor.close()
    return result


def end_rent(landlord_id, contract_id):
    connection = get_connection('landlords')
    cursor = connection.cursor()
    result = cursor.callfunc('meow.end_rent', cx_Oracle.NUMBER, [landlord_id, contract_id])
    cursor.close()
    return result

