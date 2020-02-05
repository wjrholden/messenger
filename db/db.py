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
        print("DB connection created")
        print(f"Current SQLite version: {sqlite3.version}")
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


def select_message_by_recipient_name(conn, recipient_name):
    """
    Query for messages to a given recipient
    :param conn:
    :param recipient_name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages WHERE recipient_id="
                "(select id from users where name=?)",
                (recipient_name,))
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
    
    return rows


def main():
    database = "messenger.db"
    # create a database connection
    conn = create_connection(database)

    with conn:
        # # create new users
        # sender = ('chad',)
        # sender_id = create_user(conn, sender)
        # print(f"sender [{sender}] created with user_id: {sender_id}")
        # recipient = ('chris',)
        # recipient_id = create_user(conn, recipient)
        # print(f"recipient [{recipient}] created with user_id: {recipient_id}")
 
        # # create a message
        # message = (sender_id, recipient_id, "test message 3")
        # message_id = create_message(conn, message)
        # print(f"message created [{message}] with message_id: {message_id}")

        select_user_id_by_name(conn, 'johnny')

    if conn:
        conn.close()


if __name__ == '__main__':
    main()