from __future__ import annotations

from pathlib import Path
import hashlib

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_XLSX = ROOT / "data" / "raw" / "Coffee Shop Sales.xlsx"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_CSV = PROCESSED_DIR / "coffee_shop_sales_clean.csv"


PROFIT_RATE_BY_CATEGORY = {
    "Bakery": 0.34,
    "Branded": 0.28,
    "Coffee": 0.42,
    "Coffee beans": 0.31,
    "Drinking Chocolate": 0.38,
    "Flavours": 0.55,
    "Loose Tea": 0.37,
    "Packaged Chocolate": 0.33,
    "Tea": 0.40,
}

SEGMENT_BY_CATEGORY = {
    "Bakery": "Food",
    "Branded": "Merchandise",
    "Coffee": "Beverage",
    "Coffee beans": "Retail Pack",
    "Drinking Chocolate": "Beverage",
    "Flavours": "Add-on",
    "Loose Tea": "Retail Pack",
    "Packaged Chocolate": "Retail Pack",
    "Tea": "Beverage",
}

REGION_BY_STORE = {
    "Astoria": "Queens",
    "Hell's Kitchen": "Manhattan",
    "Lower Manhattan": "Manhattan",
}


def stable_customer_id(row: pd.Series) -> str:
    """Create a repeatable simulated customer key for customer analytics."""
    seed = f"{row['store_id']}|{row['transaction_date']}|{row['transaction_time']}|{row['transaction_id']}"
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
    bucket = int(digest[:8], 16) % 18000 + 1
    return f"CUST-{bucket:05d}"


def main() -> None:
    if not RAW_XLSX.exists():
        raise FileNotFoundError(
            f"Missing source workbook: {RAW_XLSX}. Run scripts/download_dataset.ps1 first."
        )

    df = pd.read_excel(RAW_XLSX, sheet_name="Transactions")
    df = df.dropna(how="all").drop_duplicates()

    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["transaction_time"] = df["transaction_time"].astype(str)
    df["transaction_qty"] = pd.to_numeric(df["transaction_qty"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["transaction_date", "transaction_qty", "unit_price"])

    df["Revenue"] = (df["transaction_qty"] * df["unit_price"]).round(2)
    df["ProfitRate"] = df["product_category"].map(PROFIT_RATE_BY_CATEGORY).fillna(0.35)
    df["Profit"] = (df["Revenue"] * df["ProfitRate"]).round(2)
    df["EstimatedCost"] = (df["Revenue"] - df["Profit"]).round(2)
    df["CustomerID"] = df.apply(stable_customer_id, axis=1)
    df["Segment"] = df["product_category"].map(SEGMENT_BY_CATEGORY).fillna("Other")
    df["Region"] = df["store_location"].map(REGION_BY_STORE).fillna("New York")
    df["City"] = "New York"
    df["OrderDate"] = df["transaction_date"].dt.date
    df["OrderTime"] = df["transaction_time"]
    df["Year"] = df["transaction_date"].dt.year
    df["MonthNo"] = df["transaction_date"].dt.month
    df["MonthName"] = df["transaction_date"].dt.strftime("%b")
    df["YearMonth"] = df["transaction_date"].dt.strftime("%Y-%m")
    df["Weekday"] = df["transaction_date"].dt.day_name()
    df["Hour"] = pd.to_datetime(df["transaction_time"], format="%H:%M:%S").dt.hour

    clean = df.rename(
        columns={
            "transaction_id": "OrderID",
            "transaction_qty": "Quantity",
            "store_id": "StoreID",
            "store_location": "StoreLocation",
            "product_id": "ProductID",
            "unit_price": "UnitPrice",
            "product_category": "ProductCategory",
            "product_type": "ProductType",
            "product_detail": "ProductName",
        }
    )[
        [
            "OrderID",
            "OrderDate",
            "OrderTime",
            "Quantity",
            "StoreID",
            "StoreLocation",
            "City",
            "Region",
            "CustomerID",
            "Segment",
            "ProductID",
            "ProductCategory",
            "ProductType",
            "ProductName",
            "UnitPrice",
            "Revenue",
            "EstimatedCost",
            "Profit",
            "ProfitRate",
            "Year",
            "MonthNo",
            "MonthName",
            "YearMonth",
            "Weekday",
            "Hour",
        ]
    ]

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    clean.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"Rows exported: {len(clean):,}")
    print(f"Output: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
