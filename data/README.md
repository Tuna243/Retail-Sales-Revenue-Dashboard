# Data

Source dataset: [Coffee Shop Sales by ahmedabbas757 on Kaggle](https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales/data).

## Raw

`data/raw/Coffee Shop Sales.xlsx` contains the original `Transactions` sheet from Kaggle.

## Processed

`data/processed/coffee_shop_sales_clean.csv` is the Power BI-ready table produced by `scripts/prepare_data.py`.

Because the source dataset does not include customer, segment, region, or profit fields, the processed file adds:

- `Revenue`: `Quantity * UnitPrice`
- `Profit`: estimated profit using category-level margin assumptions
- `CustomerID`: repeatable simulated customer identifier for customer analytics
- `Segment`: product-driven business segment
- `Region`, `City`: store-location mapping for geographic visuals

These simulated fields should be described as assumptions in the Power BI report.
