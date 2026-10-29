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

# The log parser function
def log_parser(text: str) -> list[dict]:
    """Extracts valid transactions from log text using regex"""
    pattern = re.compile(
        r"^\[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
        r"\[(?P<register_id>POS_\d+)\] "
        r"item=(?P<item>\w+) "
        r"price=(?P<price>\d+\.\d{2}) "
        r"(?P<currency>EUR|NOK|USD) "
        r"\((?P<status>SUCCESS|REFUND|CANCELLED)\)$"
    )

    transactions = []

    for line in text.splitlines():
        match = pattern.fullmatch(line)

        if match:
           transaction = match.groupdict()
           transaction["price"] = float(transaction["price"])
           transactions.append(transaction)

    return transactions