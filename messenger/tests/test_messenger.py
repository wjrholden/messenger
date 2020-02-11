import random

import requests
from randomwordgenerator import randomwordgenerator as rwg

BASE_URL = "http://localhost:8000/messages"
RANDOM_WORDS = rwg.generate_random_words(1000000)


def test_messenger_apis():
    for i in range(12):
        message = _generate_test_message()
        print(f"message = {message}")
    assert False


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
