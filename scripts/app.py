# app.py (Streamlit UI for CSV-Cleaner-Pro)
# Save this file at:
# C:\Users\Adithya\Downloads\Bibhu\Freelance\CSV_Cleaner_Pro\scripts\app.py

import sys
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import traceback
import importlib.util
import typing

# Ensure the scripts/ folder is on sys.path so imports like `import clean_sales_data`
# succeed when app.py runs from the scripts/ folder.
THIS_FILE = Path(__file__).resolve()
SCRIPTS_DIR = THIS_FILE.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


# ---------------------------
# Project root detection
# ---------------------------
# If this file is inside "scripts/" within your project, project_root will be the parent folder.
THIS_FILE = Path(__file__).resolve()
SCRIPTS_DIR = THIS_FILE.parent
PROJECT_ROOT = SCRIPTS_DIR.parent

# Useful paths (create if missing)
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_CLEANED = PROJECT_ROOT / "data" / "cleaned"
DATA_RAW.mkdir(parents=True, exist_ok=True)
DATA_CLEANED.mkdir(parents=True, exist_ok=True)

# Banner (optional)
BANNER_PATH = PROJECT_ROOT / "banner.png"

# ---------------------------
# Import your cleaning function
# ---------------------------
# Expected function signature (recommended):
#   clean_sales_data(input_path: str | Path, output_path: str | Path) -> None
# If your actual function has a different name or signature, update the `CLEANER_FUNC_NAME`.
CLEANER_MODULE_NAME = "clean_sales_data"
CLEANER_FUNC_NAME = "clean_sales_data"


def load_cleaner_module() -> typing.Callable:
    """
    Attempt to import clean_sales_data.clean_sales_data.
    Fallback: load module from file PROJECT_ROOT/clean_sales_data.py
    Returns the callable function.
    Raises ImportError/AttributeError if not found.
    """
    # 1) Try normal import
    try:
        mod = importlib.import_module(CLEANER_MODULE_NAME)
        func = getattr(mod, CLEANER_FUNC_NAME)
        return func
    except Exception:
        # 2) Fallback: look for file in project root and scripts folder
        possible_paths = [
            PROJECT_ROOT / f"{CLEANER_MODULE_NAME}.py",
            SCRIPTS_DIR / f"{CLEANER_MODULE_NAME}.py",
        ]
        for p in possible_paths:
            if p.exists():
                try:
                    spec = importlib.util.spec_from_file_location(CLEANER_MODULE_NAME, str(p))
                    module = importlib.util.module_from_spec(spec)
                    loader = spec.loader
                    assert loader is not None
                    loader.exec_module(module)
                    func = getattr(module, CLEANER_FUNC_NAME)
                    return func
                except Exception as e:
                    raise ImportError(f"Found {p} but failed to load function '{CLEANER_FUNC_NAME}': {e}") from e

        # If we reach here, raise helpful error
        raise ImportError(
            f"Could not import module '{CLEANER_MODULE_NAME}' or find it at {possible_paths}. "
            "Make sure clean_sales_data.py exists in the project root or scripts/ and defines "
            f"a function named '{CLEANER_FUNC_NAME}(input_path, output_path)'."
        )


# Lazily load the cleaning function so Streamlit starts even if import has issues
try:
    clean_sales_data = load_cleaner_module()
except Exception as e:
    clean_sales_data = None
    CLEANER_IMPORT_ERROR = str(e)
else:
    CLEANER_IMPORT_ERROR = None

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="CSV-Cleaner-Pro", page_icon="🧹", layout="wide")

# Top header
col_left, col_right = st.columns([3, 1])
with col_left:
    st.title("🧹 CSV-Cleaner-Pro")
    st.subheader("Upload → Clean → Preview → Download")
    st.markdown(
        "A small UI wrapper around your cleaning logic (`clean_sales_data.py`). "
        "This app writes uploaded files to `data/raw/` and cleaned files to `data/cleaned/`."
    )
with col_right:
    if BANNER_PATH.exists():
        st.image(str(BANNER_PATH), width=200)

# Sidebar — instructions & debugging
with st.sidebar:
    st.header("How to use")
    st.markdown(
        """
1. Choose a CSV file (comma-separated).  
2. Click **Clean & Preview**.  
3. Inspect the cleaned preview and download the result.
"""
    )
    st.markdown("---")
    st.header("Developer / Debug")
    if CLEANER_IMPORT_ERROR:
        st.error("Cleaner import error — app cannot run cleaning.")
        st.caption(CLEANER_IMPORT_ERROR)
        st.markdown(
            "Make sure `clean_sales_data.py` exists at the project root and defines:\n\n"
            "`def clean_sales_data(input_path, output_path):`"
        )
    else:
        st.success("Cleaner module loaded.")
        st.caption(f"Cleaner func: {CLEANER_FUNC_NAME}()")
    st.markdown("---")
    st.write("Advanced: you can run the cleaner script directly from the project root:")
    st.code("python clean_sales_data.py", language="bash")

# File uploader area
st.markdown("## Upload CSV")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"], accept_multiple_files=False)
force_overwrite = st.checkbox("Overwrite existing cleaned file if name collides", value=True)
run_button = st.button("Clean & Preview")

# Helper: show friendly error box
def _show_import_error():
    st.error("Cleaner not available. Fix import or place clean_sales_data.py in project root.")
    if 'CLEANER_IMPORT_ERROR' in globals():
        st.text(CLEANER_IMPORT_ERROR)


# Main run block
if run_button:
    if clean_sales_data is None:
        _show_import_error()
    else:
        if uploaded_file is None:
            st.warning("Please upload a CSV file first.")
        else:
            try:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                raw_fname = f"uploaded_{ts}.csv"
                cleaned_fname = f"uploaded_cleaned_{ts}.csv"

                raw_path = DATA_RAW / raw_fname
                cleaned_path = DATA_CLEANED / cleaned_fname

                # Save uploaded bytes to disk (Streamlit gives an UploadedFile object)
                with open(raw_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.info(f"Saved uploaded file to `{raw_path}`. Running cleaner...")

                # Call the cleaner function. Many implementations accept (input_path, output_path).
                # If your function has a different signature, adjust accordingly.
                # We convert Path to str just to be compatible.
                # pass Path objects so cleaner code that uses .parent/.exists() works
                clean_sales_data(input_path=raw_path, output_path=cleaned_path)


                # Load cleaned CSV into DataFrame for preview
                df_clean = pd.read_csv(cleaned_path)

                st.success("✅ Cleaning completed successfully.")
                # Metrics row
                m1, m2, m3 = st.columns([1, 1, 1])
                with m1:
                    st.metric("Rows", f"{df_clean.shape[0]}")
                with m2:
                    st.metric("Columns", f"{df_clean.shape[1]}")
                with m3:
                    missing_total = int(df_clean.isna().sum().sum())
                    st.metric("Total missing cells", f"{missing_total}")

                # Two-column layout: preview + summary
                left_col, right_col = st.columns([3, 1])
                with left_col:
                    st.markdown("### Preview (first 10 rows)")
                    st.dataframe(df_clean.head(10), use_container_width=True)
                    st.markdown("### Sample validation (first 5 rows)")
                    # Show a tiny validation: sales == quantity * unit_price if those columns exist
                    if {"quantity", "unit_price", "sales"}.issubset(set(map(str.lower, df_clean.columns))):
                        # Normalize column case-sensitively — attempt common names
                        # This tries to find exact columns (case-insensitive)
                        cols_lower_map = {c.lower(): c for c in df_clean.columns}
                        qcol = cols_lower_map.get("quantity")
                        upcol = cols_lower_map.get("unit_price")
                        scol = cols_lower_map.get("sales")
                        # compute difference
                        try:
                            sample = df_clean[[qcol, upcol, scol]].head(5).copy()
                            sample["calc_sales"] = (sample[qcol] * sample[upcol]).round(2)
                            sample["sales_diff"] = (sample[scol].round(2) - sample["calc_sales"]).round(2)
                            st.dataframe(sample)
                        except Exception:
                            st.info("Could not run quick formula check (unexpected column types).")
                    else:
                        st.info("Formula check skipped (quantity/unit_price/sales columns not present).")

                with right_col:
                    st.markdown("### Summary stats")
                    numeric_df = df_clean.select_dtypes(include="number")
                    if not numeric_df.empty:
                        st.dataframe(numeric_df.describe().transpose())
                    else:
                        st.info("No numeric columns to summarize.")

                    st.markdown("### Missing values")
                    miss = df_clean.isna().sum().to_frame("missing_count")
                    miss["missing_pct"] = (miss["missing_count"] / len(df_clean) * 100).round(2)
                    st.dataframe(miss.sort_values("missing_count", ascending=False))

                    st.markdown("### Quick actions")
                    # Download button (generates fresh bytes)
                    csv_bytes = df_clean.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Download cleaned CSV",
                        data=csv_bytes,
                        file_name=f"cleaned_sales_{ts}.csv",
                        mime="text/csv",
                    )
                    st.write(f"Saved cleaned file at `{cleaned_path}`.")

            except Exception as exc:
                st.error("❌ Cleaning failed — see traceback below.")
                st.text(traceback.format_exc())
                st.markdown("**Hints / next steps**")
                st.write(
                    """
- Make sure your CSV headers are what the cleaner expects (open the CSV in a text editor or Excel).  
- If you see an ImportError about the cleaner, ensure `clean_sales_data.py` exists and defines `clean_sales_data(input_path, output_path)`.  
- For encoding errors, re-save CSV as UTF-8 and try again.
"""
                )

# Footer
st.markdown("---")
st.caption("CSV-Cleaner-Pro — Streamlit UI. Written to work from the `scripts/` folder. 🚀")
