import argparse
from pathlib import Path
import sys
import pandas as pd
from .core import clean_sales_dataframe

def main():
    p = argparse.ArgumentParser(prog="csv-cleaner", description="Clean, validate, and standardize messy sales CSVs.")
    p.add_argument("--input", required=True, help="Path to input CSV")
    p.add_argument("--output", required=True, help="Path to write cleaned CSV")
    args = p.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    if not in_path.exists():
        print(f"ERROR: Input file not found: {in_path}", file=sys.stderr)
        return 2

    df = pd.read_csv(in_path, low_memory=False)
    cleaned = clean_sales_dataframe(df)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(out_path, index=False)
    print(f"✅ Cleaned CSV written to: {out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
