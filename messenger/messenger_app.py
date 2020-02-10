import json

import falcon

from db import db


"""
created with guidance from the Falcon quickstart guide:
https://falcon.readthedocs.io/en/stable/user/quickstart.html
"""
class MessengerResource():

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def on_get(self, req, resp, message_id=None):
        """
        HTTP GET request handler
        :param req: the Falcon request object
        :param resp: the Falcon response object
        :param message_id: optional, an ID of a message
        :return: a status code and message body
        """
        if message_id:
            print(f"request received for message with ID: {message_id}")
            message = db.get_message_by_id(self.db_conn, message_id)
            if message:
                print(f"message found by ID: {message_id}\n{message}")
                resp.body = json.dumps(
                    self._format_message(self.db_conn, message))
            else:
                print(f"no messages found with ID: {message_id}")
                resp.status = falcon.HTTP_404
                resp.body = json.dumps({
                    "error": f"no messages found with ID: {message_id}"})
        elif not req.params:
            print("no query params requested, retrieving all messages")
            messages = db.get_all_messages(self.db_conn)
            resp.body = json.dumps([
                self._format_message(self.db_conn, msg) for msg in messages
            ])
        else:
            print(f"query params = {req.params}")

    def on_post(self, req, resp):
        """
        HTTP POST request handler
        :param req: the Falcon request object
        :param resp: the Falcon response object
        :return: a status code and message location header
        """
        resp.body = json.dumps({
            "message": "POST request received!"
        })

    @staticmethod
    def _format_message(db_conn, message):
        """
        converts the message dict and populates user names
        :param message: a message row from the DB
        """
        return {
            "sender": db.select_user_name_by_id(
                db_conn, message['sender_id'])['name'],
            "recipient": db.select_user_name_by_id(
                db_conn, message['recipient_id'])['name'],
            "content": message['content'],
            "message_date": message['creation_date']
        }


database_file = "messenger.db"
messenger = MessengerResource(db.create_connection(database_file))

app = falcon.API()
app.add_route('/messages', messenger)
app.add_route('/messages/{message_id}', messenger)
