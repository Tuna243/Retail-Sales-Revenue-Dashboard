# Retail Sales & Revenue Dashboard - Power BI Build Guide

## 1. Import data

1. Open Power BI Desktop.
2. Select `Get Data -> Text/CSV`.
3. Choose `data/processed/coffee_shop_sales_clean.csv`.
4. Select `Transform Data`.
5. Rename the query to `Sales`.
6. Confirm data types match `powerbi/power_query_transform.m`.

## 2. Data model

Create a Date table from `powerbi/dax_measures.dax`, then:

- Relationship: `Date[Date]` 1-to-many `Sales[OrderDate]`
- Mark `Date` as date table using `Date[Date]`
- Sort `Date[Month]` by `Date[Month No]`

## 3. Measures

Create these core DAX measures from `powerbi/dax_measures.dax`:

- `Total Revenue`
- `Total Profit`
- `Profit Margin`
- `Total Orders`
- `Avg Order Value`
- `Customer Count`
- `Repeat Customer`
- `Avg Customer Spend`

## 4. Page 1 - Executive Overview

Top KPI cards:

- Revenue
- Profit
- Margin
- Orders
- AOV

Main visuals:

- Line chart: `Date[Date]` vs `Total Revenue`
- Clustered bar chart: `Sales[ProductCategory]` vs `Total Revenue`
- Treemap or filled map: `Sales[Region]` / `Sales[StoreLocation]` vs `Total Profit`

Suggested insight text:

- Coffee and Tea are the two main revenue engines.
- Manhattan contributes the largest estimated profit because it includes two store locations.
- Revenue trend covers 2023-01-01 to 2023-06-30, so forecast should be treated as short-horizon.

## 5. Page 2 - Product Performance

Visuals:

- Table: `ProductName`, `ProductCategory`, `Total Revenue`, `Total Profit`, `Total Quantity`, `Profit Margin`
- Bar chart: Top 10 products by `Total Revenue`
- Scatter chart: `Total Revenue` vs `Profit Margin`, size by `Total Quantity`

Insights to look for:

- High revenue but low margin products
- Dead products with low revenue and low quantity
- Best sellers by revenue and quantity

## 6. Page 3 - Customer Analytics

KPI cards:

- Repeat Customer
- Customer Count
- Avg Customer Spend

Visuals:

- Bar chart: `Segment` vs `Total Revenue`
- Matrix: `Segment`, `Customer Count`, `Avg Customer Spend`, `Profit Margin`
- Donut chart: revenue share by `Segment`

Important note:

`CustomerID` is simulated because the Kaggle source file does not include real customer identifiers.

## 7. Page 4 - Sales Forecast

Visual:

- Line chart: `Date[Date]` vs `Total Revenue`
- In Analytics pane, add Forecast
- Forecast length: 3 months or 6 months
- Confidence interval: 95%

Use daily or monthly granularity. Monthly is cleaner because the source data only spans six months.

## 8. Slicers

Add slicers to each page:

- Region
- ProductCategory
- Segment
- Date
- StoreLocation

Sync slicers across pages when useful.

## 9. Design

Import `powerbi/theme_retail_corporate.json`.

Layout:

- KPI row at the top
- Charts in the middle
- Insight text boxes at the bottom
- Corporate colors: dark blue, white, gray, with green/orange/red accents for performance states
