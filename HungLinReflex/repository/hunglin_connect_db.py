import mysql.connector

def connect():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="hunglin",
        password="Rafaela4840",
        database='hunglin'
    )
    cursor = conn.cursor()
    return conn, cursor
