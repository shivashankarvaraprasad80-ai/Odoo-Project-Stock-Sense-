import psycopg2

common_pwds = [
    'postgres', 'root', 'admin', 'password', '1234', '12345', '123456', 
    'admin123', 'root123', 'openpgpwd', 'odoo', 'system', 'qwerty', '12345678', '123456789'
]

success = False
for pwd in common_pwds:
    try:
        psycopg2.connect(dbname='postgres', user='postgres', password=pwd, host='127.0.0.1')
        print(f"FOUND PASSWORD: {pwd}")
        success = True
        break
    except Exception as e:
        pass

if not success:
    print("NO PASSWORD MATCHED")
