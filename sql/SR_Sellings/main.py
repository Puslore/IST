import os
from csv_operations import import_from_csv
from database.session import *


def gui():
    '''creates GUI'''
    ...


def create_db(path: str, need_csv_filling: bool=False):
    check = check_db_exist(path)
    if not check and need_csv_filling:
        try:
            init_db(path)
            conn = get_connection(path)

            cvs_paths = [
                './csvs/categories.csv',
                './csvs/goods.csv'
            ]
            data = import_from_csv(cvs_paths)
            categories_data, goods_data = data.values()

            for category in categories_data:
                create_category(conn, category)
            for good in goods_data:
                create_good(conn, good)

        except Exception as err:
            print(f'Error with DB creating - {err}')
            os.remove(path)

        finally:
            if conn:
                conn.close()


def check_db_exist(path: str) -> bool:
    '''Checking DB existence'''    
    if os.path.exists(path):
        return True

    with open(path, mode='w'):
        pass
    return False


def main():
    '''Main function'''
    path = './database/database.db'
    create_db(path, need_csv_filling=False)
    gui()


if __name__ == "__main__":
    main()
