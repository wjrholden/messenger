import sqlite3
from sqlite3 import Error

"""
created with guidance from SQLite tutorial for Python:
https://www.sqlitetutorial.net/sqlite-python/
"""


def create_connection(db_file):
    """
    create a database connection to the SQLite database specified by db_file
    :param db_file: database file name
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"DB connected to {db_file}")
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(f"An error occurred connecting to {db_file}: {e}")
        raise e
    return conn


def create_message(conn, msg):
    """
    Insert a new message into the messages table
    :param conn: the DB connection
    :param msg: a dict of the sender ID, recipient ID, and message content
    :return: the ID of the newly created message
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO messages(sender_id,recipient_id,content) "
                "VALUES(?,?,?)",
                (msg["sender_id"], msg["recipient_id"], msg["message"]))
    conn.commit()
    return cur.lastrowid


def create_user(conn, user_name):
    """
    Insert a new user in the users table
    :param conn: the DB connection
    :param user_name: name of the user to be created
    :return: the ID of the newly created user
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name) "
                "VALUES(?)", (user_name, ))
    conn.commit()
    return cur.lastrowid


def _execute_query(conn, sql_statement, params=None):
    """
    Handler for all queries
    :param conn: the DB connection
    :param sql_statement: a SQL statement to execute
    :param params: any parameters needed in the SQL statement
    :return: a list of dicts with the column names and their values of a row
    """
    cur = conn.cursor()
    if not params:
        cur.execute(sql_statement)
    else:
        cur.execute(sql_statement, params)
    rows = cur.fetchall()
    items = [dict(row) for row in rows]
    return items


def get_all_messages(conn):
    """
    Query for all messages
    :param conn: the DB connection
    :return: a list of messages as dicts
    """
    sql_statement = "SELECT * FROM messages"
    messages = _execute_query(conn, sql_statement)
    return messages


def get_all_users(conn):
    """
    Query for all users
    :param conn: the DB connection
    :return: a list of users as dicts
    """
    sql_statement = "SELECT * FROM users"
    users = _execute_query(conn, sql_statement)
    return users


def get_message_by_id(conn, msg_id):
    """
    Query for all messages
    :param conn: the DB connection
    :param msg_id: the ID of a message
    :return: a message as dict
    """
    sql_statement = "SELECT * FROM messages WHERE id=?"
    query_params = (msg_id, )
    messages = _execute_query(conn, sql_statement, query_params)
    return messages[0] if messages else None


def select_messages_by_recipient_and_sender(conn, recipient_name, sender_name):
    """
    Query for messages to a given recipient from a given sender
    :param conn: the DB connection
    :param recipient_name:
    :param sender_name:
    :return:
    """
    sql_statement = ("SELECT * FROM messages "
                     "WHERE recipient_id="
                     "(SELECT id FROM users WHERE name=?) "
                     "AND sender_id="
                     "(SELECT id FROM users WHERE name=?)")
    query_params = (recipient_name, sender_name)
    messages = _execute_query(conn, sql_statement, params=query_params)
    return messages


def select_messages_by_recipient_name(conn, recipient_name):
    """
    Query for messages to a given recipient
    :param conn: the DB connection
    :param recipient_name:
    :return:
    """
    sql_statement = ("SELECT * FROM messages "
                     "WHERE recipient_id="
                     "(SELECT id FROM users WHERE name=?)")
    query_params = (recipient_name, )
    messages = _execute_query(conn, sql_statement, params=query_params)
    return messages


def select_messages_by_sender_name(conn, sender_name):
    """
    Query for messages from a given sender
    :param conn: the DB connection
    :param sender_name:
    :return:
    """
    sql_statement = ("SELECT * FROM messages "
                     "WHERE sender_id="
                     "(SELECT id FROM users WHERE name=?)")
    query_params = (sender_name, )
    messages = _execute_query(conn, sql_statement, params=query_params)
    return messages


def select_user_id_by_name(conn, user_name):
    """
    Query user ID by name
    :param conn: the DB connection
    :param user_name: a users name (str)
    :return: the ID of the user or none
    """
    sql_statement = "SELECT id FROM users WHERE name=?"
    query_params = (user_name, )
    user_ids = _execute_query(conn, sql_statement, params=query_params)
    return user_ids[0] if user_ids else None


def select_user_name_by_id(conn, user_id):
    """
    Query user name by ID
    :param conn: the DB connection
    :param user_id: a user id
    :return: the ID of the user or none
    """
    sql_statement = "SELECT name FROM users WHERE id=?"
    query_params = (user_id, )
    user_ids = _execute_query(conn, sql_statement, params=query_params)
    return user_ids[0] if user_ids else None
