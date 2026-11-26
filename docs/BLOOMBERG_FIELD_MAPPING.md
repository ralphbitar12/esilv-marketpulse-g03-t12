# Bloomberg Field Mapping (TD09)

## Access mode

Field mnemonics were observed LIVE on the classroom Bloomberg Terminal
(BLOOM-A501), via the FLDS screen, on 2026-11-26.

## Identifier mapping

| MarketPulse canonical | Bloomberg identifier |
|---|---|
| AAPL  | AAPL US Equity |
| SP500 | SPX Index      |

Canonical tickers remain AAPL and SP500 everywhere outside the provider.

## Field mapping

| Canonical | Bloomberg mnemonic | AAPL US Equity | SPX Index |
|---|---|---|---|
| open   | PX_OPEN   | 353.475    | 7060.33   |
| high   | PX_HIGH   | 356.75     | 7199.31   |
| low    | PX_LOW    | 345.13     | 6970.11   |
| close  | PX_LAST   | 355.58     | 7182.78   |
| volume | PX_VOLUME | 54 285 255 | 952.87MLN |

Values observed on 2026-11-25 session.

## Missing or special fields

- `PX_SETTLE` returns `N.A.` on SPX Index: not available, not used.


