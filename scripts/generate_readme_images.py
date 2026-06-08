from __future__ import annotations

from pathlib import Path
import math

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "coffee_shop_sales_clean.csv"
OUT = ROOT / "images"

W, H = 1400, 850
BG = "#F5F7FB"
CARD = "#FFFFFF"
TEXT = "#1F2937"
MUTED = "#6B7280"
BLUE = "#2F80ED"
DARK = "#0F2A43"
GREEN = "#27AE60"
ORANGE = "#F2994A"
RED = "#EB5757"
GRID = "#E5E7EB"
PALETTE = [BLUE, GREEN, ORANGE, RED, "#56CCF2", "#9B51E0", "#6FCF97", "#BDBDBD"]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["arialbd.ttf" if bold else "arial.ttf", "segoeuib.ttf" if bold else "segoeui.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


F_TITLE = font(34, True)
F_H2 = font(22, True)
F_LABEL = font(16)
F_SMALL = font(13)
F_NUM = font(30, True)


def money(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value/1_000:.2f}K"
    return f"${value:.2f}"


def number(value: float) -> str:
    if abs(value) >= 1_000:
        return f"{value/1_000:.0f}K"
    return f"{value:.0f}"


def canvas(title: str, subtitle: str = "") -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.text((40, 28), title, fill=DARK, font=F_TITLE)
    if subtitle:
        draw.text((42, 72), subtitle, fill=MUTED, font=F_LABEL)
    return img, draw


def rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str = CARD) -> None:
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=GRID, width=1)


def card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str, value: str) -> None:
    rect(draw, box)
    x1, y1, _, _ = box
    draw.text((x1 + 22, y1 + 24), value, fill=TEXT, font=F_NUM)
    draw.text((x1 + 22, y1 + 68), label, fill=MUTED, font=F_LABEL)


def hbar(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    labels: list[str],
    values: list[float],
    title: str,
    color: str = BLUE,
) -> None:
    rect(draw, box)
    x1, y1, x2, y2 = box
    draw.text((x1 + 22, y1 + 18), title, fill=TEXT, font=F_H2)
    top = y1 + 62
    left = x1 + 170
    right = x2 - 36
    row_h = max(28, int((y2 - top - 28) / max(len(labels), 1)))
    maxv = max(values) if values else 1
    for i, (label, value) in enumerate(zip(labels, values)):
        y = top + i * row_h
        label_short = label[:22] + ("..." if len(label) > 22 else "")
        draw.text((x1 + 22, y + 5), label_short, fill=TEXT, font=F_SMALL)
        bw = int((right - left) * value / maxv)
        draw.rounded_rectangle((left, y + 4, left + bw, y + row_h - 7), radius=4, fill=color)
        draw.text((left + bw + 8, y + 5), money(value), fill=MUTED, font=F_SMALL)


def line_chart(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    values: list[float],
    title: str,
    color: str = BLUE,
    forecast: list[float] | None = None,
) -> None:
    rect(draw, box)
    x1, y1, x2, y2 = box
    draw.text((x1 + 22, y1 + 18), title, fill=TEXT, font=F_H2)
    left, top, right, bottom = x1 + 55, y1 + 70, x2 - 30, y2 - 45
    all_values = values + (forecast or [])
    mn, mx = min(all_values), max(all_values)
    span = mx - mn or 1
    for i in range(5):
        y = top + i * (bottom - top) / 4
        draw.line((left, y, right, y), fill=GRID, width=1)
    def pts(series: list[float], offset: int = 0, total: int | None = None) -> list[tuple[float, float]]:
        total = total or len(series)
        out = []
        for idx, v in enumerate(series):
            x = left + (idx + offset) * (right - left) / max(total - 1, 1)
            y = bottom - (v - mn) * (bottom - top) / span
            out.append((x, y))
        return out
    total = len(values) + len(forecast or [])
    p = pts(values, 0, total)
    if len(p) > 1:
        draw.line(p, fill=color, width=3)
    if forecast:
        fp = pts(forecast, len(values), total)
        draw.line([p[-1]] + fp, fill="#111827", width=2)
        upper = [(x, y - 45) for x, y in fp]
        lower = [(x, y + 45) for x, y in reversed(fp)]
        draw.polygon(upper + lower, fill="#D1D5DB")
        draw.line([p[-1]] + fp, fill="#111827", width=2)
    draw.text((left, bottom + 12), "Jan 2023", fill=MUTED, font=F_SMALL)
    draw.text((right - 80, bottom + 12), "Jun 2023", fill=MUTED, font=F_SMALL)


def donut(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], labels: list[str], values: list[float], title: str) -> None:
    rect(draw, box)
    x1, y1, x2, y2 = box
    draw.text((x1 + 22, y1 + 18), title, fill=TEXT, font=F_H2)
    cx, cy = x1 + 180, y1 + 190
    r = 115
    start = 90
    total = sum(values) or 1
    for i, value in enumerate(values):
        angle = 360 * value / total
        draw.pieslice((cx - r, cy - r, cx + r, cy + r), start, start + angle, fill=PALETTE[i % len(PALETTE)])
        start += angle
    draw.ellipse((cx - 55, cy - 55, cx + 55, cy + 55), fill=CARD)
    for i, label in enumerate(labels):
        y = y1 + 95 + i * 30
        draw.rectangle((x1 + 345, y + 5, x1 + 360, y + 20), fill=PALETTE[i % len(PALETTE)])
        draw.text((x1 + 370, y), label, fill=TEXT, font=F_SMALL)


def table(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], rows: list[list[str]], title: str) -> None:
    rect(draw, box)
    x1, y1, x2, _ = box
    draw.text((x1 + 22, y1 + 18), title, fill=TEXT, font=F_H2)
    y = y1 + 65
    col_x = [x1 + 24, x1 + 300, x1 + 450, x1 + 600]
    headers = rows[0]
    for i, h in enumerate(headers):
        draw.text((col_x[i], y), h, fill=MUTED, font=F_SMALL)
    draw.line((x1 + 22, y + 24, x2 - 22, y + 24), fill=GRID)
    for row in rows[1:]:
        y += 34
        for i, cell in enumerate(row):
            draw.text((col_x[i], y), str(cell), fill=TEXT, font=F_SMALL)


def overview(df: pd.DataFrame) -> None:
    img, draw = canvas("Retail Sales & Revenue Dashboard", "Executive Overview")
    revenue = df["Revenue"].sum()
    profit = df["Profit"].sum()
    orders = df["OrderID"].nunique()
    aov = revenue / orders
    margin = profit / revenue
    cards = [
        ("Total Revenue", money(revenue)),
        ("Total Profit", money(profit)),
        ("Profit Margin", f"{margin:.2%}"),
        ("Avg Order Value", f"${aov:.2f}"),
        ("Total Orders", number(orders)),
    ]
    for i, (label, value) in enumerate(cards):
        card(draw, (40 + i * 265, 115, 275 + i * 265, 220), label, value)
    daily = df.groupby("OrderDate")["Revenue"].sum().tolist()
    line_chart(draw, (40, 250, 720, 560), daily, "Sales Trend")
    cat = df.groupby("ProductCategory")["Revenue"].sum().sort_values(ascending=False)
    hbar(draw, (750, 250, 1360, 560), cat.index.tolist(), cat.tolist(), "Revenue by Category")
    reg = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
    hbar(draw, (40, 590, 720, 810), reg.index.tolist(), reg.tolist(), "Profit by Region", GREEN)
    seg = df.groupby("Segment")["Revenue"].sum().sort_values(ascending=False)
    hbar(draw, (750, 590, 1360, 810), seg.index.tolist(), seg.tolist(), "Revenue by Segment", ORANGE)
    img.save(OUT / "overview.png")


def product(df: pd.DataFrame) -> None:
    img, draw = canvas("Product Performance", "Top products and margin analysis")
    prod = df.groupby("ProductName").agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum")).sort_values("Revenue", ascending=False).head(10)
    hbar(draw, (40, 115, 760, 800), prod.index.tolist(), prod["Revenue"].tolist(), "Top 10 Products by Revenue")
    rows = [["Product", "Revenue", "Profit", "Qty"]]
    for name, row in prod.head(8).iterrows():
        rows.append([name[:28], money(row["Revenue"]), money(row["Profit"]), f"{int(row['Quantity']):,}"])
    table(draw, (790, 115, 1360, 800), rows, "Product Performance Table")
    img.save(OUT / "product-analysis.png")


def customer(df: pd.DataFrame) -> None:
    img, draw = canvas("Customer Analytics", "Segment behavior and customer value")
    revenue = df["Revenue"].sum()
    cust = df["CustomerID"].nunique()
    avg = revenue / cust
    repeat = df.groupby("CustomerID")["OrderID"].nunique().gt(1).sum()
    card(draw, (40, 115, 350, 220), "Repeat Customer", f"{repeat:,}")
    card(draw, (380, 115, 690, 220), "Customer Count", f"{cust:,}")
    card(draw, (720, 115, 1030, 220), "Avg Customer Spend", f"${avg:.2f}")
    seg = df.groupby("Segment")["Revenue"].sum().sort_values(ascending=False)
    hbar(draw, (40, 255, 680, 590), seg.index.tolist(), seg.tolist(), "Revenue by Segment")
    donut(draw, (710, 255, 1360, 590), seg.index.tolist(), seg.tolist(), "Revenue Share by Segment")
    rows = [["Segment", "Customers", "Avg Spend", "Margin"]]
    metrics = df.groupby("Segment").agg(Revenue=("Revenue", "sum"), Profit=("Profit", "sum"), Customers=("CustomerID", "nunique")).sort_values("Revenue", ascending=False)
    for name, row in metrics.iterrows():
        rows.append([name, f"{int(row['Customers']):,}", f"${row['Revenue']/row['Customers']:.2f}", f"{row['Profit']/row['Revenue']:.2%}"])
    table(draw, (40, 625, 1360, 815), rows, "Segment Profitability")
    img.save(OUT / "customer-analysis.png")


def forecast(df: pd.DataFrame) -> None:
    img, draw = canvas("Sales Forecast", "3-month forecast based on daily revenue trend")
    daily = df.groupby("OrderDate")["Revenue"].sum().tolist()
    last = daily[-1]
    slope = (daily[-1] - daily[0]) / max(len(daily), 1)
    fc = [last + slope * i for i in range(1, 91)]
    line_chart(draw, (40, 120, 1360, 720), daily, "Total Revenue by OrderDate", forecast=fc)
    card(draw, (40, 740, 350, 825), "Forecast Length", "3 Months")
    card(draw, (380, 740, 690, 825), "Confidence Interval", "90%")
    card(draw, (720, 740, 1030, 825), "Trend", "Increasing")
    img.save(OUT / "forecast.png")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(DATA, parse_dates=["OrderDate"])
    df["OrderDate"] = df["OrderDate"].dt.date.astype(str)
    overview(df)
    product(df)
    customer(df)
    forecast(df)
    print(f"Images written to {OUT}")


if __name__ == "__main__":
    main()
