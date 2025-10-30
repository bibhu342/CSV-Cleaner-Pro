"""
clean_sales_data.py
Author: Bibhudendu Behera
Description:
A lightweight automation script to clean raw sales CSV data using Python + Pandas.
"""

import pandas as pd
from pathlib import Path

# File paths
RAW_PATH = Path("data/raw/sales_dirty.csv")
CLEAN_PATH = Path("data/cleaned/sales_cleaned_final.csv")

def clean_sales_data(input_path=RAW_PATH, output_path=CLEAN_PATH):
    """Reads raw CSV, cleans it, and saves a cleaned version."""

    # Load data
    df = pd.read_csv(input_path)

    # Standardize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Handle missing values
    df["customer_name"] = df["customer_name"].fillna("Unknown")
    df["order_date"] = df["order_date"].fillna("2024-12-31")

    # Normalize text columns
    for col in ["customer_name", "city", "category", "product"]:
        df[col] = df[col].astype(str).str.strip().str.title()

    # Clean numeric columns
    for col in ["unit_price", "sales"]:
        df[col] = (
            df[col].astype(str)
            .str.replace(r"[^0-9.\-]", "", regex=True)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fix sales = quantity × unit_price
    df["sales"] = df["quantity"] * df["unit_price"]

    # Convert dates
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Sort chronologically
    df = df.sort_values("order_date").reset_index(drop=True)

    # Save output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"✅ Cleaned file saved successfully at:\n{output_path.resolve()}")
    print(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")

if __name__ == "__main__":
    clean_sales_data()
