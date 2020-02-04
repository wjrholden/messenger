import json

import falcon

"""
created with guidance from the Falcon quickstart guide:
https://falcon.readthedocs.io/en/stable/user/quickstart.html
"""


class MessengerResource(object):

    def on_get(self, req, resp):
        resp.body(json.dumps({
            "message": "GET request received!"
        }))

    def on_post(self, req, resp):
        resp.body(json.dumps({
            "message": "POST request received!"
        }))


app = falcon.API()
messenger = MessengerResource()
app.add_route('/messages', messenger)
