import os


def get_real_path(relative_path: str, relative_path_start: str = __file__) -> str:
    """
    Gets the absolute path without symlinks for the specified relative path.
    The start of the relative path (unless specified otherwise) is the root directory of the project
    Args:
        relative_path: relative path to convert
        relative_path_start: directory to use as the starting point of the relative path

    Returns:
        Absolute path for the specified relative path as string.
    """
    if relative_path is not None and len(relative_path) > 0:
        if relative_path[0] != '/':
            relative_path = '/' + relative_path

    return f"{os.path.realpath(os.path.dirname(relative_path_start))}{relative_path}"
