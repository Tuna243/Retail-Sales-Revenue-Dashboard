# Open in Power BI

Do not open the generated `.pbip` files first. They are source-control scaffolds and can trigger Power BI Desktop May 2026 errors such as:

- `Missing_References`
- `Cannot read properties of undefined (reading 'customTheme')`
- `Non-null assertion failure: query`

Use the data-source shortcut instead:

```text
powerbi/Retail Sales Revenue Dashboard/coffee_shop_sales_clean.pbids
```

## Steps

1. Double-click `coffee_shop_sales_clean.pbids`.
2. In Power BI Desktop Navigator, select `coffee_shop_sales_clean.csv`.
3. Click `Load`.
4. Rename the table to `Sales`.
5. Add measures from `powerbi/dax_measures.dax`.
6. Build visuals using `docs/dashboard_build_guide.md`.
7. Save the completed report as `.pbix`.

## Core visuals

- Card: `Total Revenue`
- Card: `Total Profit`
- Card: `Profit Margin`
- Card: `Total Orders`
- Card: `Avg Order Value`
- Line chart: `OrderDate` by `Total Revenue`
- Bar chart: `ProductCategory` by `Total Revenue`
- Treemap: `Region` by `Total Profit`
