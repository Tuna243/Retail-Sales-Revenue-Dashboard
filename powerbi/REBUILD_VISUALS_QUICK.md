# Rebuild Power BI Visuals Quickly

After loading `coffee_shop_sales_clean.pbids`, rename the table to `Sales`, then create the measures from `powerbi/dax_measures.dax`.

## Page 1 - Executive Overview

Create 5 Card visuals at the top:

| Visual | Field |
| --- | --- |
| Card | `Total Revenue` |
| Card | `Total Profit` |
| Card | `Profit Margin` |
| Card | `Total Orders` |
| Card | `Avg Order Value` |

Create these charts:

| Visual | Axis / Group | Values |
| --- | --- | --- |
| Line chart | `OrderDate` | `Total Revenue` |
| Clustered bar chart | `ProductCategory` | `Total Revenue` |
| Treemap | `Region` | `Total Profit` |
| Bar chart | `Segment` | `Total Revenue` |

Add slicers:

- `Region`
- `ProductCategory`
- `Segment`
- `OrderDate`

## Page 2 - Product Performance

Create a Table visual:

- `ProductName`
- `ProductCategory`
- `Total Revenue`
- `Total Profit`
- `Total Quantity`
- `Profit Margin`

Create charts:

| Visual | Axis / Details | Values |
| --- | --- | --- |
| Bar chart | `ProductName` | `Total Revenue` |
| Scatter chart | Details: `ProductName`; X: `Total Revenue`; Y: `Profit Margin`; Size: `Total Quantity` |

For the product bar chart, apply visual filter:

- Filter type: `Top N`
- Show items: `Top 10`
- By value: `Total Revenue`

## Page 3 - Customer Analytics

Create 3 Card visuals:

| Visual | Field |
| --- | --- |
| Card | `Repeat Customer` |
| Card | `Customer Count` |
| Card | `Avg Customer Spend` |

Create charts:

| Visual | Axis / Legend | Values |
| --- | --- | --- |
| Bar chart | `Segment` | `Total Revenue` |
| Donut chart | `Segment` | `Total Revenue` |
| Matrix | Rows: `Segment`; Values: `Customer Count`, `Avg Customer Spend`, `Profit Margin` |

## Page 4 - Sales Forecast

Create a Line chart:

- X-axis: `OrderDate`
- Y-axis: `Total Revenue`

Then open the Analytics pane:

- Forecast: On
- Length: `3 months`
- Confidence interval: `95%`

## Formatting

Import theme:

```text
powerbi/theme_retail_corporate.json
```

Suggested layout:

- KPI cards on top
- Main charts in the middle
- Slicers on the left or top
- Insight text boxes at the bottom
