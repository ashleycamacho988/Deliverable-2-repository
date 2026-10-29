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

# The recursive active register search function
def find_active_registers(data: dict | list) -> set[str]:
    """Finds all active register IDs in nested dictionaries and lists"""
    active_registers = set()

    if isinstance(data, dict):
        if data.get("active") is True and "id" in data:
            active_registers.add(data["id"])

        for value in data.values():
            if isinstance(value, (dict, list)):
                active_registers.update(find_active_registers(value))

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                active_registers.update(find_active_registers(item))

    return active_registers