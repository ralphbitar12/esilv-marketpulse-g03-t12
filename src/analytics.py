"""MarketPulse analytics: pure functions for comparison (TD07)."""


def index_by_date(prices):
    return {row["date"]: row for row in prices}
 # Owner: Ralph


def align_series(instrument_prices, benchmark_prices):
    inst_by_date = index_by_date(instrument_prices)
    bench_by_date = index_by_date(benchmark_prices)


    common_dates = sorted(set(inst_by_date.keys()) & set(bench_by_date.keys()))


    aligned_instrument = [inst_by_date[d] for d in common_dates]
    aligned_benchmark = [bench_by_date[d] for d in common_dates]


    return aligned_instrument, aligned_benchmark
 # Owner: Ralph

def calculate_period_return(prices):
    raise NotImplementedError  # Owner: Thomas


def calculate_base_100(prices):
    raise NotImplementedError  # Owner: Thomas


def calculate_relative_performance(instrument_return, benchmark_return):
    raise NotImplementedError  # Owner: Thomas