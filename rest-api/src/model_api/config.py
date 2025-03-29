import os

MODEL_PATH = os.getenv('M7_MODEL_PATH')

if MODEL_PATH is None:
    raise RuntimeError("Environmentvariable MODEL_PATH is not set!")
else:
    print(f"Set MODEL_PATH to {MODEL_PATH}")
