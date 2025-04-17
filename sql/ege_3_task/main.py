from session import *
import pandas as pd
import datetime


def create_db():

    init_db()

    path = './table.xls'
    sheet_names = pd.ExcelFile(path).sheet_names

    for sheet_name in sheet_names:
        try:
            if sheet_name == 'Магазин':
                data_shops = pd.read_excel(path, sheet_name=sheet_name)
            
            elif sheet_name == 'Товар':
                data_goods = pd.read_excel(path, sheet_name=sheet_name)
            
            elif sheet_name == 'Движение товаров':
                data_operations = pd.read_excel(path, sheet_name=sheet_name)
                # list(data_operations.itertuples())[-1]
                # map(lambda x: True if x == 'Поступление' else False, list(data_operations.itertuples())[-1])
        
        except Exception as err:
            print(f'Error: {err}')
        
        finally:
            pass

    for _, shop_id, region, address in data_shops.itertuples():
        try:
            if not get_shop(shop_id):
                create_shop(shop_id, region, address)
        
        except Exception as err:
            print(f'Error: {err}')
        
        finally:
            pass

    for _, articul, group, name, measure, value, cost in data_goods.itertuples():
        try:
            if not get_good(articul):
                create_good(articul, group, name, measure, value, cost)

        except Exception as err:
            print(f'Error: {err}')
        
        finally:
            pass

    for _, operation_id, date, shop_id, articul, amount, operation_type in data_operations.itertuples():
        try:
            if not get_operation(operation_id):
                create_operation(operation_id, date, shop_id, articul, amount, operation_type)

        except Exception as err:
            print(f'Error: {err}')
        
        finally:
            pass


def get_turgenevskaya_shops(shop_list):
    necessary_ids = []

    for i in shop_list:
        if i.address.split()[0] == 'Тургеневская,':
            necessary_ids.append(i.shop_id)
    
    return necessary_ids


def get_necessary_date(operations):
    dates = []

    for operation in operations:
        if int(operation.date.split()[0].split('-')[-1]) in range(7, 23):
            dates.append(operation.date)
    
    return dates


def get_shampoos(goods):
        shampoos = []

        for good in goods:
            if good.name.split()[0] == 'Шампунь':
                shampoos.append(good.articul)
        
        return shampoos


def main():
    # create_db()

    shop_list = get_shop()
    operations = get_operation()
    goods = get_good()

    shop_ids = get_turgenevskaya_shops(shop_list)
    dates = get_necessary_date(operations)
    good_ids = get_shampoos(goods)

    result = 0

    for operation in operations:
        if operation.date in dates and\
            operation.shop_id in shop_ids and\
            operation.articul in good_ids and\
            operation.operation_type == 'Продажа':
                result += get_good(operation.articul).value * operation.pacs_amount
    
    result //= 1000
    print(result)


if __name__ == '__main__':
    main()
