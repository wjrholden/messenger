import sqlite3
from sqlite3 import Error

"""
implementation borrowed from SQLite tutorial for Python:
https://www.sqlitetutorial.net/sqlite-python/
"""


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"DB connected to {db_file}")
    except Error as e:
        print(f"An error occurred connecting to {db_file}: {e}")
        raise e
    return conn


def create_user(conn, user):
    """
    Insert a new user in the users table
    :param conn:
    :param user:
    :return: user id
    """
    insert_sql = ''' INSERT INTO users(name)
                     VALUES(?) '''
    cur = conn.cursor()
    cur.execute(insert_sql, user)
    conn.commit()
    return cur.lastrowid


def create_message(conn, msg):
    """
    Insert a new message in the messages table
    :param conn:
    :param msg:
    :return:
    """
    sql = ''' INSERT INTO messages(sender_id,recipient_id,content)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, msg)
    conn.commit()
    return cur.lastrowid


def select_user_id_by_name(conn, user_name):
    """
    Query user ID by name
    :param conn:
    :param user_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE name=?", (user_name,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows


def get_all_messages(conn):
    """
    Query for all messages
    :param conn:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows


def select_messages_by_recipient_and_sender(conn, recipient_name, sender_name):
    """
    Query for messages to a given recipient from a given sender
    :param conn:
    :param recipient_name:
    :param sender_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages "
                "WHERE recipient_id="
                "(SELECT id FROM users WHERE name=?) "
                "AND sender_id="
                "(SELECT id FROM users WHERE name=?)",
                (recipient_name, sender_name))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows


def select_messages_by_recipient_name(conn, recipient_name):
    """
    Query for messages to a given recipient
    :param conn:
    :param recipient_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages "
                "WHERE recipient_id="
                "(SELECT id FROM users WHERE name=?)",
                (recipient_name, ))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows


def select_messages_by_sender_name(conn, sender_name):
    """
    Query for messages from a given sender
    :param conn:
    :param sender_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages "
                "WHERE sender_id="
                "(SELECT id FROM users WHERE name=?)",
                (sender_name, ))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows


def main():
    database = "../db/messenger.db"
    # create a database connection
    conn = create_connection(database)

    with conn:
        get_all_messages(conn)

    if conn:
        conn.close()


if __name__ == '__main__':
    main()
