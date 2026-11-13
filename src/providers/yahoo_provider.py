"""Yahoo Finance provider (TD08)."""

import yfinance as yf

CANONICAL_TO_YAHOO = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def fetch_yahoo_prices(canonical_ticker, lookback="1mo", interval="1d"):
    if canonical_ticker not in CANONICAL_TO_YAHOO:
        raise ValueError(f"Unknown canonical ticker: {canonical_ticker}")

    yahoo_symbol = CANONICAL_TO_YAHOO[canonical_ticker]
    raw = yf.Ticker(yahoo_symbol).history(period=lookback, interval=interval)

    rows = []
    for date, row in raw.iterrows():
        rows.append({
            "date": date.strftime("%Y-%m-%d"),
            "ticker": canonical_ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        })

    return sorted(rows, key=lambda r: r["date"])