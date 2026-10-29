# Code for task 2
from pathlib import Path

# The recursive directory search function
def find_files(directory: str | Path) -> list[Path]:
    """Finds all log files in a nested directory"""
    directory_path = Path(directory)
    log_files = []

    for item in directory_path.iterdir():
        if item.is_dir():
            log_files.extend(find_files(item))

        elif item.is_file() and item.suffix == ".log":
            log_files.append(item)

    return log_files