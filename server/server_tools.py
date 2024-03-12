"""
This script provides command line tools for managing a PostgreSQL database.

It supports the following operations:
- Initialize the database
- Add an entry to the database
- Remove an entry from the database by ID
- List all entries in the database in a readable format

The script uses the psycopg2 library to connect to the database.
The connection parameters are read from environment variables.

Usage:
- python server-tools.py --init
- python server-tools.py --add "Some data"
- python server-tools.py --remove 1
- python server-tools.py --list
"""

import os
import argparse
import psycopg2
import psycopg2.extras

def connect_to_db():
    """
    Connect to the PostgreSQL database using connection parameters from environment variables.
    Returns a connection object.
    """
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'database_name'),
        user=os.getenv('DB_USER', 'database_user'),
        password=os.getenv('DB_PASS', 'database_password'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )
    return conn

def initialize_db(conn):
    """
    Initialize the database. Creates a table named 'licenses' if it doesn't exist.
    Takes a connection object as argument.
    """
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM licenses LIMIT 1")
            print("Table already exists.")
    except psycopg2.Error as _:
        conn.rollback()
        print("Creating new table.")
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS licenses (
                    id SERIAL PRIMARY KEY,
                    hash TEXT NOT NULL UNIQUE,
                    expires_after TIMESTAMP NOT NULL,
                    activation_key TEXT NOT NULL UNIQUE,
                    activated_on TIMESTAMP
                )
            """)
        conn.commit()

def add_entry(conn, entry):
    """
    Add an entry to the database.
    Takes a connection object and the entry data as arguments.
    """
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO licenses (id, hash, expires_after, activation_key, activated_on) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (entry['id'],
             entry['hash'],
             entry['expires_after'],
             entry['activation_key'],
             entry['activated_on'])
        )
    conn.commit()

def remove_entry(conn, entry_id):
    """
    Remove an entry from the database by ID.
    Takes a connection object and the entry ID as arguments.
    """
    with conn.cursor() as cur:
        cur.execute("DELETE FROM entries WHERE id = %s", (entry_id,))
    conn.commit()

def list_entries(conn):
    """
    List all entries in the database in a readable format.
    Takes a connection object as argument.
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM licenses")
        entries = cur.fetchall()
    for entry in entries:
        print(f"""
              ID: {entry['id']},
              Hash: {entry['hash']},
              Expires after: {entry['expires_after']},
              Activation key: {entry['activation_key']},
              Activated on: {entry['activated_on']}""")

def main():
    """
    Parse command line arguments and call the appropriate function.
    """
    parser = argparse.ArgumentParser(description='Manage database entries.')
    parser.add_argument('--init',
                        action='store_true',
                        help='Initialize the database')
    parser.add_argument('--add',
                        metavar='ENTRY',
                        help='''Add an entry to the database.
                        Example: --add "id=1 hash=hash expires_after=2024-02-01
                        activation_key=activation-key activated_on=2024-01-01"''')
    parser.add_argument('--remove',
                        metavar='ID',
                        type=int,
                        help='Remove an entry from the database by ID')
    parser.add_argument('--list',
                        action='store_true',
                        help='List all entries in the database')

    args = parser.parse_args()

    conn = connect_to_db()

    if args.init:
        initialize_db(conn)
    elif args.add:
        arguments = args.add.split(' ')
        entry = {
            'id': arguments[0].split('id=')[-1][-1],
            'hash': arguments[1].split('hash=')[-1],
            'expires_after': arguments[2].split('expires_after=')[-1],
            'activation_key': arguments[3].split('activation_key=')[-1],
            'activated_on': arguments[4].split('activated_on=')[-1],
        }
        add_entry(conn, entry)
    elif args.remove:
        remove_entry(conn, args.remove)
    elif args.list:
        list_entries(conn)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
