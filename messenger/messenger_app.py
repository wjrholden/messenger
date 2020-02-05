import json

import falcon

from db import db
# (create_connection,
#                    create_message,
#                    create_user, 
#                    get_all_messages,
#                    select_messages_by_recipient_and_sender,
#                    select_user_id_by_name)


"""
created with guidance from the Falcon quickstart guide:
https://falcon.readthedocs.io/en/stable/user/quickstart.html
"""
class MessengerResource():

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def on_get(self, req, resp):
        resp.body = json.dumps({
            "message": "GET request received!"
        })

    def on_post(self, req, resp):
        resp.body = json.dumps({
            "message": "POST request received!"
        })


database_file = "messenger.db"
messenger = MessengerResource(db.create_connection(database_file))

app = falcon.API()
app.add_route('/messages', messenger)
