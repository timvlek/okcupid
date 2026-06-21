import os
from pathlib import Path

# Define state variable for use in change_working_directory()
_cwd_executed = False

def change_working_directory() -> None:
    """
    Changes the current working directory to the script's directory.
    Ensures this function can only be executed once.
    """
    global _cwd_executed

    if not _cwd_executed:
        script_dir = Path(__file__).parent.resolve()
        os.chdir(script_dir)
        _cwd_executed = True