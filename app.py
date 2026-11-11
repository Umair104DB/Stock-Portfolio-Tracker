import csv
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "stock_price_reference.csv"
OUTPUT_FILE = Path(__file__).parent / "portfolio_summary.csv"


def load_prices():
    prices = {}
    with DATA_FILE.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            prices[row["symbol"].upper()] = float(row["price_usd"])
    return prices


def main():
    prices = load_prices()
    portfolio = {}
    print("Stock Portfolio Tracker. Prices are fixed demo values in USD.")
    print("Available symbols:", ", ".join(sorted(prices)))
    while True:
        symbol = input("Enter stock symbol (or DONE): ").strip().upper()
        if symbol == "DONE":
            break
        if symbol not in prices:
            print("Symbol not found. Choose one from the list.")
            continue
        try:
            quantity = float(input("Enter quantity: "))
            if quantity <= 0:
                raise ValueError
        except ValueError:
            print("Quantity must be a positive number.")
            continue
        portfolio[symbol] = portfolio.get(symbol, 0) + quantity
    total = 0.0
    rows = []
    print("\nPORTFOLIO SUMMARY")
    for symbol, quantity in sorted(portfolio.items()):
        value = quantity * prices[symbol]
        total += value
        rows.append([symbol, quantity, prices[symbol], round(value, 2)])
        print(f"{symbol}: {quantity:g} shares × ${prices[symbol]:.2f} = ${value:,.2f}")
    print(f"Total investment value: ${total:,.2f}")
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["symbol", "quantity", "price_usd", "market_value_usd"])
        writer.writerows(rows)
    print(f"Saved portfolio to {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
