import sqlite3
from models import *
from datetime import datetime


# Запрос для вставки категорий
insert_category_query = "INSERT INTO categories (name) VALUES (?)"

# Запрос для вставки товаров
insert_good_query = "INSERT INTO goods (name, category_id, price, amount) VALUES (?, ?, ?, ?)"

# Запрос для вставки чеков
insert_receipt_query = "INSERT INTO receipts (date, total_amount) VALUES (?, ?)"

# Запрос для вставки операций
insert_operation_query = "INSERT INTO operations (receipt_id, product_id, amount, price, total_price) VALUES (?, ?, ?, ?, ?)"



def get_connection(path: str):
    '''Return connection with DB'''
    conn = sqlite3.connect(path) 
    
    return conn


def init_db(path: str):
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


def create_operation():
    ...

def create_recipe():
    ...


