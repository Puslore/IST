import re
from database.session import *

# TODO
# доработать
# добавить функцию оформления покупки, просмотра чеков
# АААА Я ЩАС УСТАНУ И ЛЯГУ СПАТЬ ПОМОГИТЕ

class ShopController:
    '''Class to connect GUI with DB'''
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect_to_db(self):
        '''Create connection with DB'''
        self.connection = get_connection(self.db_path)

        return self.connection is not None

    def get_good_by_name(self, name: str) -> dict:
        '''Get good info by name'''
        if not self.connection:
            self.connect_to_db()

        good = get_good_by_name(self.connection, name)

        return good

    def get_all_categories(self) -> list:
        '''Get all categories'''
        if not self.connection:
            self.connect_to_db()

        categories = get_categories(self.connection)

        return categories

    def get_goods_by_category(self, category_name: str) -> list:
        '''Get good list by category name'''
        if not self.connection:
            self.connect_to_db()

        products = get_goods_by_category(self.connection, category_name)
        return products

    def get_good_info(self, name: str) -> dict:
        good_data = get_good_by_name(self.connection, name)
        keys = ['name', 'price', 'amount']
        good_info = {k: good_data[k] for k in keys}

        return good_info

    def process_purchase(self, string_: str, quantity: int) -> str:
        try:
            name = string_.split(',')[0]
            print(name, 'dsmklfsaklfkldsfmkldsfmkldsfmkdsmflkdsmflkdsmfld')
            good = self.get_good_by_name(name)
            price = int(string_.split(':')[-1].split()[0])

            success = self.create_receipt(good['name'], quantity, price)
            print(success, 'отладка success -=-=-=-=-=-=-=-=-=-')
            if success:
                return f'Успешно! Куплено: {name}, в количестве {quantity} шт. суммарной стоимостью {price}'
            else:
                raise Exception('Error with process_purchase')

        except Exception as err:
            print(f'ERROR WITH PURCHASE PROCESS --- {err}')
            return 'Ошибка------------------'


    def update_product_quantity(self, product_name: str, new_quantity: int) -> bool:
        try:
            success = update_good_quantity(self.connection, product_name, new_quantity)
            if success:
                return True
            else:
                raise Exception('yes, unknown error')
        
        except Exception as err:
            print(f'ERROR UPDATING QUANTITY(controller) --- {err}')
            return False


    def create_receipt(self, product_name: str, quantity: int, total_price: float) -> bool:
        try:
            good_info = get_good_by_name(self.connection, product_name)
            receipt_data = [good_info['id'], quantity, total_price]
            create_receipt(self.connection, receipt_data)
            return True
        
        except Exception as err:
            print(f'ERROR WITH CREATING RECEIPT --- {err}')
            return False


    def close_connection(self):
        '''Closing connection with DB'''
        if self.connection:
            self.connection.close()
