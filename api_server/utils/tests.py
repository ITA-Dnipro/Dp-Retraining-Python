import os


def find_fullpath(filename: str, start_path: str) -> str:
    """Finds full path for a specific filename.

    Args:
        filename: file to find.
        start_path: start location of search.

    Returns:
    full path to a file.
    """
    for root, dirs, files in os.walk(start_path):
        if filename in files:
            return os.path.join(root, filename)
