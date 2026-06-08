# Retail Sales & Revenue Dashboard

Power BI project mô phỏng nhu cầu của một công ty bán lẻ cần theo dõi doanh thu, lợi nhuận, hiệu suất sản phẩm, hành vi khách hàng và forecast sales.

## Dataset

Nguồn dữ liệu: [Coffee Shop Sales - Kaggle](https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales/data)

File gốc có 149,116 giao dịch từ 2023-01-01 đến 2023-06-30. Dataset gốc không có `Profit`, `Customer`, `Region`, `Segment`, nên project tạo thêm các trường mô phỏng có kiểm soát trong `scripts/prepare_data.py`.

## Project structure

```text
data/
  raw/Coffee Shop Sales.xlsx
  processed/coffee_shop_sales_clean.csv
docs/
  dashboard_build_guide.md
powerbi/
  dax_measures.dax
  power_query_transform.m
  theme_retail_corporate.json
scripts/
  download_dataset.ps1
  prepare_data.py
```

## How to run

```powershell
.\scripts\download_dataset.ps1
C:\Users\tuanh\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts\prepare_data.py
```

If Python is installed globally, this also works:

```powershell
python scripts\prepare_data.py
```

## Power BI setup

1. Open `powerbi/Retail Sales Revenue Dashboard/coffee_shop_sales_clean.pbids`.
2. In Power BI Desktop Navigator, select `coffee_shop_sales_clean.csv`.
3. Click `Load`.
4. Rename the loaded table to `Sales`.
5. Apply the DAX measures from `powerbi/dax_measures.dax`.
6. Build the visuals using `docs/dashboard_build_guide.md`.
7. Save as `.pbix`.

The repository includes a Power BI data-source shortcut plus a preview workbook:

- `powerbi/Retail Sales Revenue Dashboard/coffee_shop_sales_clean.pbids`
- `powerbi/Retail Sales Revenue Dashboard/Retail Sales Revenue Dashboard Preview.xlsx`

The `.pbids` file lets Power BI Desktop create the query/model through its official import flow. The preview workbook mirrors the first dashboard page with KPI cards and charts for quick review outside Power BI.

## Core KPIs

| KPI | Value |
| --- | ---: |
| Total Revenue | $698,812.33 |
| Total Profit | $273,898.46 |
| Profit Margin | 39.19% |
| Total Orders | 149,116 |
| Quantity Sold | 214,470 |
| Simulated Customers | 17,994 |

## Required report pages

### Page 1 - Executive Overview

- KPI cards: Revenue, Profit, Margin, Orders, AOV
- Sales trend line chart
- Revenue by category bar chart
- Profit by region treemap or map

### Page 2 - Product Performance

- Top products table
- Top 10 products by revenue
- Revenue vs margin scatter chart
- Insight focus: low-margin winners, dead products, best sellers

### Page 3 - Customer Analytics

- Repeat Customer
- Customer Count
- Avg Customer Spend
- Segment analysis by revenue and profit margin

### Page 4 - Sales Forecast

- Line chart by date
- Power BI Analytics forecast: 3 months or 6 months

## Initial insights

- Coffee is the highest revenue category at about `$269.95K`.
- Tea is second at about `$196.41K`.
- Manhattan has the highest estimated profit because it covers Hell's Kitchen and Lower Manhattan.
- Top product by revenue is `Sustainably Grown Organic Lg`.
- Profit fields are estimated, so business conclusions about margin should be framed as model-based assumptions.
