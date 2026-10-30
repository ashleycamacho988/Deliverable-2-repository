from pathlib import Path
from tkinter import filedialog as fd
import os
import pandas as pd
import numpy as np


def login() -> Path:
    while True:
        filename = fd.askdirectory()

        if "data" in filename:
            if os.path.isdir(f"{filename}/2026/library_cafe") and os.path.isdir(f"{filename}/2026/science_building") and os.path.isdir(f"{filename}/2026/student_union") is True:
                return Path(filename)


def dir_parse(path: Path) -> dict:
    list_dir_1 = os.listdir(path)

    list_dir_2 = []  # list of years
    dict_dir_3 = {}  # lists of places in eah year
    dict_dir_4 = {}  # lists of positions in each place in each year

    for item in list_dir_1:
        if os.path.isdir(Path(f"{path}/{item}")) is True:
            list_dir_2.append(item)

    if len(list_dir_2) > 0:
        for item in list_dir_2:

            dir_3 = os.listdir(Path(f"{path}/{item}"))

            item_3_list = []

            dict_dir_4_sub = {}

            for item_3 in dir_3:
                if os.path.isdir(Path(f"{path}/{item}/{item_3}")) is True:

                    item_3_list.append(item_3)

                dir_4 = os.listdir(Path(f"{path}/{item}/{item_3}"))

                item_4_list = []

                for item_4 in dir_4:
                    if os.path.isdir(Path(f"{path}/{item}/{item_3}/{item_4}")) is True:

                        item_4_list.append(item_4)

                dict_dir_4_sub.update({item_3: item_4_list})

            dict_dir_3.update({item: item_3_list})
            dict_dir_4.update({item: dict_dir_4_sub})

    return dict_dir_4


def lines_to_remove_frame(dir_dict: dict, path: Path) -> pd.DataFrame:

    return_frame = pd.DataFrame(columns=["year", "building", "position", "path", "line_num", "line"])

    for index, key in enumerate(dir_dict):
        for index_2, key_2 in enumerate(dir_dict[key]):
            for index_3, key_3 in enumerate(dir_dict[key][key_2]):
                current_path = Path(f"{path}/{key}/{key_2}/{key_3}")

                if Path(f"{current_path}/register_sales.log").is_file():
                    current_file = Path(f"{current_path}/register_sales.log")

                    try:
                        with open(current_file, "r", encoding="utf=8") as file:
                            for line_index, line in enumerate(file):
                                new_row = pd.DataFrame([{"year": key, "building": key_2, "position": key_3, "path": current_file, "line_num": line_index, "line": line}])

                                return_frame = pd.concat([return_frame, new_row], ignore_index=True)
                    except Exception:
                        with open(current_file, "r", encoding="iso-8859-1") as file:
                            for line_index, line in enumerate(file):
                                new_row = pd.DataFrame([{"year": key, "building": key_2, "position": key_3, "path": current_file, "line_num": line_index, "line": line}])

                                return_frame = pd.concat([return_frame, new_row], ignore_index=True)

    return return_frame


def remove_noise(remove_frame: pd.DataFrame) -> pd.DataFrame:
    remove_frame = remove_frame.drop(remove_frame[remove_frame["line"] == "--- PRINTER PAPER LOW ---\n"].index).reset_index(drop=True)
    remove_frame = remove_frame.drop(remove_frame[remove_frame["line"] == "=== NETWORK SYNC OK ===\n"].index).reset_index(drop=True)
    remove_frame = remove_frame.drop(remove_frame[remove_frame["line"] == "[DEBUG] BARCODE SCANNER REBOOTED\n"].index).reset_index(drop=True)

    return remove_frame


def split_line(split_frame: pd.DataFrame) -> pd.DataFrame:
    split_frame[["timestamp", "timestamp_h", "register_id", "item", "price", "currency", "status"]] = split_frame["line"].str.split(" ", expand=True)
    split_frame["timestamp"] = split_frame["timestamp"].str.replace("[", "", regex=False)
    split_frame["timestamp_h"] = split_frame["timestamp_h"].str.replace("]", "", regex=False)
    split_frame["timestamp"] = split_frame["timestamp"] + " " + split_frame["timestamp_h"]
    split_frame["register_id"] = split_frame["register_id"].str.replace("[", "", regex=False)
    split_frame["register_id"] = split_frame["register_id"].str.replace("]", "", regex=False)
    split_frame["item"] = split_frame["item"].str.replace("item=", "", regex=False)
    split_frame["price"] = split_frame["price"].str.replace("price=", "", regex=False)
    split_frame["status"] = split_frame["status"].str.replace("(", "", regex=False)
    split_frame["status"] = split_frame["status"].str.replace(")\n", "", regex=False)
    split_frame["price"] = pd.to_numeric(split_frame["price"], errors="coerce")
    split_frame["price"] = split_frame["price"].to_numpy(dtype=np.float64)
    split_frame = split_frame.drop(columns=["line", "timestamp_h"])

    return split_frame


def remove_deviation(dev_frame: pd.DataFrame) -> pd.DataFrame:
    dev_frame.loc[dev_frame["price"] >= ((dev_frame["price"].std())*3), "price"] = dev_frame["price"].median()

    dev_frame["original_price"] = dev_frame["price"]

    dev_frame.loc[dev_frame["currency"] == "NOK", "price"] = dev_frame["price"] * 10

    return dev_frame


def refund_fun(refund_frame: pd.DataFrame) -> float:
    count_sales = (refund_frame["status"] == "SUCCESS").sum()
    count_refund = (refund_frame["status"] == "REFUND").sum()

    refund_ratio = count_refund/(count_sales + 10**(-6))

    return refund_ratio


def print_file(print_frame: pd.DataFrame) -> None:
    print_frame[["timestamp", "register_id", "item", "price", "currency", "status"]].to_csv("cleaned_transaction.csv", sep=",", index=False, encoding='utf-8')

    print_frame.groupby(["item", "status"])["original_price"].sum().to_csv("status_pivot_table.csv", sep=",", index=False, encoding='utf-8')

    item_list = (print_frame.groupby(["item"])["original_price"].sum())

    print(item_list["item"])

path = login()
df = lines_to_remove_frame(dir_parse(path), path)

df = remove_noise(df)

df = split_line(df)

df = remove_deviation(df)

# task 1
print(df[["timestamp", "register_id", "item", "price", "currency", "status"]])

# task 2
print(df["path"])

# task 3
print(f"Refund ration: {refund_fun(df)} refunds for every sale.")

print_file(df)
