# 🧹 CSV-Cleaner-Pro
### A Python-Powered Data Cleaning Automation Tool

---

## 📘 Project Overview
**CSV-Cleaner-Pro** is a production-ready, automated Python tool built to clean and standardize messy sales data in CSV format.  
It reads raw datasets, fixes missing and inconsistent values, validates business logic (`sales = quantity × unit_price`), and exports a perfectly cleaned file — ready for analytics, dashboards, or machine learning.

---

## 🎯 Objective
To automate the process of cleaning messy CSV data using pure **Python + Pandas** — ensuring accurate, formatted, and analysis-ready datasets.

---

## ⚙️ Tech Stack
- **Language:** Python (v3.11)
- **Libraries:** Pandas, NumPy, Pathlib
- **Tools:** Jupyter Notebook, VS Code, GitHub
- **Dataset:** 160-row sample messy sales data (`sales_dirty.csv`)

---

## 🧩 Data Cleaning Pipeline

### 1️⃣ Data Inspection
- Checked structure, types, and missing values using `df.info()` and `df.isna()`
- Found 10 missing customer names, 7 missing order dates, and 10 duplicate rows

### 2️⃣ Handle Missing Values
```python
df['customer_name'] = df['customer_name'].fillna("Unknown")
df['order_date'] = df['order_date'].fillna("2024-12-31")

### 3️⃣ Text Normalization
for col in ['customer_name', 'city', 'category', 'product']:
    df[col] = df[col].astype(str).str.strip().str.title()

### 4️⃣ Numeric Cleaning
for col in ['unit_price', 'sales']:
    df[col] = (
        df[col].astype(str)
        .str.replace(r'[^0-9.\-]', '', regex=True)
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')

### 5️⃣ Validation & Fixes
df['sales'] = df['quantity'] * df['unit_price']

### 6️⃣ Date Cleaning
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

### 7️⃣ Finalization
- Removed duplicates
- Sorted chronologically
- Exported cleaned dataset

### 🧾 Final Results
| Metric              | Result                            |
| ------------------- | --------------------------------- |
| Original rows       | 160                               |
| Cleaned rows        | 150                               |
| Columns             | 9                                 |
| Missing values      | 0                                 |
| Duplicates removed  | 10                                |
| Valid sales formula | ✅ `sales = quantity × unit_price` |
| Date format         | ISO (`YYYY-MM-DD`)                |

### 📁 Folder Structure
CSV-Cleaner-Pro/
├── data/
│   ├── raw/ (messy input)
│   └── cleaned/ (final outputs)
├── scripts/
│   └── clean_sales_data.py
├── notebooks/
│   └── CSV_Cleaner_Pro_Dev.ipynb
├── README.md
├── requirements.txt
└── .gitignore

### ⚙️ How to Use

1️⃣ Clone the Repository
git clone https://github.com/bibhudendu-behera/CSV-Cleaner-Pro.git
cd CSV-Cleaner-Pro

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Place Your Raw File
Drop your messy CSV file inside:
data/raw/sales_dirty.csv

4️⃣ Run the Cleaner Script
python scripts/clean_sales_data.py

5️⃣ Get Your Output
Cleaned file will be saved at:
data/cleaned/sales_cleaned_final.csv

🧠 Key Learnings
- Real-world data cleaning using Pandas
- Handling mixed date formats and currencies
- Automating dataset cleaning end-to-end
- Reusable code design for freelancing tasks

🚀 Future Enhancements
- Add CLI arguments:
  python scripts/clean_sales_data.py --input <file> --output <file>
- Add logging and progress tracking
- Deploy as a web-based cleaning tool using Streamlit or Flask

👨‍💻 Author
Bibhudendu Behera
🚀 Aspiring AI Engineer | Freelance Data Specialist
📍 Bangalore, India
🔗 LinkedIn

💼 Freelancing Focus: Data Cleaning, Automation, Python Tools