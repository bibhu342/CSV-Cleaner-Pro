from __future__ import annotations
import re
import pandas as pd

def _clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=lambda c: re.sub(r"\s+", "_", c.strip().lower()))
    return df

def _strip_object_cols(df: pd.DataFrame) -> pd.DataFrame:
    obj_cols = df.select_dtypes(include=["object"]).columns
    for c in obj_cols:
        df[c] = df[c].astype(str).str.strip()
        df[c] = df[c].str.replace(r"\s+", " ", regex=True)
    return df

def _titlecase_if_present(df: pd.DataFrame, cols=("customer_name","city")) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().str.title()
    return df

def _parse_dates(df: pd.DataFrame, cols=("order_date",)) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce", utc=False)
    return df

def _to_numeric(df: pd.DataFrame, col: str) -> pd.Series:
    s = df[col].astype(str)
    s = s.str.replace(r"[^\d\.\-]", "", regex=True)
    return pd.to_numeric(s, errors="coerce")

def _ensure_numeric(df: pd.DataFrame) -> pd.DataFrame:
    for c in ("quantity","unit_price","price","amount","sales"):
        if c in df.columns:
            df[c] = _to_numeric(df, c)
    return df

def _compute_sales(df: pd.DataFrame) -> pd.DataFrame:
    q_col = next((c for c in ("quantity","qty") if c in df.columns), None)
    p_col = next((c for c in ("unit_price","price","unitprice") if c in df.columns), None)
    if q_col and p_col:
        computed = df[q_col].fillna(0) * df[p_col].fillna(0)
        if "sales" in df.columns:
            df["sales"] = df["sales"].fillna(computed)
        else:
            df["sales"] = computed
    return df

def _drop_full_empty_cols(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(axis=1, how="all")

def _dedupe(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(ignore_index=True)

def clean_sales_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _clean_column_names(df)
    df = _strip_object_cols(df)
    df = _titlecase_if_present(df, cols=("customer_name","city","category","product"))
    df = _parse_dates(df, cols=("order_date",))
    df = _ensure_numeric(df)
    df = _compute_sales(df)
    df = _drop_full_empty_cols(df)
    df = _dedupe(df)
    return df
