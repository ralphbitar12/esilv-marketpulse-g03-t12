from pathlib import Path
import csv
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance,
)
from src.providers.yahoo_provider import fetch_yahoo_prices
from src.providers.bloomberg_provider import fetch_bloomberg_prices


DATA_DIR = Path("data/sample")

PROVIDER = "bloomberg"  # "bloomberg", "yahoo" or "csv"
LOOKBACK = "1mo"
INTERVAL = "1d"

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"

PROVIDER_LABELS = {
    "bloomberg": "Bloomberg stage",
    "yahoo": "Yahoo Finance",
    "csv": "CSV",
}
PROVIDER_LABEL = PROVIDER_LABELS[PROVIDER]

# Honest access mode. The Bloomberg path reads an instructor-approved fixture,
# it does NOT prove live Bloomberg connectivity.
ACCESS_MODES = {
    "bloomberg": "APPROVED_SAMPLE",
    "yahoo": "LIVE",
    "csv": "LOCAL_FILE",
}
ACCESS_MODE = ACCESS_MODES[PROVIDER]


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


def load_provider_prices(ticker):
    if PROVIDER == "bloomberg":
        return fetch_bloomberg_prices(ticker)
    if PROVIDER == "yahoo":
        return fetch_yahoo_prices(ticker, LOOKBACK, INTERVAL)
    if PROVIDER == "csv":
        return filter_prices(load_prices(), ticker)
    raise ValueError(f"Unsupported provider: {PROVIDER}")


def build_market_snapshot():
    """Shared application result consumed by the terminal path and by TD11."""
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = load_provider_prices(instrument["ticker"])
    benchmark_prices = load_provider_prices(benchmark["ticker"])

    if not instrument_prices:
        raise ValueError("Instrument rows are empty.")
    if not benchmark_prices:
        raise ValueError("Benchmark rows are empty.")

    aligned_instrument, aligned_benchmark = align_series(instrument_prices, benchmark_prices)
    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(instrument_return, benchmark_return)
    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    return {
        "provider": PROVIDER_LABEL,
        "access_mode": ACCESS_MODE,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_prices": instrument_prices,
        "benchmark_prices": benchmark_prices,
        "aligned_instrument": aligned_instrument,
        "aligned_benchmark": aligned_benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }


def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_prices = snapshot["instrument_prices"]
    benchmark_prices = snapshot["benchmark_prices"]
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
    print(f"First close  : {float(instrument_prices[0]['close']):.2f} {instrument['currency']}")
    print(f"Last close   : {float(instrument_latest['close']):.2f} {instrument['currency']}")
    print()

    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Market       : {benchmark.get('market', 'N/A')}")
    print(f"Observations : {len(benchmark_prices)}")
    print(f"First date   : {get_first_date(benchmark_prices)}")
    print(f"Last date    : {get_last_date(benchmark_prices)}")
    print(f"First close  : {float(benchmark_prices[0]['close']):.2f}")
    print(f"Last close   : {float(benchmark_latest['close']):.2f}")
    print()

    print(f"Period: {snapshot['lookback']}")
    print(f"Interval: {snapshot['interval']}")
    print(f"Provider: {snapshot['provider']}")
    print(f"Access mode: {snapshot['access_mode']}")
    print()

    aligned_instrument = snapshot["aligned_instrument"]
    instrument_return = snapshot["instrument_return"]
    benchmark_return = snapshot["benchmark_return"]
    relative_performance = snapshot["relative_performance"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print("Comparison (aligned)")
    print(f"Aligned sessions     : {len(aligned_instrument)}")
    print(f"{instrument['ticker']} period return  : {instrument_return:+.2f}%")
    print(f"{benchmark['ticker']} period return : {benchmark_return:+.2f}%")
    print(f"Relative performance : {relative_performance:+.2f} percentage points")
    print()

    print("Base 100")
    print(f"{instrument['ticker']}  : {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']} : {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")


if __name__ == "__main__":
    main()