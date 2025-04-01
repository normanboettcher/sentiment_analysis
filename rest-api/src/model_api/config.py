import os

MODEL_PATH = os.getenv("M7_MODEL_PATH")
LOOKUP_TABLE_PATH = os.getenv("LOOKUP_TABLE_PATH")
VOCAB_SIZE = os.getenv("MODEL_VOCAB_SIZE")
NUM_OOV_BUCKETS = os.getenv("MODEL_NUM_OOV_BUCKETS")


def env_var_not_set(var):
    return f"Environmentvariable {var} is not set!"


def load_config():
    if VOCAB_SIZE is None:
        raise RuntimeError(env_var_not_set("MODEL_VOCAB_SIZE"))
    else:
        print(f"Set VOCAB_SIZE to {VOCAB_SIZE}")

    if NUM_OOV_BUCKETS is None:
        raise RuntimeError(env_var_not_set("MODEL_NUM_OOV_BUCKETS"))
    else:
        print(f"Set MODEL_NUM_OOV_BUCKETS to {NUM_OOV_BUCKETS}")

    if LOOKUP_TABLE_PATH is None:
        raise RuntimeError(env_var_not_set("LOOKUP_TABLE_PATH"))
    else:
        print(f"Set LOOKUP_TABLE_PATH to {LOOKUP_TABLE_PATH}")

    if MODEL_PATH is None:
        raise RuntimeError(env_var_not_set("MODEL_PATH"))
    else:
        print(f"Set MODEL_PATH to {MODEL_PATH}")

    return {
        "MODEL_PATH": MODEL_PATH,
        "LOOKUP_TABLE_PATH": LOOKUP_TABLE_PATH,
        "VOCAB_SIZE": VOCAB_SIZE,
        "NUM_OOV_BUCKETS": NUM_OOV_BUCKETS,
    }
