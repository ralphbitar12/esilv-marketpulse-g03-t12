from pathlib import Path
import csv
import json


DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
PROVIDER_LABEL = "CSV"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]

    print("=== MarketPulse ===")
    print()

    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Market       : {instrument.get('market', 'N/A')}")
    print(f"Observations : {len(instrument_prices)}")
    print(f"First date   : {get_first_date(instrument_prices)}")
    print(f"Last date    : {get_last_date(instrument_prices)}")
    print(f"First close  : {instrument_prices[0]['close']} {instrument['currency']}")
    print(f"Last close   : {instrument_latest['close']} {instrument['currency']}")
    print()

    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Market       : {benchmark.get('market', 'N/A')}")
    print(f"Observations : {len(benchmark_prices)}")
    print(f"First date   : {get_first_date(benchmark_prices)}")
    print(f"Last date    : {get_last_date(benchmark_prices)}")
    print(f"First close  : {benchmark_prices[0]['close']}")
    print(f"Last close   : {benchmark_latest['close']}")
    print()

    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print(f"Provider: {PROVIDER_LABEL}")

if __name__ == "__main__":
    main()