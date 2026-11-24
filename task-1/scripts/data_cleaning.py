"""Clean the raw Superstore dataset and persist CSV and SQLite outputs."""

from pathlib import Path
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "superstore_raw.csv"
CLEANED_PATH = PROJECT_ROOT / "data" / "superstore_cleaned.csv"
DB_PATH = PROJECT_ROOT / "data" / "superstore.db"


def load_raw_data(path: Path = RAW_PATH) -> pd.DataFrame:
    """Load the raw CSV file with UTF-8/Latin-1 fallback."""
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")


def clean_superstore_data(raw_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Remove appended non-order rows, deduplicate, standardize types, and engineer features."""
    stats: dict[str, int] = {"raw_rows": len(raw_df)}

    # Drop appended metadata/return rows where Order Date or Sales is missing
    df = raw_df.dropna(subset=["Order Date", "Ship Date", "Sales", "Profit"]).copy()
    stats["after_dropping_non_order_rows"] = len(df)
    stats["non_order_rows_removed"] = stats["raw_rows"] - stats["after_dropping_non_order_rows"]

    # Standardize column names to snake_case for Python and SQL compatibility
    df.columns = [col.strip().lower().replace(" ", "_").replace("-", "_") for col in df.columns]

    # Strip extraneous whitespace on text columns
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype("string").str.strip()

    # Parse dates and numeric types
    df["row_id"] = pd.to_numeric(df["row_id"], errors="coerce").astype("Int64")
    df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y")
    for num_col in ["sales", "quantity", "discount", "profit"]:
        df[num_col] = pd.to_numeric(df[num_col], errors="coerce")

    # Impute missing Postal Code (Burlington, Vermont -> 05401) and zero-pad to 5 digits
    stats["missing_postal_codes_filled"] = int(df["postal_code"].isna().sum())
    df["postal_code"] = (
        df["postal_code"]
        .fillna(5401)
        .astype(float)
        .astype(int)
        .astype(str)
        .str.zfill(5)
    )

    # Deduplicate identical line items ignoring row_id
    feature_cols = [c for c in df.columns if c != "row_id"]
    before_dedup = len(df)
    df = df.drop_duplicates(subset=feature_cols, keep="first").reset_index(drop=True)
    stats["duplicates_removed"] = before_dedup - len(df)
    stats["cleaned_rows"] = len(df)

    # Feature engineering
    df["order_year"] = df["order_date"].dt.year
    df["order_month"] = df["order_date"].dt.month
    df["order_year_month"] = df["order_date"].dt.to_period("M").astype(str)
    df["order_quarter"] = df["order_date"].dt.to_period("Q").astype(str)
    df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
    df["profit_margin"] = np.where(df["sales"] != 0, df["profit"] / df["sales"], 0.0)
    df["is_profitable"] = df["profit"] > 0

    return df, stats


def save_outputs(df: pd.DataFrame, csv_path: Path = CLEANED_PATH, db_path: Path = DB_PATH) -> None:
    """Save cleaned DataFrame to CSV and SQLite via SQLAlchemy."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)

    engine = create_engine(f"sqlite:///{db_path}")
    df.to_sql("orders", con=engine, if_exists="replace", index=False)
    with engine.connect() as conn:
        row_count = conn.execute(text("SELECT COUNT(*) FROM orders")).scalar_one()
    print(f"Saved cleaned CSV: {csv_path} ({len(df)} rows)")
    print(f"Saved SQLite DB:   {db_path} (table 'orders': {row_count} rows)")


def main() -> None:
    raw_df = load_raw_data()
    cleaned_df, stats = clean_superstore_data(raw_df)
    print("Cleaning Summary:")
    for key, val in stats.items():
        print(f"  - {key}: {val}")
    save_outputs(cleaned_df)


if __name__ == "__main__":
    main()

