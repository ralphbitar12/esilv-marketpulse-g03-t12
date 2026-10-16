# TD2 - Answers

1. `load_instruments()`
   - This function reads the JSON file.
   - It loads the instrument and benchmark information.

2. `load_prices()`
   - This function reads the CSV file.
   - It loads all the market prices.

3. `filter_prices(prices, ticker)`
   - This function selects only one ticker.
   - It keeps only the rows for the chosen asset.

4. `main()`
   - This is the main function.
   - It coordinates the whole program and calls the other functions.

5. The input files are stored in `data/sample/`.

So:
- JSON → `load_instruments()`
- CSV → `load_prices()`
- One ticker selection → `filter_prices(prices, ticker)`
- Execution control → `main()`
- Files folder → `data/sample/`
