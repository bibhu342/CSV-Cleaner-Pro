# scripts/cli.py
import argparse
from scripts.clean_sales_data import clean_sales_data

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-i","--input", default="data/raw/sales_dirty.csv")
    p.add_argument("-o","--output", default="data/cleaned/sales_cleaned_final.csv")
    args = p.parse_args()
    clean_sales_data(input_path=args.input, output_path=args.output)
if __name__=="__main__":
    main()

