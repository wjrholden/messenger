import json
from datetime import datetime, timedelta

import falcon

from db import db


"""
created with guidance from the Falcon quickstart guide:
https://falcon.readthedocs.io/en/stable/user/quickstart.html
"""
class MessengerResource():

    def __init__(self, db_conn):
        """
        On Falcon startup, create connection to local database
        """
        self.db_conn = db_conn

    def on_get(self, req, resp, message_id=None):
        """
        HTTP GET request handler
        :param req: the Falcon request object
        :param resp: the Falcon response object
        :param message_id: optional, an ID of a message
        :return: a status code and message body
        """
        enable_message_limit = 'limit' in req.params
        enable_message_range = 'range' in req.params
        is_single_message_stream = 'sender' in req.params \
                                   and 'recipient' in req.params
        invalidate_no_sender = 'recipient' in req.params \
                               and 'sender' not in req.params
        invalidate_no_recipient = 'sender' in req.params \
                                  and 'recipient' not in req.params

        # if sender sent without recipient or recipient without sender, invalid
        if invalidate_no_recipient or invalidate_no_sender:
            resp.body = json.dumps({
                "message": "sender AND recipient are required parameters"})
            resp.status = falcon.HTTP_400

        # request for a specific message by it's ID
        if message_id:
            print(f"request received for message with ID: {message_id}")
            message = db.get_message_by_id(self.db_conn, message_id)
            if message:
                print(f"message found by ID: {message_id}\n{message}")
                resp.body = json.dumps(
                    self._format_message(self.db_conn, message))
            else:
                print(f"no messages found with ID: {message_id}")
                resp.body = json.dumps({
                    "error": f"no messages found with ID: {message_id}"})
                resp.status = falcon.HTTP_404

        # no sender OR recipient query params --> get all messages
        elif not is_single_message_stream:
            print("retrieving all messages")
            messages = db.get_all_messages(self.db_conn)
            if enable_message_limit:
                limit = int(req.params['limit'])
                print(f"limiting messages to {limit} most recent")
                messages = messages[-limit:]
            if enable_message_range:
                messages = self._filter_messages_by_range(
                    messages, req.params['range'])
            resp.body = json.dumps([
                self._format_message(self.db_conn, msg) for msg in messages])
            if not messages:
                resp.status = falcon.HTTP_404
                resp.body = json.dumps({"error": "no messages in DB"})

        # fall-through case is sender AND recipient params sent
        else:
            print("retrieving message stream for "\
                  f"sender[{req.params['sender']}] and "\
                  f"recipient[{req.params['recipient']}]")
            messages = db.select_messages_by_recipient_and_sender(
                self.db_conn, req.params['recipient'], req.params['sender'])
            if enable_message_limit:
                limit = int(req.params['limit'])
                print(f"limiting messages to {limit} most recent")
                messages = messages[-limit:]
            if enable_message_range:
                messages = self._filter_messages_by_range(
                    messages, req.params['range'])
            resp.body = json.dumps([
                self._format_message(self.db_conn, msg) for msg in messages
            ])

    def on_post(self, req, resp):
        """
        HTTP POST request handler
        :param req: the Falcon request object
        :param resp: the Falcon response object
        :return: a status code and message location header
        """
        message = req.media
        print(f"creating new message: {message}")
        new_db_entry = {"message": message["message"]}

        sender_db_entry = db.select_user_id_by_name(
            self.db_conn, message['sender'])
        sender_id = sender_db_entry['id'] if sender_db_entry is not None else 0
        recipient_db_entry = db.select_user_id_by_name(
            self.db_conn, message['recipient'])
        recipient_id = recipient_db_entry['id'] \
            if recipient_db_entry is not None else 0

        # if sender or recipient haven't been users before, add them
        if not sender_id:
            sender_id = db.create_user(self.db_conn, message['sender'])
        if not recipient_id:
            recipient_id = db.create_user(self.db_conn, message['recipient'])

        new_db_entry["sender_id"] = sender_id
        new_db_entry["recipient_id"] = recipient_id

        message_id = db.create_message(self.db_conn, new_db_entry)
        print(f"message created successfully with ID: {message_id}")
        resp.location = f"/{message_id}"
        resp.body = json.dumps(message)
        resp.status = falcon.HTTP_201

    @staticmethod
    def _format_message(db_conn, message):
        """
        converts the message dict and populates user names
        :param db_conn: the DB connection
        :param message: a message row from the DB
        """
        return {
            "sender": db.select_user_name_by_id(
                db_conn, message['sender_id'])['name'],
            "recipient": db.select_user_name_by_id(
                db_conn, message['recipient_id'])['name'],
            "message": message['content'],
            "message_date": message['creation_date']
        }

    @staticmethod
    def _filter_messages_by_range(messages, message_range):
        """
        Removes messages older than the provided range day
        :param messages: an array of messages
        :param message_range: a str indicating a day range
        """
        day_range = int(message_range.replace('d', ''))
        print(f"filtering messages older than {day_range} days old")
        oldest_date = datetime.today() - timedelta(days=day_range)
        for index, message in enumerate(messages):
            message_date = datetime.fromisoformat(message['creation_date'])
            if message_date < oldest_date:
                messages.pop(index)
        return messages


database_file = "messenger.db"
messenger = MessengerResource(db.create_connection(database_file))

app = falcon.API()
app.add_route('/messages', messenger)
app.add_route('/messages/{message_id}', messenger)
