# Retail Sales & Revenue Dashboard

## 1. Project Overview

This is a Power BI dashboard project built to analyze retail sales performance for a coffee shop business.

The main goal of this project is to help a retail company monitor revenue, profit, product performance, customer behavior, and future sales trends in one interactive dashboard.

The dashboard answers questions such as:

- How much revenue and profit did the business generate?
- Which product categories contribute the most revenue?
- Which regions or store areas are most profitable?
- Which products are best sellers?
- Which customer segments are the most valuable?
- What does the sales trend look like in the next few months?

## 2. Tools Used

- Power BI Desktop
- Power Query
- DAX
- Excel / CSV
- Python for data preparation
- GitHub for project documentation and version control

## 3. Dataset

Dataset source: [Coffee Shop Sales - Kaggle](https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales/data)

The original dataset contains transaction-level coffee shop sales data from `2023-01-01` to `2023-06-30`.

Key fields used in the dashboard:

- Order Date
- Revenue
- Profit
- Quantity
- Product Category
- Product Name
- Store Location
- Region
- Segment
- Customer ID

Note: the original Kaggle dataset does not include profit, customer, region, or segment fields. I created these additional analytical fields during the data preparation step so the dashboard can support profit analysis, customer analytics, and regional comparison.

## 4. Data Preparation

Main cleaning and preparation steps:

1. Removed duplicate records.
2. Removed empty rows.
3. Converted date, time, number, and currency columns to correct formats.
4. Created `Revenue` from quantity and unit price.
5. Estimated `Profit` using product-category margin assumptions.
6. Created simulated `CustomerID` for customer analysis.
7. Created `Segment` and `Region` fields for business reporting.
8. Exported the cleaned dataset for Power BI.

Cleaned data file:

```text
data/processed/coffee_shop_sales_clean.csv
```

## 5. Dashboard Pages

### Page 1 - Executive Overview

This page gives a high-level view of business performance.

Main visuals:

- Total Revenue card
- Total Profit card
- Profit Margin card
- Average Order Value card
- Total Orders card
- Sales Trend line chart
- Revenue by Category bar chart
- Profit by Region treemap
- Region, Segment, Category, and Date slicers

### Page 2 - Product Performance

This page focuses on product-level performance.

Main visuals:

- Product performance table
- Top 10 products by revenue
- Revenue and profit comparison
- Product category analysis

This page helps identify best-selling products, low-margin products, and products that may need operational attention.

### Page 3 - Customer Analytics

This page analyzes customer behavior and segment performance.

Main visuals:

- Repeat Customer card
- Customer Count card
- Average Customer Spend card
- Revenue by Segment bar chart
- Revenue Share by Segment donut chart
- Segment profitability matrix

### Page 4 - Sales Forecast

This page shows the sales trend and forecast.

Main visuals:

- Revenue trend by date
- 3-month sales forecast
- Confidence interval for forecast range

## 6. Key Measures

Some DAX measures used in this project:

```DAX
Total Revenue = SUM(Sales[Revenue])
```

```DAX
Total Profit = SUM(Sales[Profit])
```

```DAX
Profit Margin = DIVIDE([Total Profit], [Total Revenue])
```

```DAX
Total Orders = DISTINCTCOUNT(Sales[OrderID])
```

```DAX
Avg Order Value = DIVIDE([Total Revenue], [Total Orders])
```

```DAX
Customer Count = DISTINCTCOUNT(Sales[CustomerID])
```

## 7. Main KPIs

| KPI | Value |
| --- | ---: |
| Total Revenue | $698.81K |
| Total Profit | $273.90K |
| Profit Margin | 39.19% |
| Total Orders | 149K |
| Average Order Value | $4.69 |
| Quantity Sold | 214,470 |

## 8. Insights

- Coffee is the strongest revenue category, generating about `$269.95K`.
- Tea is the second-highest revenue category, generating about `$196.41K`.
- Manhattan is the most profitable region in the dataset.
- Beverage products dominate revenue share compared with other segments.
- Sales show an upward trend from January to June 2023.
- The forecast indicates continued revenue growth if the current trend continues.

## 9. Project Files

```text
Retail-Sales-Revenue-Dashboard/
│
├── data/
│   ├── raw/
│   │   └── Coffee Shop Sales.xlsx
│   └── processed/
│       └── coffee_shop_sales_clean.csv
│
├── powerbi/
│   ├── Retail Sales Revenue Dashboard/
│   │   └── Retail Sales Revenue Dashboard.pbix
│   ├── dax_measures.dax
│   └── theme_retail_corporate.json
│
├── scripts/
│   ├── download_dataset.ps1
│   └── prepare_data.py
│
└── docs/
    └── dashboard_build_guide.md
```

## 10. How to Open the Dashboard

Open the Power BI file:

```text
powerbi/Retail Sales Revenue Dashboard/Retail Sales Revenue Dashboard.pbix
```

If the `.pbix` file needs to be rebuilt, load the cleaned CSV file into Power BI:

```text
data/processed/coffee_shop_sales_clean.csv
```

Then apply the DAX measures from:

```text
powerbi/dax_measures.dax
```

## 11. What I Learned

Through this project, I practiced:

- Cleaning and preparing sales data
- Creating business KPIs with DAX
- Building interactive Power BI dashboards
- Designing executive-level reports
- Analyzing product and customer performance
- Creating a sales forecast in Power BI
- Presenting business insights from raw transactional data

## 12. Business Value

This dashboard helps business users quickly understand sales performance, identify strong and weak product categories, monitor customer segments, and support better operational decisions through data visualization.
