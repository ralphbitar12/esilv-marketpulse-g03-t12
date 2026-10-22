"""MarketPulse analytics: pure functions for comparison (TD07)."""


def index_by_date(prices):
    raise NotImplementedError  # Owner: Ralph


def align_series(instrument_prices, benchmark_prices):
    raise NotImplementedError  # Owner: Ralph


def calculate_period_return(prices):
	if not prices:
		raise ValueError("Cannot calculate period return on an empty series.")

	first_close = float(prices[0]["close"])
	last_close = float(prices[-1]["close"])

	if first_close == 0.0:
		raise ValueError("First close cannot be zero.")

	return ((last_close / first_close) - 1.0) * 100.0
# Owner: Thomas


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
# Owner: Thomas


def calculate_relative_performance(instrument_return, benchmark_return):
	return instrument_return - benchmark_return
# Owner: Thomas