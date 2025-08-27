# Tradelog

A simple, local-first trade journal for analyzing your performance.

## Structure
- `data/`: CSV trades
- `notebooks/`: analysis notebooks
- `outputs/`: exported charts/tables

## CSV Schema
Required columns in `data/trades_template.csv`:
```
trade_id,open_datetime,close_datetime,symbol,asset_class,side,qty,entry_price,exit_price,fees,account,setup,rr_plan,rr_realized,stop_loss,take_profit,notes
```
- `side`: BUY or SELL
- `asset_class`: stock, forex, crypto, futures, options
- Date format: `YYYY-MM-DD HH:MM`

## Setup
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```
jupyter lab
```
Open `notebooks/Trade_Analysis_Clean.ipynb`.

## KPIs
- Win rate, average R, expectancy, profit factor
- Drawdown, equity curve
- Best/worst setups and symbols

## Notes
- Add your trades as new rows or copy your own CSV to `data/`.
- Ensure numeric columns have proper decimals; avoid thousands separators.
