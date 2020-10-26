from pathlib import Path


def get() -> Path:
    """
    Get path of root project structure.

    :return: A Path object with the absolute project root path.
    """
    return Path(__file__).parent.parent.parent
