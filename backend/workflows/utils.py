import json
import os
import sys
import traceback

from django.conf import settings
from django.utils.crypto import get_random_string
import environ
import importlib

env = environ.Env()


def generate_webhook_token():
    return get_random_string(
        int(env('WEBHOOK_TOKEN_LENGTH')),
        allowed_chars=env('WEBHOOK_TOKEN_CHARACTERS')
    )


def get_nested_value(data: dict, dotted_path: str, default=None):
    keys = dotted_path.split(".")
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data


def extract_event_type(payload, platform):
    if platform == 'Trello':
        return f"{payload.get('action', {}).get('type')}"
    elif platform == 'Clickup':
        return f"{payload.get('event')}"
    else:
        raise ValueError(f"Unknown platform: {platform}")


def get_error_dict(e: Exception, **kwargs):
    return {
        "message": kwargs.get("message", None),
        "error": f"{type(e).__name__}: {str(e)}",
        "traceback": traceback.format_exc()
    }


def load_json_file(path):
    file = os.path.join(settings.BASE_DIR, path)
    if not os.path.exists(file):
        raise FileNotFoundError()

    with open(file, 'r') as f:
        data = json.load(f)
    return data


def load_action_plugin(slug: str) -> callable:
    some_dir = os.path.join(settings.BASE_DIR, 'plugins', slug)

    if not os.path.exists(some_dir):
        raise FileNotFoundError("Plugin could not be found")
    if not os.path.isdir(some_dir):
        raise NotADirectoryError("The plugin doesnt have correct configuration")

    execution_file = os.path.join(some_dir, 'execution.py')
    if not os.path.exists(execution_file):
        raise FileNotFoundError("The execution.py was not found for the plugin")

    sys.path.append(some_dir)

    try:
        module = importlib.import_module("execution")

        if not hasattr(module, "create_plugin") or not callable(module.create_plugin):
            raise AttributeError("Plugin doesnt have create_plugin function")

        return module.create_plugin
    except ImportError:
        raise ImportError("Unable to import the plugin")
    finally:
        if some_dir in sys.path:
            sys.path.remove(some_dir)
