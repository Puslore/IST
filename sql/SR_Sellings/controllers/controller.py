from database.session import *

# TODO
# доработать
# добавить функциюю оформления покупки, просмотра чеков

class ShopController:
    '''Class to connect GUI with DB'''
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect_to_db(self):
        '''Create connection with DB'''
        self.connection = get_connection(self.db_path)

        return self.connection is not None

    def get_good_by_name(self, name) -> dict:
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

    def get_goods_by_category(self, category_name):
        '''Get good list by category name'''
        if not self.connection:
            self.connect_to_db()

        products = get_goods_by_category(self.connection, category_name)
        return products

    def close_connection(self):
        '''Closing connection with DB'''
        if self.connection:
            self.connection.close()
