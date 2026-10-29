# Code for task 4
import pandas as pd

# The DataFrame creation function
def create_dataframe(transactions: list[dict]) -> pd.DataFrame:
    """Converts the list of transaction dictionaries into a DataFrame"""
    df = pd.DataFrame(transactions)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")
    df = df.sort_index()

    return df