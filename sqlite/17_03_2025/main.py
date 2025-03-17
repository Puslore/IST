import sqlite3
import os


filename = './test_base.db'
if not os.path.exists(filename):
    with open(filename, 'w'):
        pass


connection = sqlite3.connect('test_base.db')
cursor = connection.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS 'job_titles' (
        'id_job_title' INTEGER PRIMARY KEY NOT NULL UNIQUE,
        'name' TEXT NOT NULL UNIQUE
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS 'employees' (
        'id' INTEGER PRIMARY KEY NOT NULL UNIQUE,
        'surname' TEXT NOT NULL,
        'name' TEXT NOT NULL,
        'id_job_title' INTEGER NOT NULL,
        FOREIGN KEY('id_job_title') REFERENCES job_titles('id_job_title')
    );
''')

cursor.execute("""
    CREATE TABLE IF NOT EXISTS 'clients' (
    'client_id' INTEGER PRIMARY KEY NOT NULL UNIQUE,
    'organisation' TEXT NOT NULL,
    'phone' INTEGER NOT NULL
    );
""")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS 'orders' (
    'order_id' INTEGER PRIMARY KEY NOT NULL UNIQUE,
    'employee_id' INTEGER NOT NULL,
    'client_id' INTEGER NOT NULL,
    'sum' INTEGER NOT NULL,
    'date' DATETIME NOT NULL,
    'checked' BOOLEAN NOT NULL,
    FOREIGN KEY('client_id') REFERENCES clients('client_id')
    );
''')


job_titles_data = [
    (1, 'Manager'),
    (2, 'Developer'),
    (3, 'Analytic'),
    (4, 'Designer'),
    (5, 'Promise')
]

employees_data = [
    (1, "Иванов", "Иван", 2),
    (2, "Петров", "Петр", 1),
    (3, "Сидорова", "Мария", 3),
    (4, "Козлов", "Алексей", 2),
    (5, "Васильева", "Ольга", 4),
    (6, 'Алабайкин', 'Тимофей', 5),
    (7, 'Тимофейкин', 'Алабай', 5)
]

clients_data = [
    (1, 'ООО "Здоровая Проблема"', '88005553535'),
    (2, 'ООО СтройПромМаркет', '1231231230'),
    (3, 'ИП Все починим все сломаем!', '99999999999')
]

orders_data = [
    (1, 6, 1, 600, '08-03-2025', True),
    (2, 6, 2, 400, '01-01-2000', True)
]


cursor.executemany("INSERT OR IGNORE INTO 'job_titles' ('id_job_title', 'name') VALUES (?, ?)", job_titles_data)
cursor.executemany("INSERT OR IGNORE INTO 'employees' ('id', 'surname', 'name', 'id_job_title') VALUES (?, ?, ?, ?)", employees_data)
cursor.executemany('INSERT OR IGNORE INTO "clients" ("client_id", "organisation", "phone") VALUES (?, ?, ?)', clients_data)
cursor.executemany('INSERT OR IGNORE INTO "orders" ("order_id", "employee_id", "client_id", "sum", "date", "checked") VALUES (?, ?, ?, ?, ?, ?)', orders_data)


cursor.execute('''
    SELECT e.surname, e.name, j.name as job_title
    FROM employees e
    JOIN job_titles j ON e.id_job_title = j.id_job_title
''')

employees_with_job_titles = cursor.fetchall()
# print(employees_with_job_titles)
print('сотрудники и их должности')

for employee in employees_with_job_titles:
    print(f'{employee[0]} {employee[1]} - {employee[2]}')


cursor.execute('''
    SELECT e.surname, e.name, j.organisation, k.date
    FROM employees e
    JOIN orders k ON e.id = k.employee_id
    JOIN clients j ON k.client_id = j.client_id 
''')

orders_out = cursor.fetchall()
print('\nЗаказы')

# print(orders_out)

for order in orders_out:
    print(f'{order[1]} {order[0]}: {order[2]} -- {order[3]}')


connection.commit()
connection.close()
