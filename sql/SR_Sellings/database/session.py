import sqlite3
from database.models import *
from datetime import datetime


# Запрос для вставки категорий
insert_category_query = "INSERT INTO categories (name) VALUES (?)"

# Запрос для вставки товаров
insert_good_query = "INSERT INTO goods (name, category_id, price, amount) VALUES (?, ?, ?, ?)"

# Запрос для вставки чеков
insert_receipt_query = "INSERT INTO receipts (date, total_amount) VALUES (?, ?)"

# Запрос для вставки операций
insert_operation_query = "INSERT INTO operations (receipt_id, product_id, amount, price, total_price) VALUES (?, ?, ?, ?, ?)"



def get_connection(path: str = './database.db'):
    '''Return connection with DB'''
    conn = sqlite3.connect(path) 
    
    return conn


# Используется одноразово
def init_db(path: str):
    '''DB initialization'''
    try:
        conn = get_connection(path)
        cursor = conn.cursor()
        
        cursor.execute(table_categories)
        cursor.execute(table_goods)
        cursor.execute(table_receipts)
        cursor.execute(table_operations)
    
    except Exception as err:
        raise Exception(f'Error while creating tables - {err}')
    
    finally:
        if conn:
            conn.close()


def create_category(conn, data): # TODO доделать. conn создается во время сессии один раз, и передается постоянно.
    '''Creating category'''
    try:
        cursor = conn.cursor()
        if type(data) is not list:
            cursor.execute(insert_category_query, data)
        
        else:
            cursor.executemany(insert_category_query, data)
    
    except Exception as err:
        print(f'Error while creating new category - {err}')


def create_good(conn, data): # TODO доделать. conn создается во время сессии один раз, и передается постоянно.
    '''Creating operation'''
    try:
        cursor = conn.cursor()
        if type(data) is not list:
            cursor.execute(insert_good_query, data)
        
        else:
            cursor.executemany(insert_good_query, data)
    
    except Exception as err:
        print(f'Error while creating new good - {err}')


def create_operation(conn, data): # TODO доделать. conn создается во время сессии один раз, и передается постоянно.
    '''Creating operation'''
    try:
        cursor = conn.cursor()
        if type(data) is not list:
            cursor.execute(insert_operation_query, data)
        
        else:
            cursor.executemany(insert_operation_query, data)
    
    except Exception as err:
        print(f'Error while creating new operation - {err}')
    
    finally:
        if conn:
            conn.close()

def create_receipt(conn, data): # TODO доделать. conn создается во время сессии один раз, и передается постоянно.
    '''Creating receipt'''
    try:
        cursor = conn.cursor()
        if type(data) is not list:
            cursor.execute(insert_receipt_query, data)
        
        else:
            cursor.executemany(insert_receipt_query, data)
    
    except Exception as err:
        print(f'Error while creating new receipt - {err}')
