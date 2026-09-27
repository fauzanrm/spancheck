from importlib.metadata import version
from spancheck.text import normalize

__version__ = version("spancheck")

def hello() -> str:
    return "Hello from spancheck!"
