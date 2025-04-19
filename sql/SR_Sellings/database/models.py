table_categories = '''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
)
'''

table_goods = '''
CREATE TABLE IF NOT EXISTS goods (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    category_id INTEGER NOT NULL,
    price FLOAT NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
'''

# table_receipts = '''
# CREATE TABLE IF NOT EXISTS receipts (
#     id INTEGER PRIMARY KEY,
#     date TEXT NOT NULL,
#     total_amount FLOAT NOT NULL
# )
# '''

# receipt_id INTEGER NOT NULL,
# price FLOAT NOT NULL,
# FOREIGN KEY (receipt_id) REFERENCES receipts(id),
table_receipts = '''
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    total_price FLOAT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES goods(id)
)
'''
