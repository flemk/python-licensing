"""
This module defines a Flask application that provides a license checking service.

The application exposes a single endpoint, /check_license, which accepts GET requests.
The endpoint expects two parameters, 'hash' and 'key', which represent a license 
hash and key respectively.
The application checks the provided license against a PostgreSQL database and
returns whether the license is valid.

The database connection parameters are read from environment variables:
- DB_NAME: The name of the database.
- DB_USER: The username to connect to the database.
- DB_PASS: The password to connect to the database.

The application is served over HTTPS. The SSL certificate and key are read
from 'cert.pem' and 'key.pem' respectively.
"""

from flask import Flask, request
from server_tools import initialize_db, connect_to_db

app = Flask(__name__)
conn = None

def check_license(license_hash, key):
    """
    Check if a license is valid.

    This function checks if a license, represented by a hash and a key, is valid.
    It does this by querying a PostgreSQL database.

    Parameters:
    hash (str): The hash of the license.
    key (str): The key of the license.

    Returns:
    bool: True if the license is valid, False otherwise.
    """
    conn_ = conn
    if conn is None or conn.closed:
        conn_ = connect_to_db()

    cur = conn_.cursor()
    cur.execute("SELECT * FROM licenses WHERE hash = %s AND activation_key = %s",
                (license_hash, key))
    result = cur.fetchone()
    if result is None:
        return False
    return result[0]

@app.route('/check_license', methods=['GET'])
def handle_check_license():
    """
    Handle a request to check a license.

    This function handles a GET request to the /check_license endpoint.
    It reads the 'hash' and 'key' parameters from the request, checks if the license is valid,
    and returns a JSON response with the result.

    Returns:
    dict: A dictionary with the keys 'valid' (a boolean indicating if the license is valid)
    and 'message' (a string with a message about the license status).
    """
    license_hash = request.args.get('hash')
    key = request.args.get('activation_key')
    valid = check_license(license_hash, key)
    return {'valid': valid}

if __name__ == '__main__':
    conn = connect_to_db()
    initialize_db(conn)
    app.run(ssl_context=('cert.pem', 'key.pem'))
