import sqlite3
import datetime


def init():
    conn = sqlite3.connect('order.db', isolation_level=None)
    cursor = conn.cursor()
    sql = """CREATE TABLE IF NOT EXISTS order_history(id integer primary key autoincrement, user, date, price, currency)"""
    cursor.execute(sql)#executeコマンドでSQL文を実行
    conn.commit()
    conn.close()

""" 
レコードを追加する場合はinsert文を使う。
SQLインジェクションという不正SQL命令への脆弱性対策でpythonの場合は「？」を使用して記載するのが基本。
"""
def add_data(price, currency):
    conn = sqlite3.connect('order.db', isolation_level=None)
    cursor = conn.cursor()
    user = user.id
    sql = """INSERT INTO order_history (user, date, price, currency) VALUES (?, ?, ?)"""#?は後で値を受け取るよという意味

    data = ((datetime.datetime.now(), price, currency))
    cursor.execute(sql, data)
    conn.commit()#コミットする
    conn.close()

def check_data():
    sql = """SELECT * FROM order_history"""
    conn = sqlite3.connect('order.db', isolation_level=None)
    cursor = conn.cursor()
    cursor.execute(sql)
    print(cursor.fetchall())#全レコードを取り出す
    conn.close()



add_data()