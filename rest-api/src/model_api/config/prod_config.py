import os

from flask import current_app


def env_var_not_set(var):
    return f"Environmentvariable {var} is not set!"


class ProdConfig:
    MODEL_PATH = os.getenv("M7_MODEL_PATH")
    LOOKUP_TABLE_PATH = os.getenv("LOOKUP_TABLE_PATH")
    FRONTEND_HOST_URL = os.getenv('FRONTEND_HOST_URL', 'localhost')
    FRONTEND_PORT = os.getenv('FRONTEND_PORT', '5000')

    if LOOKUP_TABLE_PATH is None:
        raise RuntimeError(env_var_not_set("LOOKUP_TABLE_PATH"))
    else:
        print(f"Set LOOKUP_TABLE_PATH to {LOOKUP_TABLE_PATH}")

    if MODEL_PATH is None:
        raise RuntimeError(env_var_not_set("MODEL_PATH"))
    else:
        print(f"Set MODEL_PATH to {MODEL_PATH}")
