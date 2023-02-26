import sqlite3
import datetime
import pandas as pd


def init():
    conn = sqlite3.connect('db/user.db', isolation_level=None)
    cursor = conn.cursor()
    
    sql = """CREATE TABLE IF NOT EXISTS user(
        id integer primary key autoincrement,
        fn,
        ln,
        em,
        ph,
        address,
        address2,
        created_time
        )"""
    cursor.execute(sql)
    conn.commit()
    conn.close()

def add_data(user):
    conn = sqlite3.connect('db/user.db', isolation_level=None)
    user['created_time'] = datetime.datetime.now()
    print(user)
    df = pd.DataFrame.from_dict([user])
    print(df)
    #Pandas to_sql
    df.to_sql(name='user', con=conn, if_exists='append', index=False)
    conn.close()

