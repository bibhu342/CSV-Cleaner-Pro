"""
clean_sales_data.py
Author: Bibhudendu Behera
Description:
Robust cleaner for CSV-Cleaner-Pro with extended header aliases,
including mappings for Diwali dataset headers like:
User_ID, Cust_name, Product_ID, Orders, Amount, age_group, etc.
"""

import pandas as pd
from pathlib import Path
import re
import io

# Default file paths (when running standalone)
RAW_PATH = Path("data/raw/sales_dirty.csv")
CLEAN_PATH = Path("data/cleaned/sales_cleaned_final.csv")


def _read_csv_with_fallback(path):
    """Try multiple encodings and parsing engines; fall back to replacement decode."""
    encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252"]
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            try:
                return pd.read_csv(path, encoding=enc, engine="python", on_bad_lines="skip")
            except Exception:
                continue
    # Final fallback
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8", errors="replace")
    return pd.read_csv(io.StringIO(text))


def _normalize_header(h: str) -> str:
    if h is None:
        return ""
    h = str(h).strip().lower()
    h = re.sub(r"[^\w]+", "_", h)
    h = re.sub(r"_+", "_", h).strip("_")
    return h


def clean_sales_data(input_path=RAW_PATH, output_path=CLEAN_PATH):
    """Reads a raw CSV, cleans it robustly, and writes a cleaned CSV."""

    input_path = Path(input_path)
    df = _read_csv_with_fallback(input_path)

    # Normalize headers (to snake-like tokens)
    df.columns = [_normalize_header(c) for c in df.columns]

    # Extended header map (canonical -> variants)
    header_map = {
        # core customer/id/name mappings
        "customer_id": ["user_id", "user_id", "customer_id", "cust_id", "custid"],
        "customer_name": ["cust_name", "custname", "customer", "customer_name", "client", "name"],
        # dates
        "order_date": [
            "order_date", "orderdate", "date", "invoice_date", "purchase_date", "transaction_date"
        ],
        # quantities / order counts
        "quantity": [
            "quantity", "qty", "orders", "order_count", "qty_ordered", "quantityordered",
            "quantity_ordered", "no_of_items", "units", "item_count", "quantity_purchased"
        ],
        # unit price variants
        "unit_price": [
            "unit_price", "unitprice", "price", "unit_cost", "priceeach", "price_each",
            "price_per_unit", "price_per_item", "selling_price", "mrp", "priceperunit"
        ],
        # total/sales amount variants
        "sales": [
            "sales", "sales_amount", "salesvalue", "total", "amount", "revenue", "total_amount",
            "totalamount", "invoice_amount", "amount_paid", "total_price", "order_amount", "grand_total",
            "amount"  # Diwali uses "Amount"
        ],
        # product & category
        "product": ["product", "product_id", "product_id", "product_name", "item", "sku", "productcode"],
        "category": ["category", "cat", "type", "product_category", "productcategory"],
        # geography / other text fields
        "city": ["city", "town", "region", "state", "location"],
        "marital_status": ["marital_status", "maritalstatus", "marital", "married_status"],
        "age_group": ["age_group", "age_group_1", "agegroup", "age_group1", "age_group.1"],
        "occupation": ["occupation", "job", "profession"],
        "gender": ["gender", "sex"],
        "zone": ["zone", "region_zone", "geozone"],
    }

    # reverse lookup: variant -> canonical
    reverse_map = {v: k for k, vs in header_map.items() for v in vs}

    # rename matching columns
    new_cols = {}
    for c in df.columns:
        if c in reverse_map:
            new_cols[c] = reverse_map[c]
    if new_cols:
        df = df.rename(columns=new_cols)

    # Ensure canonical columns exist
    for col in header_map.keys():
        if col not in df.columns:
            df[col] = pd.NA

    # Basic missing-value handling
    if "customer_name" in df.columns:
        df["customer_name"] = df["customer_name"].fillna("Unknown")
    if "order_date" in df.columns:
        df["order_date"] = df["order_date"].fillna(pd.NA)

    # Safe text normalization (handles Series, DataFrame-like selections)
    text_cols = [
        "customer_id", "customer_name", "product", "city", "category",
        "marital_status", "age_group", "occupation", "gender", "zone"
    ]

    def _normalize_series_like(obj, out_col_prefix=None):
        if isinstance(obj, pd.DataFrame):
            for i in range(obj.shape[1]):
                col_label = obj.columns[i]
                series = obj.iloc[:, i]
                target_name = col_label if isinstance(col_label, (str, int)) else f"{out_col_prefix}_{i}"
                df[target_name] = series.astype(str).str.strip().str.title()
        else:
            df[out_col_prefix] = obj.astype(str).str.strip().str.title()

    for col in text_cols:
        if col in df.columns:
            try:
                series_like = df[col]
                _normalize_series_like(series_like, out_col_prefix=col)
            except Exception:
                for c in df.columns:
                    try:
                        if df[c].dtype == object or pd.api.types.is_string_dtype(df[c]):
                            df[c] = df[c].astype(str).str.strip().str.title()
                    except Exception:
                        df[c] = df[c].astype(str).apply(lambda x: str(x).strip().title())
                break
        else:
            df[col] = pd.NA

    # Numeric cleaning (quantity, unit_price, sales)
    numeric_candidates = ["quantity", "unit_price", "sales", "amount", "orders"]
    for col in numeric_candidates:
        if col in df.columns:
            # remove non-numeric characters (keeps dot and minus)
            df[col] = df[col].astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert quantity-like to nullable integer if possible
    if "quantity" in df.columns:
        try:
            if pd.api.types.is_float_dtype(df["quantity"]):
                non_null = df["quantity"].dropna()
                if len(non_null) > 0 and non_null.apply(float.is_integer).all():
                    df["quantity"] = df["quantity"].astype("Int64")
        except Exception:
            pass

    # Handle cases where 'orders' or 'amount' mapped but canonical names expected are 'quantity'/'sales'
    # If 'orders' exists and canonical 'quantity' is empty, copy it
    if "orders" in df.columns and ("quantity" not in df.columns or df["quantity"].isna().all()):
        df["quantity"] = df["orders"]

    if "amount" in df.columns and ("sales" not in df.columns or df["sales"].isna().all()):
        df["sales"] = df["amount"]

    # Recompute sales from quantity * unit_price if both available
    if {"quantity", "unit_price"}.issubset(df.columns):
        try:
            df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
            df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
            df["sales"] = df["quantity"] * df["unit_price"]
        except Exception:
            def _safe_mul(a, b):
                try:
                    return float(a) * float(b)
                except Exception:
                    return pd.NA
            df["sales"] = [_safe_mul(q, p) for q, p in zip(df["quantity"], df["unit_price"])]

    # Date parsing with simple dayfirst heuristic (DD/MM/YYYY detection)
    if "order_date" in df.columns:
        df["order_date_parsed"] = pd.to_datetime(df["order_date"], errors="coerce", dayfirst=False)
        total_rows = len(df)
        nat_count = df["order_date_parsed"].isna().sum()
        raw_sample = df["order_date"].astype(str).dropna().head(200).astype(str).tolist()
        contains_slash = any("/" in s for s in raw_sample)
        if (total_rows > 0) and (nat_count / max(1, total_rows) > 0.2) and contains_slash:
            df["order_date_parsed"] = pd.to_datetime(df["order_date"], errors="coerce", dayfirst=True)
        df["order_date"] = df["order_date_parsed"]
        df.drop(columns=["order_date_parsed"], inplace=True)

    # Deduplicate and sort (best-effort)
    df.drop_duplicates(inplace=True)
    if "order_date" in df.columns:
        try:
            df = df.sort_values("order_date").reset_index(drop=True)
        except Exception:
            df = df.reset_index(drop=True)

    # Save cleaned CSV
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"✅ Cleaned file saved successfully at:\n{output_path.resolve()}")
    print(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")


if __name__ == "__main__":
    clean_sales_data()
