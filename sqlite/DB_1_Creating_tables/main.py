import sqlite3
import os
import csv

def create_database_connection(db_file):
    if not os.path.exists(db_file):
        with open(db_file, 'w'):
            pass
    
    connection = sqlite3.connect(db_file)
    return connection

def create_tables(cursor):
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
    'phone' TEXT,
    'id_job_title' INTEGER NOT NULL,
    FOREIGN KEY('id_job_title') REFERENCES job_titles('id_job_title')
    );
    ''')

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS 'clients' (
    'client_id' INTEGER PRIMARY KEY NOT NULL UNIQUE,
    'organisation' TEXT NOT NULL,
    'phone' TEXT NOT NULL
    );
    """)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS 'orders' (
    'order_id' INTEGER PRIMARY KEY NOT NULL UNIQUE,
    'client_id' INTEGER NOT NULL,
    'employee_id' INTEGER NOT NULL,
    'sum' INTEGER NOT NULL,
    'date' DATETIME NOT NULL,
    'checked' BOOLEAN NOT NULL,
    FOREIGN KEY('client_id') REFERENCES clients('client_id'),
    FOREIGN KEY('employee_id') REFERENCES employees('id')
    );
    ''')

def prepare_data():
    job_titles_data = [
        (1, 'Manager'),
        (2, 'Developer'),
        (3, 'Analytic'),
        (4, 'Designer'),
        (5, 'Promise')
    ]

    employees_data = [
        (1, "Иванов", "Иван", "+7-111-111-11-11", 2),
        (2, "Петров", "Петр", "+7-222-222-22-22", 1),
        (3, "Сидорова", "Мария", "+7-333-333-33-33", 3),
        (4, "Козлов", "Алексей", "+7-444-444-44-44", 2),
        (5, "Васильева", "Ольга", "+7-555-555-55-55", 4),
        (6, 'Алабайкин', 'Тимофей', "8-900-555-35-35", 5),
        (7, 'Тимофейкин', 'Алабай', "+7-777-777-77-77", 5)
    ]

    clients_data = [
        (1, 'ООО "Здоровая Проблема"', '88005553535'),
        (2, 'ООО СтройПромМаркет', '1231231230'),
        (3, 'ИП Все починим все сломаем!', '99999999999')
    ]

    orders_data = [
        (1, 1, 6, 600, '2025-03-08', True),
        (2, 2, 6, 400, '2000-01-01', True),
        (3, 3, 1, 900, '2024-12-15', False),
        (4, 1, 2, 1200, '2025-01-20', True),
        (5, 2, 3, 750, '2025-02-10', False),
        (6, 3, 4, 500, '2025-03-15', True),
        (7, 1, 5, 850, '2025-04-01', False)
    ]

    return {
        'job_titles': job_titles_data,
        'employees': employees_data,
        'clients': clients_data,
        'orders': orders_data
    }

def fill_tables(cursor, data):
    cursor.executemany("INSERT OR IGNORE INTO 'job_titles' ('id_job_title', 'name') VALUES (?, ?)", data['job_titles'])
    cursor.executemany("INSERT OR IGNORE INTO 'employees' ('id', 'surname', 'name', 'phone', 'id_job_title') VALUES (?, ?, ?, ?, ?)", data['employees'])
    cursor.executemany('INSERT OR IGNORE INTO "clients" ("client_id", "organisation", "phone") VALUES (?, ?, ?)', data['clients'])
    cursor.executemany('INSERT OR IGNORE INTO "orders" ("order_id", "client_id", "employee_id", "sum", "date", "checked") VALUES (?, ?, ?, ?, ?, ?)', data['orders'])

def execute_basic_queries(cursor):
    print('Сотрудники и их должности')
    cursor.execute('''
    SELECT e.surname, e.name, j.name as job_title
    FROM employees e
    JOIN job_titles j ON e.id_job_title = j.id_job_title
    ''')
    employees_with_job_titles = cursor.fetchall()
    for employee in employees_with_job_titles:
        print(f'{employee[0]} {employee[1]} - {employee[2]}')

    print('\nЗаказы')
    cursor.execute('''
    SELECT e.surname, e.name, j.organisation, k.date
    FROM employees e
    JOIN orders k ON e.id = k.employee_id
    JOIN clients j ON k.client_id = j.client_id
    ''')
    orders_out = cursor.fetchall()
    for order in orders_out:
        print(f'{order[1]} {order[0]}: {order[2]} -- {order[3]}')

def execute_simple_queries(cursor):
    print('\n=== Пять простых запросов ===')

    print('\n1. Общее количество заказов:')
    cursor.execute('SELECT COUNT(*) FROM orders')
    result = cursor.fetchone()
    print(f'Всего заказов: {result[0]}')

    print('\n2. Максимальная сумма заказа:')
    cursor.execute('SELECT MAX(sum) FROM orders')
    result = cursor.fetchone()
    print(f'Максимальная сумма: {result[0]}')

    print('\n3. Общая сумма всех заказов:')
    cursor.execute('SELECT SUM(sum) FROM orders')
    result = cursor.fetchone()
    print(f'Общая сумма: {result[0]}')

    print('\n4. Средняя сумма заказа:')
    cursor.execute('SELECT AVG(sum) FROM orders')
    result = cursor.fetchone()
    print(f'Средняя сумма: {result[0]}')

    print('\n5. Количество выполненных заказов:')
    cursor.execute('SELECT COUNT(*) FROM orders WHERE checked = 1')
    result = cursor.fetchone()
    print(f'Количество выполненных заказов: {result[0]}')

def execute_aggregation_queries(cursor):

    print('\n1. Количество заказов по клиентам:')
    cursor.execute('''
    SELECT c.organisation, COUNT(o.order_id) as order_count
    FROM clients c
    LEFT JOIN orders o ON c.client_id = o.client_id
    GROUP BY c.client_id
    ''')
    results = cursor.fetchall()
    for result in results:
        print(f'{result[0]}: {result[1]} заказов')

    print('\n2. Суммарная стоимость заказов по сотрудникам:')
    cursor.execute('''
    SELECT e.surname, e.name, SUM(o.sum) as total_sum
    FROM employees e
    LEFT JOIN orders o ON e.id = o.employee_id
    GROUP BY e.id
    ''')
    results = cursor.fetchall()
    for result in results:
        total = result[2] if result[2] is not None else 0
        print(f'{result[0]} {result[1]}: {total} руб.')

    print('\n3. Средняя сумма заказа по должностям сотрудников:')
    cursor.execute('''
    SELECT j.name, AVG(o.sum) as avg_sum
    FROM job_titles j
    LEFT JOIN employees e ON j.id_job_title = e.id_job_title
    LEFT JOIN orders o ON e.id = o.employee_id
    GROUP BY j.id_job_title
    ''')
    results = cursor.fetchall()
    for result in results:
        avg_sum = result[1] if result[1] is not None else 0
        print(f'{result[0]}: {avg_sum} руб.')

def execute_join_queries(cursor):

    print('\n1. Выполненные заказы с суммой больше 500:')
    cursor.execute('''
    SELECT o.order_id, c.organisation, e.surname, e.name, o.sum, o.date
    FROM orders o
    JOIN clients c ON o.client_id = c.client_id
    JOIN employees e ON o.employee_id = e.id
    WHERE o.checked = 1 AND o.sum > 500
    ''')
    results = cursor.fetchall()
    for result in results:
        print(f'Заказ №{result[0]}: {result[1]}, Сотрудник: {result[3]} {result[2]}, Сумма: {result[4]}, Дата: {result[5]}')

    print('\n2. Невыполненные заказы для ООО "Здоровая Проблема":')
    cursor.execute('''
    SELECT o.order_id, e.surname, e.name, o.sum, o.date
    FROM orders o
    JOIN employees e ON o.employee_id = e.id
    JOIN clients c ON o.client_id = c.client_id
    WHERE o.checked = 0 AND c.organisation = 'ООО "Здоровая Проблема"'
    ''')
    results = cursor.fetchall()
    for result in results:
        print(f'Заказ №{result[0]}: Сотрудник: {result[2]} {result[1]}, Сумма: {result[3]}, Дата: {result[4]}')

    print('\n3. Заказы, выполненные разработчиками:')
    cursor.execute('''
    SELECT o.order_id, e.surname, e.name, c.organisation, o.sum, o.date
    FROM orders o
    JOIN employees e ON o.employee_id = e.id
    JOIN clients c ON o.client_id = c.client_id
    JOIN job_titles j ON e.id_job_title = j.id_job_title
    WHERE j.name = 'Developer'
    ''')
    results = cursor.fetchall()
    for result in results:
        print(f'Заказ №{result[0]}: Сотрудник: {result[2]} {result[1]}, Клиент: {result[3]}, Сумма: {result[4]}, Дата: {result[5]}')

def create_sample_files():
    with open('new_employees.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'surname', 'name', 'phone', 'id_job_title'])
        writer.writerow([8, 'Смирнов', 'Дмитрий', '+7-888-888-88-88', 3])
        writer.writerow([9, 'Кузнецова', 'Елена', '+7-999-999-99-99', 1])

    with open('new_clients.txt', 'w', encoding='utf-8') as file:
        file.write('client_id\torganisation\tphone\n')
        file.write('4\tЗАО "Технологии будущего"\t74951234567\n')
        file.write('5\tИП Иванов И.И.\t79091234567\n')

def import_data_from_files(cursor):
    """Импортирует данные из внешних файлов (CSV, TXT)"""
    print('\n=== Импорт данных из внешних файлов ===')
    
    create_sample_files()

    print('\nИмпорт сотрудников из CSV:')
    try:
        with open('new_employees.csv', 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                if len(row) == 5:
                    cursor.execute('''
                    INSERT OR IGNORE INTO employees (id, surname, name, phone, id_job_title) 
                    VALUES (?, ?, ?, ?, ?)
                    ''', row)
                    print(f'Добавлен сотрудник: {row[2]} {row[1]}')
    except Exception as e:
        print(f'Ошибка при импорте из CSV: {e}')

    print('\nИмпорт клиентов из TXT:')
    try:
        with open('new_clients.txt', 'r', encoding='utf-8') as file:
            next(file)
            for line in file:
                fields = line.strip().split('\t')
                if len(fields) == 3:
                    cursor.execute('''
                    INSERT OR IGNORE INTO clients (client_id, organisation, phone) 
                    VALUES (?, ?, ?)
                    ''', fields)
                    print(f'Добавлен клиент: {fields[1]}')
    except Exception as e:
        print(f'Ошибка при импорте из TXT: {e}')

    print('\nВсе сотрудники после импорта:')
    cursor.execute('SELECT id, surname, name, phone, id_job_title FROM employees')
    results = cursor.fetchall()
    for row in results:
        print(f'ID: {row[0]}, ФИО: {row[2]} {row[1]}, Телефон: {row[3]}, ID должности: {row[4]}')

    print('\nВсе клиенты после импорта:')
    cursor.execute('SELECT client_id, organisation, phone FROM clients')
    results = cursor.fetchall()
    for row in results:
        print(f'ID: {row[0]}, Организация: {row[1]}, Телефон: {row[2]}')

def main():
    db_file = './test_base.db'
    
    connection = create_database_connection(db_file)
    cursor = connection.cursor()
    
    create_tables(cursor)
    
    data = prepare_data()
    fill_tables(cursor, data)
    
    execute_basic_queries(cursor)
    
    execute_simple_queries(cursor)
    
    execute_aggregation_queries(cursor)
    
    execute_join_queries(cursor)
    
    import_data_from_files(cursor)
    
    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
