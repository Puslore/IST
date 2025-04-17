import sqlite3
import csv
import os
from os.path import exists

# 1. Создание базы данных по схеме
def create_database(check):
    """Создание базы данных в соответствии со схемой."""
    conn = sqlite3.connect('./students.db')
    cursor = conn.cursor()
    
    # Создание таблиц в соответствии со схемой
    if not check:
        cursor.execute('''
        CREATE TABLE уровень_обучения (
            id_уровня INTEGER PRIMARY KEY,
            название VARCHAR
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE направления (
            id_направления INTEGER PRIMARY KEY,
            название VARCHAR
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE типы_обучения (
            id_типа INTEGER PRIMARY KEY,
            название VARCHAR
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE студенты (
            id_студента INTEGER PRIMARY KEY,
            id_уровня INTEGER,
            id_направления INTEGER,
            id_типа_обучения INTEGER,
            фамилия VARCHAR,
            имя VARCHAR,
            отчество VARCHAR,
            средний_балл INTEGER,
            FOREIGN KEY (id_уровня) REFERENCES уровень_обучения(id_уровня),
            FOREIGN KEY (id_направления) REFERENCES направления(id_направления),
            FOREIGN KEY (id_типа_обучения) REFERENCES типы_обучения(id_типа)
        )
        ''')
        
        conn.commit()
        print("База данных создана успешно.")
    return conn


def files_check(files: list) -> bool:
    """Проверка существования CSV файлов."""
    for file in files:
        if not os.path.exists(f'./{file[0]}'):
            raise Exception('Нет необходимых CSV файлов')
            # with open(f'./{file[0]}', 'w'):
            #     pass            
            # if os.path.exists(f'./{file[0]}'):
            #     return_ = True
            # if not return_:
            #     raise Exception('')

    return True


def import_from_csv(conn):
    """Импорт данных из CSV файлов в таблицы базы данных."""
    cursor = conn.cursor()
    
    # Определение CSV файлов и соответствующих таблиц
    csv_mappings = [
        ('level.csv', 'уровень_обучения'),
        ('directions.csv', 'направления'),
        ('types.csv', 'типы_обучения'),
        ('students.csv', 'студенты')
    ]
    
    # Проверка наличия всех CSV файлов
    all_files_exist = files_check(csv_mappings)
    
    if all_files_exist:
        # Импорт данных из каждого CSV файла
        for csv_file, table_name in csv_mappings:
            try:
                with open(csv_file, 'r', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    
                    # Получение имен столбцов из таблицы
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = [row[1] for row in cursor.fetchall()]
                    
                    # Проверка, является ли первая строка заголовком
                    first_row = next(csv_reader, None)
                    if first_row and len(first_row) == len(columns):
                        if all(col.lower() in [c.lower() for c in columns] for col in first_row):
                            pass
                        else:
                            file.seek(0)
                    
                    # Чтение и вставка строк данных
                    for row in csv_reader:
                        if len(row) != len(columns):
                            print(f"Предупреждение: Пропуск строки в {csv_file} с неверным числом полей.")
                            continue
                        
                        placeholders = ', '.join(['?' for _ in columns])
                        
                        # Преобразование числовых значений
                        values = []
                        for i, val in enumerate(row):
                            col_name = columns[i].lower()
                            if 'id' in col_name or 'балл' in col_name:
                                try:
                                    values.append(int(val))
                                except ValueError:
                                    print(f"Предупреждение: Не удалось преобразовать '{val}' в целое число в {csv_file}. Используется 0.")
                                    values.append(0)
                            else:
                                values.append(val)
                        
                        cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
                    
                    print(f"Данные из {csv_file} успешно импортированы в таблицу {table_name}.")
                    
            except Exception as e:
                raise Exception(f"Ошибка при импорте данных из {csv_file}: {e}")
        
        conn.commit()


def execute_queries(conn):
    """Выполнение и отображение требуемых SQL запросов."""
    cursor = conn.cursor()
    
    print("\n======= РЕЗУЛЬТАТЫ ЗАПРОСОВ =======")
    
    # Запрос 1
    cursor.execute("SELECT COUNT(*) FROM студенты")
    count = cursor.fetchone()[0]
    print(f"\n1. Количество всех студентов: {count}")
    
    # Запрос 2
    cursor.execute('''
    SELECT н.название, COUNT(с.id_студента) as count
    FROM студенты с
    JOIN направления н ON с.id_направления = н.id_направления
    GROUP BY н.название
    ORDER BY count DESC
    ''')
    print("\n2. Количество студентов по направлениям:")
    for direction, count in cursor.fetchall():
        print(f"   {direction}: {count}")
    
    # Запрос 3
    cursor.execute('''
    SELECT т.название, COUNT(с.id_студента) as count
    FROM студенты с
    JOIN типы_обучения т ON с.id_типа_обучения = т.id_типа
    GROUP BY т.название
    ORDER BY count DESC
    ''')
    print("\n3. Количество студентов по формам обучения:")
    for edu_type, count in cursor.fetchall():
        print(f"   {edu_type}: {count}")
    
    # Запрос 4
    cursor.execute('''
    SELECT н.название,
           MAX(с.средний_балл) as max_score,
           MIN(с.средний_балл) as min_score,
           ROUND(AVG(с.средний_балл), 2) as avg_score
    FROM студенты с
    JOIN направления н ON с.id_направления = н.id_направления
    GROUP BY н.название
    ORDER BY avg_score DESC
    ''')
    print("\n4. Максимальный, минимальный, средний баллы студентов по направлениям:")
    for direction, max_score, min_score, avg_score in cursor.fetchall():
        print(f"   {direction}:")
        print(f"     Максимальный балл: {max_score}")
        print(f"     Минимальный балл: {min_score}")
        print(f"     Средний балл: {avg_score}")
    
    # Запрос 5
    cursor.execute('''
    SELECT 
        н.название as direction,
        у.название as level,
        т.название as type,
        ROUND(AVG(с.средний_балл), 2) as avg_score
    FROM студенты с
    JOIN направления н ON с.id_направления = н.id_направления
    JOIN уровень_обучения у ON с.id_уровня = у.id_уровня
    JOIN типы_обучения т ON с.id_типа_обучения = т.id_типа
    GROUP BY н.название, у.название, т.название
    ORDER BY avg_score DESC
    ''')
    print("\n5. Средний балл студентов по направлениям, уровням и формам обучения:")
    for direction, level, edu_type, avg_score in cursor.fetchall():
        print(f"   {direction}, {level}, {edu_type}: {avg_score}")
    
    # Запрос 6
    cursor.execute('''
    SELECT с.фамилия, с.имя, с.отчество, с.средний_балл
    FROM студенты с
    JOIN направления н ON с.id_направления = н.id_направления
    JOIN типы_обучения т ON с.id_типа_обучения = т.id_типа
    WHERE н.название = 'Прикладная Информатика' AND т.название = 'Очная'
    ORDER BY с.средний_балл DESC
    LIMIT 5
    ''')
    print("\n6. Топ-5 студентов направления 'Прикладная Информатика' очной формы обучения:")
    results = cursor.fetchall()
    if results:
        for i, (last_name, first_name, middle_name, score) in enumerate(results, 1):
            print(f"   {i}. {last_name} {first_name} {middle_name}: {score}")
    else:
        print("   Нет студентов, соответствующих условиям запроса.")
    
    # Запрос 7
    cursor.execute('''
    SELECT фамилия, COUNT(*) as count
    FROM студенты
    GROUP BY фамилия
    HAVING COUNT(*) > 1
    ORDER BY count DESC
    ''')
    print("\n7. Сколько однофамильцев в данной базе:")
    results = cursor.fetchall()
    if results:
        total_same_last_name = sum(count for _, count in results)
        print(f"   Всего найдено {total_same_last_name} фамилий, которые встречаются более одного раза.")
        for last_name, count in results:
            print(f"   '{last_name}' встречается {count} раз")
    else:
        print("  Нет однофамильцев")
    
    # Запрос 8
    cursor.execute('''
    SELECT фамилия, имя, отчество, COUNT(*) as count
    FROM студенты
    GROUP BY фамилия, имя, отчество
    HAVING COUNT(*) > 1
    ORDER BY count DESC
    ''')
    print("\n8. Полные тёзки (совпадают фамилии, имена, отчества):")
    results = cursor.fetchall()
    if results:
        for last_name, first_name, middle_name, count in results:
            print(f"   {last_name} {first_name} {middle_name}: {count} студентов")
    else:
        print("   Нет полных тёзок")


def check_db(path: str) -> bool:
    """Проверка существования БД"""
    if exists(path):
        return True
    else:
        with open(path, 'w'):
            pass
    if exists(path):
        return False
    else:
        raise Exception('Ошибка создания файла БД')


def main():
    conn = None
    try:
        # Создание базы данных
        path = './students.db'
        check = check_db(path)
        conn = create_database(check)

        # Импорт данных из CSV
        if not check:
            import_from_csv(conn)

        # Выполнение запросов
        execute_queries(conn)

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        if conn:
            conn.close()
            print("\nРабота с базой данных завершена.")

if __name__ == "__main__":
    main()
