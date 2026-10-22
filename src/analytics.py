def index_by_date(prices):
    return {row["date"]: row for row in prices}


def align_series(instrument_prices, benchmark_prices):
    inst_by_date = index_by_date(instrument_prices)
    bench_by_date = index_by_date(benchmark_prices)

    common_dates = sorted(set(inst_by_date.keys()) & set(bench_by_date.keys()))

    aligned_instrument = [inst_by_date[d] for d in common_dates]
    aligned_benchmark = [bench_by_date[d] for d in common_dates]

    return aligned_instrument, aligned_benchmark


def calculate_period_return(prices):
    if not prices:
        raise ValueError("Cannot calculate period return on an empty series.")

    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])

    if first_close == 0.0:
        raise ValueError("First close cannot be zero.")

    return ((last_close / first_close) - 1.0) * 100.0


def calculate_base_100(prices):
    if not prices:
        raise ValueError("Cannot calculate base-100 on an empty series.")

    first_close = float(prices[0]["close"])
    if first_close == 0.0:
        raise ValueError("First close cannot be zero.")

    base_100_series = []
    for row in prices:
        current_close = float(row["close"])
        val = (current_close / first_close) * 100.0
        base_100_series.append({
            "date": row["date"],
            "ticker": row["ticker"],
            "value": val,
        })

    return base_100_series


def calculate_relative_performance(instrument_return, benchmark_return):
    return instrument_return - benchmark_return