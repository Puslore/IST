import sqlite3


def get_connection(path):
    '''Return connection cursor with DB'''
    conn = sqlite3.connect(path)
    cursor = conn.cursor()    
    
    return cursor