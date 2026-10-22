from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance,
)

DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


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


def display_market_summary(title, instrument, prices):
    print(f"=== {title} ===")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Market       : {instrument.get('market', 'N/A')}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(f"First close  : {float(prices[0]['close']):.2f} {instrument['currency']}")
    print(f"Last close   : {float(prices[-1]['close']):.2f} {instrument['currency']}\n")


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    print("=== MarketPulse ===\n")

    display_market_summary("Instrument", instrument, instrument_prices)
    display_market_summary("Benchmark", benchmark, benchmark_prices)

    # TD07: Alignment and Comparative Analytics
    aligned_inst, aligned_bench = align_series(instrument_prices, benchmark_prices)

    inst_ret = calculate_period_return(aligned_inst)
    bench_ret = calculate_period_return(aligned_bench)
    rel_perf = calculate_relative_performance(inst_ret, bench_ret)

    inst_base_100 = calculate_base_100(aligned_inst)
    bench_base_100 = calculate_base_100(aligned_bench)

    print("Comparison (aligned)")
    print(f"Aligned sessions         : {len(aligned_inst)}")
    print(f"{instrument['ticker']} period return       : {inst_ret:+.2f}%")
    print(f"{benchmark['ticker']} period return      : {bench_ret:+.2f}%")
    print(f"Relative performance     : {rel_perf:+.2f} percentage points\n")

    print("Base 100")
    print(f"{instrument['ticker']}   : {inst_base_100[0]['value']:.2f} -> {inst_base_100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']}  : {bench_base_100[0]['value']:.2f} -> {bench_base_100[-1]['value']:.2f}\n")

    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")


if __name__ == "__main__":
    main()