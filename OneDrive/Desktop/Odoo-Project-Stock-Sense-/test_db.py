import psycopg2

creds = [
    ('postgres', 'postgres'),
    ('postgres', 'root'),
    ('postgres', 'admin'),
    ('postgres', 'password'),
    ('openpg', 'openpgpwd'),
    ('odoo', 'odoo')
]

for user, pwd in creds:
    try:
        psycopg2.connect(dbname='postgres', user=user, password=pwd, host='localhost')
        print(f"SUCCESS: {user} / {pwd}")
        break
    except Exception as e:
        pass
