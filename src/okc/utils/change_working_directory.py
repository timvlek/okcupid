import sys

def change_working_directory() -> None:
    """
    Change the current working directory to the script's directory.
    Ensures this function can only be executed once.
    """
    global _cwd_executed

    if _cwd_executed:
        return
    else:
        sys.path.append("..")
        _cwd_executed = True