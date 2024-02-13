import os
from flask import Flask, request
import psycopg2

app = Flask(__name__)

def check_license(hash, key):
    conn = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT valid FROM licenses WHERE hash = %s AND key = %s", (hash, key))
    result = cur.fetchone()
    conn.close()
    if result is None:
        return False
    return result[0]

@app.route('/check_license', methods=['GET'])
def handle_check_license():
    hash = request.args.get('hash')
    key = request.args.get('key')
    valid = check_license(hash, key)
    return {'valid': valid}

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))