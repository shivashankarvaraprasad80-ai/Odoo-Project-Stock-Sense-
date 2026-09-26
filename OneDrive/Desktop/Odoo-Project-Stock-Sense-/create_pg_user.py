import psycopg2
import sys
try:
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute("CREATE USER odoo WITH PASSWORD 'odoo' CREATEDB;")
        print("User odoo created")
    except psycopg2.errors.DuplicateObject:
        print("User odoo already exists")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
