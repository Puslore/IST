import csv


def import_from_csv(paths: list) -> dict:
    '''Import data from test CSV files'''
    data = {}

    for path in paths:
        filename = path.split('/')[-1].split('.')[0]
        data[filename] = read_csv(path)

    return data


def read_csv(path: str) -> list:
    '''Read CSV file'''
    data = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for string in reader:
                data.append(tuple(string))

        return data

    except Exception as err:
        raise Exception(f'Error with reading csv file - {err}')
