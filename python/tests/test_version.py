import tomllib
from pathlib import Path

import spancheck


def test_version_matches_pyproject():
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    assert spancheck.__version__ == pyproject["project"]["version"]
