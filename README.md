![CSV Cleaner Pro Banner](banner.png)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://csv-cleaner-pro-qy34r3dkdap9d327sn375l.streamlit.app/)

# 🧹 CSV-Cleaner-Pro  
**Clean, validate, and standardize messy CSV sales data — instantly.**  
*A Python + Streamlit powered automation tool for data specialists, analysts, and freelancers.*

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-green?logo=pandas\&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![GitHub last commit](https://img.shields.io/github/last-commit/bibhu342/CSV-Cleaner-Pro)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🌐 Live Demo  
👉 **Try it now (hosted on Streamlit Cloud):**  
🔗 [https://csv-cleaner-pro-qy34r3dkdap9d327sn375l.streamlit.app/](https://csv-cleaner-pro-qy34r3dkdap9d327sn375l.streamlit.app/)

---

## 💡 Problem It Solves  
Real-world CSV files often contain inconsistent column names, mixed date formats, currency symbols, and duplicate rows.  
**CSV-Cleaner-Pro** automates the entire cleaning process using Python + Pandas, instantly transforming raw CSVs into analysis-ready data — saving hours of manual cleanup.

---

## ⚙️ Tech Stack  

| Category | Tools |
|-----------|--------|
| **Language** | Python 3.11 |
| **Framework** | [Streamlit](https://streamlit.io) |
| **Libraries** | Pandas, NumPy, Pathlib |
| **Environment** | VS Code, GitHub, Streamlit Cloud |

---

## 🚀 Quickstart  

```bash
git clone https://github.com/bibhudendu-behera/CSV-Cleaner-Pro.git
cd CSV-Cleaner-Pro
pip install -r requirements.txt
streamlit run scripts/app.py
Then open http://localhost:8501
```

---

## 📘 Project Overview

**CSV-Cleaner-Pro** is a production-ready, automated Python tool built to clean and standardize messy sales data in CSV format.
It reads raw datasets, fixes missing and inconsistent values, validates business logic (`sales = quantity × unit_price`), and exports a perfectly cleaned file — ready for analytics, dashboards, or machine learning.

---

## 🎯 Objective

To automate the process of cleaning messy CSV data using **Python + Pandas**,
and wrap it in an interactive **Streamlit UI** for non-technical users to easily upload, preview, and download cleaned files.

---

## ⚙️ Tech Stack

* **Language:** Python (v3.11)
* **Libraries:** Pandas, NumPy, Streamlit, Pathlib
* **Tools:** VS Code, GitHub
* **Core Script:** `scripts/clean_sales_data.py`

---

## 🧩 Data Cleaning Pipeline

### 1️⃣ Data Inspection

* Checked structure, types, and missing values using `df.info()` and `df.isna()`
* Found missing customer names, missing order dates, and duplicate rows

### 2️⃣ Handle Missing Values

```python
df['customer_name'] = df['customer_name'].fillna("Unknown")
df['order_date'] = df['order_date'].fillna("2024-12-31")
```

### 3️⃣ Text Normalization

```python
for col in ['customer_name', 'city', 'category', 'product']:
    df[col] = df[col].astype(str).str.strip().str.title()
```

### 4️⃣ Numeric Cleaning

```python
for col in ['unit_price', 'sales']:
    df[col] = (
        df[col].astype(str)
        .str.replace(r'[^0-9.\-]', '', regex=True)
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')
```

### 5️⃣ Validation & Fixes

```python
df['sales'] = df['quantity'] * df['unit_price']
```

### 6️⃣ Date Cleaning

```python
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
```

### 7️⃣ Finalization

* Removed duplicates
* Sorted chronologically
* Exported cleaned dataset to `data/cleaned/`

---

## 🧾 Final Results

| Metric              | Result                            |
| ------------------- | --------------------------------- |
| Cleaned datasets    | 3 (Global, Retail, USA)           |
| Missing values      | 0 after cleaning                  |
| Duplicates removed  | ✅                                 |
| Valid sales formula | ✅ `sales = quantity × unit_price` |
| Date format         | ISO (`YYYY-MM-DD`)                |

---

## 🧠 Streamlit UI Features

* Upload any `.csv` file (any encoding: UTF-8, latin1, cp1252)
* Cleans data instantly using `clean_sales_data.py`
* Displays preview + metrics + missing value summary
* Download the cleaned CSV directly

### Run the App

```bash
streamlit run scripts/app.py
```

Then open in your browser:
**[http://localhost:8501](http://localhost:8501)**

---

## 📂 Folder Structure

```
CSV-Cleaner-Pro/
│
├── data/
│   ├── raw/              # Raw messy CSVs
│   └── cleaned/          # Cleaned outputs
│
├── scripts/
│   ├── app.py            # Streamlit front-end
│   └── clean_sales_data.py  # Core cleaning logic
│
├── assets/               # Screenshots for README
├── requirements.txt
└── README.md
```

---

## 📊 Datasets Used for Testing

| Dataset                          | Purpose                           | Status |
| -------------------------------- | --------------------------------- | ------ |
| `sales_dirty.csv`                | Internal messy sample (base test) | ✅      |
| `kaggle_test_1_sample_sales.csv` | Global sample sales data          | ✅      |
| `kaggle_test_2_retail_sales.csv` | Retail transaction dataset        | ✅      |
| `kaggle_test_3_sales_usa.csv`    | US-based sales dataset            | ✅      |

---

## 🧮 Demo Screenshots

| Dataset           | Screenshot                |
| ----------------- | ------------------------- |
| Sample Sales Data | `assets/demo_clean_1.png` |
| Retail Sales Data | `assets/demo_clean_2.png` |
| USA Sales Dataset | `assets/demo_clean_3.png` |

---

## 🧠 Key Learnings

* Real-world data cleaning using Pandas
* Handling multi-encoding and multi-locale CSVs
* Automating end-to-end data preprocessing
* Building Streamlit apps for quick ETL workflows

---

## 🚀 Future Enhancements

* Add CLI arguments (`--input`, `--output`)
* Add progress tracking and logging
* Deploy on Streamlit Cloud
* Add visualization / EDA mode (sales trends, top categories)

---

## 👨‍💻 Author

**Bibhudendu Behera**  
🚀 Aspiring AI Engineer | Freelance Data Specialist  
📍 Bangalore, India  
🔗 [LinkedIn](https://www.linkedin.com/in/bibhudendu-behera-b5375b5b)

---

## 📜 License

MIT License © 2025 — free to use and modify with attribution.

