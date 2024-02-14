"""
This script provides command line tools for managing a PostgreSQL database.

It supports the following operations:
- Initialize the database
- Add an entry to the database
- Remove an entry from the database by ID
- List all entries in the database in a readable format

The script uses the psycopg2 library to connect to the database. The connection parameters are read from environment variables.

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
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

def initialize_db(conn):
    """
    Initialize the database. Creates a table named 'licenses' if it doesn't exist.
    Takes a connection object as argument.
    """
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS licenses (
                id SERIAL PRIMARY KEY,
                hash TEXT NOT NULL,
                expires_after DATETIME NOT NULL,
                activation_key TEXT NOT NULL,
                activated_on DATETIME
            )
        """)
    conn.commit()

def add_entry(conn, entry):
    """
    Add an entry to the database.
    Takes a connection object and the entry data as arguments.
    """
    with conn.cursor() as cur:
        cur.execute("INSERT INTO licenses (data) VALUES (%s)", (entry,))
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
        print(f"ID: {entry['id']}, Data: {entry['data']}")

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
                        help='Add an entry to the database')
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
        add_entry(conn, args.add)
    elif args.remove:
        remove_entry(conn, args.remove)
    elif args.list:
        list_entries(conn)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
