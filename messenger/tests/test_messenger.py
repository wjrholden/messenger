import json
import random

import requests
from randomwordgenerator import randomwordgenerator as rwg

BASE_URL = "http://localhost:8000/messages"
RANDOM_WORDS = rwg.generate_random_words(1000000)


def test_messenger_apis():
    """
    tests the messenger app create and get single message functionality
    """
    for i in range(12):
        # create a test message through the API
        test_message = _generate_test_message()
        print(f"creating test message = {test_message}")
        create = requests.post(BASE_URL, data=json.dumps(test_message))
        assert create.status_code == 201

        # get the created message and verify field matches
        message_location = create.headers['location']
        retrieve = requests.get(f"{BASE_URL}{message_location}")
        assert retrieve.status_code == 200
        returned_message = retrieve.json()
        assert returned_message['message'] == test_message['message']
        assert returned_message['sender'] == test_message['sender']
        assert returned_message['recipient'] == test_message['recipient']


def test_messenger_limit():
    pass


def _generate_test_message():
    sender = _get_random_user()
    recipient = _get_random_user()
    while recipient == sender:
        recipient = _get_random_user()
    message = {
        "sender": sender,
        "recipient": recipient,
        "message": ' '.join([random.choice(RANDOM_WORDS) \
                             for i in range(random.choice(range(8, 12)))])
    }
    return message


def _get_random_user():
    users = [
        'Roberto', 'Felipe', 'John', 'Chad', 'Chris', 'Mike', 'Jason',
        'Vince', 'Eric', 'Zack', 'Dustin', 'Dan', 'Mitch', 'Emily', 'Emma',
        'Amanda', 'Naomi', 'Kristen', 'Anna', 'Jenna', 'Dana', 'Julia',
        'Stacy', 'Allie', 'Martha', 'Joanne'
    ]
    return random.choice(users)
