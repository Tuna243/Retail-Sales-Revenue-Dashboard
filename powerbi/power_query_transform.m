let
    Source = Csv.Document(
        File.Contents("E:\Workspace\Project\Retail-Sales-Revenue-Dashboard\data\processed\coffee_shop_sales_clean.csv"),
        [Delimiter = ",", Columns = 25, Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    ChangedTypes = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"OrderID", Int64.Type},
            {"OrderDate", type date},
            {"OrderTime", type time},
            {"Quantity", Int64.Type},
            {"StoreID", Int64.Type},
            {"StoreLocation", type text},
            {"City", type text},
            {"Region", type text},
            {"CustomerID", type text},
            {"Segment", type text},
            {"ProductID", Int64.Type},
            {"ProductCategory", type text},
            {"ProductType", type text},
            {"ProductName", type text},
            {"UnitPrice", Currency.Type},
            {"Revenue", Currency.Type},
            {"EstimatedCost", Currency.Type},
            {"Profit", Currency.Type},
            {"ProfitRate", Percentage.Type},
            {"Year", Int64.Type},
            {"MonthNo", Int64.Type},
            {"MonthName", type text},
            {"YearMonth", type text},
            {"Weekday", type text},
            {"Hour", Int64.Type}
        }
    ),
    RemovedBlankRows = Table.SelectRows(ChangedTypes, each not List.IsEmpty(List.RemoveMatchingItems(Record.FieldValues(_), {"", null}))),
    RemovedDuplicates = Table.Distinct(RemovedBlankRows, {"OrderID"})
in
    RemovedDuplicates
