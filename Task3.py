# Code for task 3
import numpy as np

# The removing price outliers function
def clean_prices(prices: list | np.ndarray) -> np.ndarray:
    """Replaces price outliers with the median of the valid prices"""
    prices_array = np.array(prices, dtype=float).flatten()

    mean_price = np.mean(prices_array)
    std_price = np.std(prices_array)

    outliers = np.abs(prices_array - mean_price) > 3 * std_price
    valid_prices = prices_array[~outliers]

    if valid_prices.size > 0:
        median_price = np.median(valid_prices)
        prices_array[outliers] = median_price

    return prices_array