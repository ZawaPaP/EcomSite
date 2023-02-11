# Import required modules
import csv
import sqlite3
import pandas as pd

def init():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS products (
        id integer primary key autoincrement,
        product_id, 
        name, 
        description,
        price_id,
        value,
        currency)"""
    cursor.execute(sql)
    conn.commit()
    conn.close()


def add_data():
    conn = sqlite3.connect('products.db', isolation_level=None)

    df_product = pd.read_csv('csv/products.csv', usecols=[0, 1, 4])
    df_price = pd.read_csv('csv/prices.csv', usecols=[0, 1, 7, 8])

    df = df_product.merge(df_price, how='inner', left_on='id', right_on='Product ID')
    #delete duplicated column
    df = df.drop(columns=['id'])
    #Pandas to_sql
    df.to_sql(name='products', con=conn, if_exists='replace', index=False)
    conn.close()

def get_data():
    conn = sqlite3.connect('products.db', isolation_level=None)
    cursor = conn.cursor()
    sql = """SELECT * FROM products"""
    cursor.execute(sql)
    
    #全レコードを取り出す
    data = (cursor.fetchall())
    conn.close()
    return data
