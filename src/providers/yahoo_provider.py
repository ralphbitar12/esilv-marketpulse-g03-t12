import yfinance as yf

CANONICAL_TO_YAHOO = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def fetch_yahoo_prices(canonical_ticker, lookback="1mo", interval="1d"):
    if canonical_ticker not in CANONICAL_TO_YAHOO:
        raise ValueError(f"Unsupported canonical ticker: {canonical_ticker}")

    yahoo_symbol = CANONICAL_TO_YAHOO[canonical_ticker]
    raw = yf.download(
        yahoo_symbol,
        period=lookback,
        interval=interval,
        progress=False,
        auto_adjust=False,
    )

    if raw.empty:
        return []

    # Flatten MultiIndex columns if yfinance returns (Price, Ticker) tuples
    if hasattr(raw.columns, "nlevels") and raw.columns.nlevels > 1:
        raw.columns = raw.columns.get_level_values(0)

    rows = []
    for idx, row in raw.iterrows():
        date_str = idx.strftime("%Y-%m-%d")
        volume_val = row["Volume"]
        volume_int = int(volume_val) if volume_val == volume_val else 0

        rows.append({
            "date": date_str,
            "ticker": canonical_ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": volume_int,
        })

    rows.sort(key=lambda r: r["date"])
    return rows