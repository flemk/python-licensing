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

import os
from flask import Flask, request
from server_tools import initialize_db, connect_to_db
from waitress import serve

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
    cur.execute("SELECT * FROM licenses WHERE activation_key = %s",
                (key,))
    result = cur.fetchone()

    # TODO
    # 1. Check if there is already a activated license with matching key
    # 1.1. If there is, check the hash
    # 1.2. Check the expiration date
    # 3. If there is not, check activation key and activate
    # 3.1. Insert hash and activation data into the database
    # 4. Generate new key and send back to the client

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
    key = request.args.get('key')
    valid = check_license(license_hash, key)
    return {'valid': valid}

if __name__ == '__main__':
    # TODO wait for the db service to accept connections
    conn = connect_to_db()
    initialize_db(conn)

    if os.getenv('ENVIRONMENT', 'production') == 'development':
        print("Running in development mode.")
        app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0')
    else:
        print("Running in production mode.")
        serve(app, host="0.0.0.0", port=os.getenv('LICENSE_PORT', '5000'), threads=4)
