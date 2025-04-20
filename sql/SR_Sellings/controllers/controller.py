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

    def process_purchase(self, name: str, quantity: int) -> str:
        try:
            print(name, 'dsmklfsaklfkldsfmkldsfmkldsfmkdsmflkdsmflkdsmfld')
            good = self.get_good_by_name(name)
            price = good['price']
            total_price = quantity * price
            date = datetime.now().strftime("%Y-%m-%d")

            success = self.create_receipt(name, quantity, total_price, date)
            print(success, 'отладка success -=-=-=-=-=-=-=-=-=-')
            if success:
                return f'Успешно! Куплено: {name}, в количестве {quantity} шт. суммарной стоимостью {total_price}\nДата: {date}'
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

    def create_receipt(self, product_name: str, quantity: int, total_price: float, date: str) -> bool:
        try:
            good_info = get_good_by_name(self.connection, product_name)
            receipt_data = [good_info['id'], quantity, total_price, date]
            create_receipt(self.connection, receipt_data)
            return True
        
        except Exception as err:
            print(f'ERROR WITH CREATING RECEIPT --- {err}')
            return False

    def get_receipts_by_date(self, date_str):
        try:

            receipts_data = get_receipts_by_date(self.connection, date_str)
            receipts = []
            for row in receipts_data:
                product_name = get_good_name_by_id(self.connection, row[1])
                receipt = {
                    'id': row[0],
                    'product_name': product_name,
                    'quantity': row[2],
                    'total_price': round(row[3], 2),
                    'date': row[4]
                }
                receipts.append(receipt)

            return receipts

        except Exception as e:
            print(f"Ошибка при получении чеков по дате: {e}")
            return []

    def close_connection(self):
        '''Closing connection with DB'''
        if self.connection:
            self.connection.close()
