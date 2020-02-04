import json

import falcon


class MessengerResource(object):

    def on_get(self, req, resp):
        resp.body(json.dumps{
            "message": "GET request received!"
        })

    def on_post(self, req, resp):
        resp.body(json.dumps{
            "message": "POST request received!"
        })


app = falcon.API()
messenger = MessengerResource()
app.add_route('/messages', messenger)
