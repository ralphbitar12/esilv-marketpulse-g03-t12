"""Bloomberg provider

Access mode: APPROVED_SAMPLE.
Field mapping source: docs/BLOOMBERG_FIELD_MAPPING.md
"""

import json
from pathlib import Path

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

SAMPLE_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "data" / "sample" / "bloomberg_reference_sample.json"
)


def fetch_raw_bloomberg_history(canonical_ticker):
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(f"Unsupported canonical ticker: {canonical_ticker}")

    with open(SAMPLE_PATH, encoding="utf-8") as f:
        data = json.load(f)

    for serie in data["series"]:
        if serie["canonical_ticker"] == canonical_ticker:
            return serie

    raise ValueError(f"No Bloomberg series for canonical ticker: {canonical_ticker}")


def normalize_bloomberg_history(raw_series, canonical_ticker):
    rows = []
    for observation in raw_series["observations"]:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return sorted(rows, key=lambda r: r["date"])


def fetch_bloomberg_prices(canonical_ticker):
    raw_series = fetch_raw_bloomberg_history(canonical_ticker)
    return normalize_bloomberg_history(raw_series, canonical_ticker)