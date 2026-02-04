# CLAUDE.md - Trade Log Analyzer

## Project Overview

Trade Log Analyzer is a Python-based tool for analyzing trading performance. It loads trade data from CSV files and provides KPI calculations, interactive visualizations, and HTML report generation. Documentation and UI strings are in **Italian**.

**Package**: `trade-log-analyzer` v1.0.0
**License**: MIT
**Python**: >= 3.8

## Repository Structure

```
tradelog/
├── src/
│   ├── trade_analyzer.py    # Core analysis engine (TradeAnalyzer class)
│   ├── app.py               # Streamlit web application
│   └── main.py              # CLI entry point
├── test_analyzer.py          # Integration test/demo script
├── tradelog_sample.csv       # Sample CSV with 5 example trades
├── run_analyzer.sh           # Bash launcher (web/cli/test modes)
├── setup.py                  # Package configuration
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation (Italian)
└── QUICKSTART.md             # Quick start guide (Italian)
```

## Architecture

### Data Pipeline

```
CSV File -> load_trades() -> _calculate_trade_metrics() -> calculate_kpis() -> visualizations/reports
```

### Core Class: `TradeAnalyzer` (`src/trade_analyzer.py`)

Single-class architecture. All analysis logic lives in `TradeAnalyzer`:

- **`load_trades(csv_file)`** - Load and parse CSV, create datetime column
- **`_calculate_trade_metrics()`** - Compute P&L, returns, R-multiple, win/loss classification
- **`calculate_kpis()`** - Full KPI suite: win rate, payoff ratio, drawdown, Sharpe ratio, strategy breakdown
- **`_calculate_max_drawdown()`** - Cumulative P&L peak-to-trough analysis
- **`_calculate_sharpe_ratio()`** - Simplified Sharpe (mean/std of net P&L)
- **`print_summary()`** - Console output of all KPIs
- **`plot_equity_curve(save_path)`** - Plotly line chart of cumulative P&L
- **`plot_returns_distribution(save_path)`** - 2x2 subplot grid (returns hist, R-multiple hist, win/loss bar, P&L scatter)
- **`export_analysis(filename)`** - Full HTML report with embedded Plotly charts

### Entry Points

1. **Web app** (`src/app.py`): Streamlit app with file upload, KPI dashboard, 4 tabs (Equity Curve, Distributions, Trade Data, Strategies), filtering, and HTML export
2. **CLI** (`src/main.py`): Accepts CSV path as argv[1], defaults to `../tradelog_sample.csv`, outputs HTML files
3. **Launcher** (`run_analyzer.sh`): Wrapper script with `web`, `cli`, and `test` modes; auto-creates virtualenv

### CSV Format (13 columns + 1 optional)

```
date, time, symbol, side, entry_price, exit_price, quantity, commission,
notes, strategy, timeframe, stop_loss, take_profit, exit_reason
```

`side` values: `BUY`, `SELL`
`exit_reason` values: `TAKE_PROFIT`, `STOP_LOSS`, `MANUAL`

## How to Run

```bash
# Web app (Streamlit)
./run_analyzer.sh web
# or: cd src && streamlit run app.py

# CLI analysis
./run_analyzer.sh cli                    # uses sample data
./run_analyzer.sh cli my_trades.csv      # custom CSV

# Tests
./run_analyzer.sh test
# or: python test_analyzer.py
```

## Dependencies

| Package | Purpose |
|---------|---------|
| pandas | Data loading, manipulation, aggregation |
| numpy | Numerical operations |
| plotly | Interactive visualizations (equity curves, distributions) |
| streamlit | Web application framework |
| matplotlib | Imported but not actively used in current code |
| seaborn | Imported but not actively used in current code |
| dash, dash-bootstrap-components | Listed but not used in current code |

**Note**: `sqlite3` and `datetime` in `requirements.txt` are stdlib modules and should not be listed.

## Testing

There is no formal test framework (no pytest/unittest). `test_analyzer.py` is an integration/demo script that:

1. Loads `tradelog_sample.csv`
2. Calculates KPIs
3. Generates HTML outputs: `test_equity_curve.html`, `test_distributions.html`, `test_report.html`
4. Prints results to console with emoji status indicators

Run from project root: `python test_analyzer.py`

Verification is manual - check console output and generated HTML files.

## Code Conventions

### Style
- PEP-8 naming: `snake_case` for functions/variables, `PascalCase` for classes
- Private methods prefixed with `_` (e.g., `_calculate_max_drawdown`)
- UI strings and comments are in **Italian**
- Emoji used in user-facing output for status indicators

### Patterns
- Error handling with try-except in data loading, user-friendly Italian error messages
- Null checks on `self.trades` before processing
- Plotly `graph_objects` for precise chart control; `make_subplots` for multi-panel layouts
- HTML export via Plotly's `.to_html()` method
- Streamlit layout: `st.columns()` for grid, `st.tabs()` for sections, `st.metric()` for KPIs

### What Does NOT Exist
- No CI/CD pipelines
- No linting/formatting configuration (no black, flake8, pylint, mypy)
- No pre-commit hooks
- No `pyproject.toml`
- No `.editorconfig`
- No Streamlit caching (`@st.cache_data` not used)
- No formal unit tests

## Key Considerations for AI Assistants

1. **Language**: All user-facing strings, comments, docstrings, and documentation are in Italian. Maintain this convention.
2. **Import paths**: `app.py` and `main.py` import `from trade_analyzer` (not `from src.trade_analyzer`). They expect to run from inside `src/`. The test script adds `src` to `sys.path` to import from root.
3. **CSV path handling**: `main.py` defaults to `../tradelog_sample.csv` (relative to `src/`). `test_analyzer.py` uses `tradelog_sample.csv` (relative to project root). `app.py` uses `../tradelog_sample.csv`.
4. **Generated HTML files**: The test script and CLI produce HTML files in the working directory. These are large (~4.7 MB each due to embedded Plotly JS) and should not be committed.
5. **Single-class design**: All analysis logic is in `TradeAnalyzer`. New analysis features should be added as methods to this class.
6. **Visualization library**: Use Plotly for all new visualizations (not matplotlib/seaborn, despite them being imported).
7. **No formal tests**: When making changes, verify by running `python test_analyzer.py` from the project root and checking output.
