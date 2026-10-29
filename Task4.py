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

# The hourly revenue function
def hourly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates the total revenue per item by the hour"""
    hourly = df.groupby("item").resample("1h")["price"].sum()

    hourly = hourly.reset_index()
    return hourly 

# The status pivot table function
def create_pivot_table(df: pd.DataFrame) -> pd.DataFrame:
    """Creates a pivot table by item across status categories"""
    pivot_table = pd.pivot_table(df, values="price", index="item", columns="status", aggfunc="sum", fill_value=0)
    return pivot_table