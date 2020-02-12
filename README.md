# Simple Messenger API exercise

An API for sending short text messages between individual users

## Setup (for Mac OSX):
### Prerequisites:
1. Xcode Command Line Tools installed: `$ xcode-select --install`
2. Homebrew installed: https://brew.sh/
3. Python 3 installed: `$ brew install python3`
4. SQLite installed
    * should be part of the Python 3 install but if not: `$ brew install sqlite`
5. Git installed 
    * should be part of the Xcode Command Line Tools but if not: `$ brew install git`

### Messenger app setup:
1. Clone the `messenger` repo from [GitHub](https://github.com/wjrholden/messenger): 
    * `$ git clone https://github.com/wjrholden/messenger.git` 
2. CD into the project directory:
    * `$ cd messenger/`
3. Create a Python virtual environment in the root project directory:
    * `$ python3 -m venv .venv`
4. Activate the Python virtual environment:
    * `$ source .venv/bin/activate`
5. Install Python dependencies in the virtual environment:
    * `$ pip install -r requirements.txt`
    * __NOTE:__ if an error occurs installing `pypandoc`, install manually to resolve with `$ pip install pypandoc`, then re-run `$ pip install -r requirements.txt` to complete installation of the remaining dependencies
6. CD into the messenger app directory:
    * `$ cd /messenger`
7. Start the messenger app server with Gunicorn:
    * `$ gunicorn messenger_app:app`
8. In a new terminal window/tab, send a test curl to the messages API:
    * `$ curl "127.0.0.1:8000/messages?limit=5"`
9. (Optional) Run the PyTest API tests:
    * Activate the Python virtual environment in the new terminal session from the base project directory, see #4 ^
    * __NOTE:__ The test SQLite database comes pre-populated with test users and messages and the below PyTest command will create additional new entries in said DB
    * `$ pytest -v`

## Invoking and exercising the Messenger APIs:
* Complete OpenAPI/Swagger v2 specification can be found in `api.yml` in the base project directory

### API usage examples:
__NOTE:__ Using [Postman](https://www.postman.com/downloads/) is highly recommended for convenience and readability of API responses

* Retrieving all test messages in database:
    * Using Postman: 
        1. Open a new request tab and set HTTP method to GET
        2. Enter `127.0.0.1:8000/messages` into URL bar
        3. Hit the `Send` button, "pretty" JSON response will appear in `Body` response section containing all test messages in the database
    * Using curl: `$ curl "127.0.0.1:8000/messages"`
        * Postman is recommended because it will "pretty-ify" the JSON response body

* Creating a new message (using Postman):
    1. Open a new request tab
    2. Set HTTP method to POST and set URL to `127.0.0.1:8000/messages`
    3. In the `Body` section directly below the address bar, using the "raw" setting (radio button), set the input type (far right dropdown) to `JSON`
    4. Copy and paste the below `JSON` snippet into the `Body` input and replace the `{user}`/`{message}` parameters with names and a message of your choice
    ```javascript
    {
        "sender": "{user}",
        "recipient": "{user}",
        "message": "{message}"
    }
    ```
    5. Hit the `Send` button, the provided message input will be returned in the response `Body` section with a `201 Created` status code and a `location` header with a relative URI containing an ID for retrieving the created message
    6. Retrieve the created message at the following parameterized URL
        * `127.0.0.1:8000/messages/{message_id}`

* Retrieving messages from a specific sender to a specific recipient:
    * The following two query parameters must BOTH be supplied to retrieve messages from a given sender to a given recipient:
        * `sender={user}` and `recipient={user}`, 
        * e.g. `127.0.0.1:8000/messages?sender={user}&recipient={user}`

* Additional query parameters and their usage:
    * The `limit` query parameter will return a limited count of the `{int}` most recent messages 
        * `limit={int}`
        * e.g. `127.0.0.1:8000/messages?limit=25`
    * The `range` query parameter will return messages from the last `{int}` number of days
        * `range={int}d` or `range={int}` 
        * e.g. `127.0.0.1:8000/messages?range=5d`

## Resources referenced:
### Documentation - 
* https://swagger.io/docs/specification/2-0/
* https://docs.python.org/3.7/
* https://www.sqlitetutorial.net/sqlite-python/
* https://falcon.readthedocs.io/en/stable/user/quickstart.html
* https://realpython.com/absolute-vs-relative-python-imports/
* https://docs.pytest.org/en/latest/getting-started.html
* https://requests.readthedocs.io/en/master/
* https://pypi.org/project/randomwordgenerator/
