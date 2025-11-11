import pandas as pd
from csv_cleaner.core import clean_sales_dataframe

def test_smoke_clean_sales_dataframe():
    df = pd.DataFrame({
        "customer_name": ["  alice ", None],
        "order_date": ["2025-01-01", "bad-date"],
        "quantity": [2, 3],
        "unit_price": ["$10.00", "15"],
        "sales": [None, None],
        "city": [" mumbai", "Bangalore"],
        "category": [" gadgets", "Home "],
        "product": ["usb", "fan"]
    })
    out = clean_sales_dataframe(df)
    # no fully-empty columns
    assert out.dropna(axis=1, how='all').shape[1] == out.shape[1]
    # customer_name cleaned and titlecased
    assert any("Alice" in str(x) for x in out["customer_name"].tolist())
    # sales computed where possible
    assert "sales" in out.columns
    assert out["sales"].notna().any()
