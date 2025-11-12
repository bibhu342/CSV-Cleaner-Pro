![CSV Cleaner Pro Banner](banner.png)

# 🧹 CSV-Cleaner-Pro 🚀  
**Instantly clean, validate, and standardize messy CSV sales data.**  
*Automated Python & Streamlit tool for analysts, teams, and freelancers.*

[![CI](https://github.com/bibhu342/CSV-Cleaner-Pro/actions/workflows/ci.yml/badge.svg)](https://github.com/bibhu342/CSV-Cleaner-Pro/actions)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://csv-cleaner-pro-bibhu342.streamlit.app)

> 💻 **Live Demo:** [Streamlit Cloud](https://csv-cleaner-pro-bibhu342.streamlit.app) — Upload any CSV & get a cleaned export instantly!

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-green?logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![GitHub last commit](https://img.shields.io/github/last-commit/bibhu342/CSV-Cleaner-Pro)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## ⚡ Quickstart

### CLI Usage

```bash
python scripts/cli.py -i data/raw/sales_dirty.csv -o data/cleaned/sales_cleaned_final.csv
```

### Run as Streamlit App

```bash
streamlit run scripts/app.py
# Then open http://localhost:8501
```

---

## 🎬 Screenshots & Demo

### Before → After

| Raw CSV | Cleaned Output |
| ------- | -------------- |
| ![Before](assets/demo_clean_1.png) | ![After](assets/demo_clean_3.png) |

### Processing Showcase

<p align="center">
  <img src="assets/demo_showcase.gif" alt="CSV Cleaner Pro Demo" width="800" />
</p>

👉 **Try It Online:**  
[Streamlit Demo](https://csv-cleaner-pro-qy34r3dkdap9d327sn375l.streamlit.app/)

---

## 💡 Why CSV-Cleaner-Pro?

Sales CSVs are often ugly:
- Inconsistent columns
- Mixed date and currency formats
- Duplicates, missing values
- Cleaning by hand = time drain

**CSV-Cleaner-Pro**: Python & Pandas automation for fully analysis-ready data with a single click.

---

## 🛠️ Tech Stack

| Category    | Tools                                    |
| ----------- | ---------------------------------------- |
| Language    | Python 3.11                              |
| Framework   | [Streamlit](https://streamlit.io)        |
| Libraries   | Pandas, NumPy, Pathlib                   |
| Environment | VS Code, GitHub, Streamlit Cloud         |

---

## 🎯 Core Features

- **End-to-end CSV Cleaning:** Structure fixes, missing value fills, business logic validation, duplicate removal
- **Business Validation:** `sales = quantity × unit_price` enforced automatically
- **Multi-Encoding Support:** Handles UTF-8, latin1, cp1252, etc.
- **Preview & Export:** Shows stats, missing summary; download output
- **Fast:** Instant results via CLI or Streamlit web UI

---

## 🧩 Cleaning Pipeline

1. **Inspection**: `df.info()` and missing value checks
2. **Missing Values**
   ```python
   df['customer_name'] = df['customer_name'].fillna("Unknown")
   df['order_date'] = df['order_date'].fillna("2024-12-31")
   ```
3. **Text Normalization**
   ```python
   for col in ['customer_name', 'city', 'category', 'product']:
       df[col] = df[col].astype(str).str.strip().str.title()
   ```
4. **Numeric Cleaning**
   ```python
   for col in ['unit_price', 'sales']:
       df[col] = df[col].astype(str).str.replace(r'[^0-9.\-]', '', regex=True)
       df[col] = pd.to_numeric(df[col], errors='coerce')
   ```
5. **Business Logic**
   ```python
   df['sales'] = df['quantity'] * df['unit_price']
   ```
6. **Date Cleaning**
   ```python
   df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
   ```
7. **Deduplication & Export**: Remove duplicates, sort, save to `data/cleaned/`

---

## 📊 Results Example

| Metric              | Value                                  |
| ------------------- | -------------------------------------- |
| Cleaned datasets    | 3 (Global, Retail, USA)                |
| Missing values      | 0 (after cleaning)                     |
| Duplicates removed  | ✅                                     |
| Valid sales formula | ✅ `sales = quantity × unit_price`      |
| Date Format         | ISO (`YYYY-MM-DD`)                     |

---

## 🧠 Streamlit UI Highlights

- Upload CSV (any encoding!)
- Auto-clean via `clean_sales_data.py`
- Preview, summary, download
- Stats: missing values, duplicates, valid columns

---

## 📂 Directory Structure

```
CSV-Cleaner-Pro/
├── data/
│   ├── raw/                # Messy CSVs
│   └── cleaned/            # Cleaned outputs
├── scripts/
│   ├── app.py              # Streamlit web app
│   └── clean_sales_data.py # Core cleaning logic
├── assets/                 # README screenshots
├── requirements.txt
└── README.md
```

---

## 🧪 Test Datasets

| Dataset                        | Description                 |
| ------------------------------ | ---------------------------|
| sales_dirty.csv                | Internal messy sample       |
| kaggle_test_1_sample_sales.csv | Global sales sample         |
| kaggle_test_2_retail_sales.csv | Retail transactions         |
| kaggle_test_3_sales_usa.csv    | US sales sample             |

---

## 🚀 Roadmap

- Progress bar & logs
- Data visualizations (sales, trends, categories)
- PDF cleaning report
- Google Sheets API integration

---

## 📦 Exported Deliverables

| Item               | Description                                 |
| -------------------|--------------------------------------------|
| ✅ CLI Tool        | Command line loader/cleaner                 |
| ✅ Streamlit App   | Web interface: upload → clean → download    |
| ✅ CI-Tested       | Automated tests via GitHub Actions          |
| ✅ Docs & Demos    | README, screenshots, usage guide            |
| ✅ Example Data    | Sample CSVs, summary reports                |

---

## 👨‍💻 Author

**Bibhudendu Behera**  
Aspiring AI Engineer · Data Specialist  
Bangalore, India  
[LinkedIn](https://www.linkedin.com/in/bibhudendu-behera-b5375b5b) · [GitHub](https://github.com/bibhu342) · [Fiverr](https://www.fiverr.com/s/7YEbRPk)  
📧 bibhu342@gmail.com

---

## 📜 License

MIT License © 2025 — Free to use and modify with attribution.