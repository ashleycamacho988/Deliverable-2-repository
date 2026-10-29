# Code for task 1
import re
from pathlib import Path

# The robust file reader function
def read_file(filename: str | Path) -> tuple[str, str]:
    """Reads a log file using UTF-8 or Latin-1 coding"""
    file_path = Path(filename)

    try:
        text = file_path.read_text(encoding="utf-8")
        return text, "utf-8"

    except UnicodeDecodeError:
        text = file_path.read_text(encoding="iso-8859-1")
        return text, "iso-8859-1"