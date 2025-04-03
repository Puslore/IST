import sqlite3 as sq
from os.path import exists
import pandas as pd
from contextlib import contextmanager


def main():
    check = check_db_exist()
    create_db(skip_creating=check)
    shop_ids = get_turgenevskaya_shops()
    dates = get_necessary_date()
    good_ids = get_shampoos()
    result = calculate_result(shop_ids, dates, good_ids)
    print(result)


@contextmanager
def get_db():
    connection = sq.connect('./database.db')
    cursor = connection.cursor()
    try:
        yield cursor
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()


def check_db_exist() -> bool:
    db_path = './database.db'
    try:
        with open(db_path, 'w') as file:
            return False
    except FileExistsError:
        return True


def read_excel_file(path: str) -> list:
    sheet_names = pd.ExcelFile(path).sheet_names
    data_shops = None
    data_goods = None
    data_operations = None

    for sheet_name in sheet_names:
        try:
            if sheet_name == 'Магазин':
                data_shops = pd.read_excel(path, sheet_name=sheet_name)
            
            elif sheet_name == 'Товар':
                data_goods = pd.read_excel(path, sheet_name=sheet_name)
            
            elif sheet_name == 'Движение товаров':
                data_operations = pd.read_excel(path, sheet_name=sheet_name)
     
        except Exception as err:
            print(f'Error: {err}')
    
    if data_shops is None or data_goods is None or data_operations is None:
        raise ValueError("Не все необходимые листы найдены в Excel-файле")
    
    return [data_shops, data_goods, data_operations]


def create_db(skip_creating: bool = False):
    data = read_excel_file('./table.xls')
    
    if not skip_creating:
        with get_db() as cursor:
            try:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS shops (
                    shop_id TEXT PRIMARY KEY NOT NULL UNIQUE,
                    region TEXT NOT NULL,
                    address TEXT NOT NULL
                )
                ''')

                for _, shop_id, region, address in data[0].itertuples():
                    cursor.execute('INSERT OR IGNORE INTO shops (shop_id, region, address) VALUES (?, ?, ?)', 
                                  [shop_id, region, address])
     
            except Exception as err:
                raise Exception(f'Error with shops: {err}')

            try:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS goods (
                    articul INTEGER PRIMARY KEY,
                    "group" TEXT NOT NULL,
                    name TEXT NOT NULL,
                    measure TEXT NOT NULL,
                    value INTEGER NOT NULL,
                    cost INTEGER NOT NULL
                )
                ''')

                for _, articul, group, name, measure, value, cost in data[1].itertuples():
                    cursor.execute('INSERT OR IGNORE INTO goods (articul, "group", name, measure, value, cost) VALUES (?, ?, ?, ?, ?, ?)', 
                                  [articul, group, name, measure, value, cost])

            except Exception as err:
                raise Exception(f'Error with goods: {err}')

            try:
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS operations (
                    operation_id INTEGER PRIMARY KEY,
                    date TEXT NOT NULL,
                    shop_id TEXT NOT NULL,
                    articul INTEGER NOT NULL,
                    pacs_amount INTEGER NOT NULL,
                    operation_type TEXT NOT NULL,
                    FOREIGN KEY (shop_id) REFERENCES shops (shop_id),
                    FOREIGN KEY (articul) REFERENCES goods (articul)
                )
                ''')

                for _, operation_id, date, shop_id, articul, amount, operation_type in data[2].itertuples():
                    date = str(date).split()[0]
                    cursor.execute('INSERT OR IGNORE INTO operations (operation_id, date, shop_id, articul, pacs_amount, operation_type) VALUES (?, ?, ?, ?, ?, ?)', 
                                  [operation_id, date, shop_id, articul, amount, operation_type])

            except Exception as err:
                raise Exception(f'Error with operations: {err}')


def get_turgenevskaya_shops() -> list:
    with get_db() as cursor:
        try:
            cursor.execute('''
            SELECT shop_id
            FROM shops
            WHERE address LIKE 'Тургеневская%'
            ''')
            return [row[0] for row in cursor.fetchall()]
        except Exception as err:
            raise Exception(f'Error with getting Turgenevskaya shops: {err}')


def get_necessary_date() -> list:
    with get_db() as cursor:
        try:
            cursor.execute('''
            SELECT DISTINCT date
            FROM operations
            WHERE date LIKE '%-09-%' AND 
                  CAST(substr(date, 9, 2) AS INTEGER) BETWEEN 7 AND 22
            ''')
            return [row[0] for row in cursor.fetchall()]
        except Exception as err:
            raise Exception(f'Error with getting necessary dates: {err}')


def get_shampoos() -> list:
    with get_db() as cursor:
        try:
            cursor.execute('''
            SELECT articul
            FROM goods
            WHERE name LIKE 'Шампунь%'
            ''')
            return [row[0] for row in cursor.fetchall()]
        except Exception as err:
            raise Exception(f'Error with getting shampoos: {err}')


def calculate_result(shop_ids, dates, good_ids) -> int:
    with get_db() as cursor:
        try:
            shop_ids_str = ', '.join(f"'{shop_id}'" for shop_id in shop_ids)
            dates_str = ', '.join(f"'{date}'" for date in dates)
            good_ids_str = ', '.join(str(good_id) for good_id in good_ids)
            
            cursor.execute(f'''
            SELECT SUM(g.value * o.pacs_amount)
            FROM operations o
            JOIN goods g ON o.articul = g.articul
            WHERE o.shop_id IN ({shop_ids_str})
            AND o.date IN ({dates_str})
            AND o.articul IN ({good_ids_str})
            AND o.operation_type = 'Продажа'
            ''')
            
            total = cursor.fetchone()[0] or 0
            return total // 1000
            
        except Exception as err:
            raise Exception(f'Error with calculating result: {err}')


if __name__ == "__main__":
    main()
