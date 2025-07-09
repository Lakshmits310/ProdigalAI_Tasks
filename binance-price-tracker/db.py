import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        dbname="binance_db",
        user="postgres",
        password="lakshmits",  # use your actual password
        host="localhost",
        port="5433"
    )

def insert_price(symbol, price, timestamp):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO prices (symbol, price, timestamp)
        VALUES (%s, %s, %s)
    """, (symbol, price, timestamp))
    conn.commit()
    cur.close()
    conn.close()
