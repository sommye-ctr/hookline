from django.utils.crypto import get_random_string
import environ

env = environ.Env()

def generate_token():
    return get_random_string(
        int(env('WEBHOOK_TOKEN_LENGTH')),
        allowed_chars=env('WEBHOOK_TOKEN_CHARACTERS')
    )