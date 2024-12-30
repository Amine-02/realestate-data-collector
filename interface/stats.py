from dataclasses import dataclass

@dataclass
class Stats:
    date: str           # e.g. "2024-12-31"
    count: int          # Number of listings
    average_price: float  # Formatted string
    median_price: int   # Formatted string
    min_price: int      # Formatted string
    max_price: int      # Formatted string
    std_dev_price: float  # Raw float for standard deviation
