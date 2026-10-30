# Code for task 5
import json
from pathlib import Path

import numpy as np
import pandas as pd

def main() -> None:
    """Processes transaction logs and generates resampled reports, pivot tables and refund ratios"""
    data_path = Path("data")

    with open(data_path / "store_config.json", encoding="utf-8") as file:
        config = json.load(file)

    active_registers = find_active_registers(config)
    log_files = find_files(data_path)

    transactions = []

    for log_file in log_files:
        text, _ = read_file(log_file)
        records = log_parser(text)

        for record in records:
            if record["register_id"] in active_registers:
                transactions.append(record)

    df = create_dataframe(transactions)

    df["price"] = clean_prices(df["price"].to_numpy())

    correct_prices = df["currency"] == "NOK"
    df.loc[correct_prices, "price"] *= 10.0

    hourly = hourly_revenue(df)
    pivot_table = create_pivot_table(df)
    refund_ratios = item_refund_ratios(df)

    df.to_csv("cleaned_transactions.csv")
    hourly.to_json("hourly_revenue.json", orient="records", date_format="iso", indent=2)
    pivot_table.to_csv("status_pivot_table.csv")
    refund_ratios.to_csv("item_refund_ratios.csv", index=False)

    print("Number of log files:", len(log_files))
    print("Number of transactions:", len(df))
    print("Active registers:", sorted(active_registers))

main()