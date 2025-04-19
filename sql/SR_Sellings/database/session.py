import sqlite3
from database.models import *
from datetime import datetime #TODO


# Запрос для вставки категорий
insert_category_query = "INSERT INTO categories (name) VALUES (?)"

# Запрос для вставки товаров
insert_good_query = "INSERT INTO goods (name, category_id, price, amount) VALUES (?, ?, ?, ?)"

# Запрос для вставки чеков
# insert_receipt_query = "INSERT INTO receipts (date, total_amount) VALUES (?, ?)"

# Запрос для вставки операций
insert_receipt_query = "INSERT INTO receipts (product_id, amount, total_price) VALUES (?, ?, ?)"

# Запрос для обновления количества товара
update_quantity_query = "UPDATE goods SET amount = ? WHERE name = ?"

# current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Запрос для создания чека
query = "INSERT INTO receipts (product_id, amount, price, total_price) VALUES (?, ?, ?, ?)"



def get_connection(path: str):
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
        # cursor.execute(table_operations)
        
        print('---DB initialized correctly')
    
    except Exception as err:
        raise Exception(f'Error while creating tables - {err}')
    
    finally:
        if conn:
            conn.close()


def create_category(conn, data):
    '''Creating category'''
    try:
        cursor = conn.cursor()
        if type(data) is not list:
            cursor.execute(insert_category_query, data)
            
            print('---Category created corrcetly')
        
        else:
            cursor.executemany(insert_category_query, data)

            print('---Categories created corrcetly')

        conn.commit()

    except Exception as err:
        print(f'Error while creating new category - {err}')


def create_good(conn, data):
    '''Creating operation'''
    try:
        cursor = conn.cursor()
        if type(data) is not list:
            cursor.execute(insert_good_query, data)

            print('---Good created corrcetly')
        
        else:
            cursor.executemany(insert_good_query, data)

            print('---Goods created corrcetly')

        conn.commit()

    except Exception as err:
        print(f'Error while creating new good - {err}')


def create_receipt(conn, data):
    '''Creating receipt'''
    try:
        cursor = conn.cursor()
        if type(data[0]) == int:
            cursor.execute(insert_receipt_query, tuple(data))

            print('---Receipt created corrcetly')

        else:
            cursor.executemany(insert_receipt_query, list(map(tuple, data)))

            print('---Receipts created corrcetly')

        conn.commit()

    except Exception as err:
        print(f'Error while creating new receipt - {err}')


# def create_receipt(conn, data):
#     '''Creating receipt'''
#     try:
#         cursor = conn.cursor()
#         if type(data) is not list:
#             cursor.execute(insert_receipt_query, data)

#             print('---Receipt created corrcetly')

#         else:
#             cursor.executemany(insert_receipt_query, data)

#             print('---Receipts created corrcetly')

#         conn.commit()

#     except Exception as err:
#         print(f'Error while creating new receipt - {err}')


def get_goods_names_and_amount(conn) -> dict:
    '''Return list with names and amount of goods'''
    query = '''
    SELECT name, amount
    FROM goods
    ORDER BY category_id
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        data = dict(data)

        return data

    except Exception as err:
        print(f'Error while getting goods names and amount - {err}')
        return {}


def get_categories(conn) -> list:
    '''Return dict with categories' names'''
    query = '''
    SELECT name 
    FROM categories
    ORDER BY name
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        data = list(map(lambda cat: cat[0], data))

        return data

    except Exception as err:
        print(f'Error while getting categories - {err}')
        return []


def get_good_by_name(conn, good_name: str) -> dict:
    '''Return whole information of good by name'''
    query = '''
    SELECT g.id, g.name, c.name AS category_name, g.price, g.amount
    FROM goods g
    JOIN categories c ON g.category_id = c.id
    WHERE g.name = ?
    '''

    try:
        cursor = conn.cursor()
        cursor.execute(query, (good_name,))
        data = cursor.fetchone()
        print(data, 'flld,sfdsindashbvaiwuevfnwcywqvr3454678909976875645354566778')
        fields = [
            'id',
            'name',
            'category',
            'price',
            'amount'
        ]
        data = dict(zip(fields, data))
        print(data, 'datadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadatadata')

        return data

    except Exception as err:
        print(f'Error while getting good by name - {err}')
        return {}


def get_goods_by_category(conn, category) -> list:
    '''Return list of goods by category'''
    query = '''
    SELECT g.name
    FROM goods g
    JOIN categories c ON g.category_id = c.id
    WHERE c.name = ?
    ORDER BY g.name
    '''
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, (category,))
        data = cursor.fetchall()
        data = list(map(lambda gd: gd[0], data))
        
        return data
    
    except Exception as err:
        print(f"Error while getting goods by category - {err}")
        return []
    
def update_good_quantity(conn, good_name: str, new_quantity: int) -> bool:
    '''Update quantity of good'''
    try:
        cursor = conn.cursor()
        cursor.execute(update_quantity_query, (new_quantity, good_name))
        
        return True
    
    except Exception as err:
        print(f'ERROR WITH UPDATING GOOD QUANTITY --- {err}')
        return False
