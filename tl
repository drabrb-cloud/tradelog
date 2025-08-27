# Tradelog - Analizzatore di Performance Trading

Applicazione completa per registrare e analizzare le operazioni di trading con calcolo automatico di KPI, visualizzazioni avanzate e interfaccia web.

## 🚀 Avvio Rapido

```bash
# Installa dipendenze
pip install -r requirements.txt

# Avvia l'app web
streamlit run src/web_app.py

# Oppure usa l'analyzer da command line
python src/trade_analyzer.py
```

## 📁 Struttura

- `tradelog_sample.csv` – Template con dati di esempio
- `src/` – Codice sorgente
  - `trade_analyzer.py` – Motore di analisi principale
  - `visualizations.py` – Grafici e visualizzazioni
  - `web_app.py` – Interfaccia web Streamlit
- `data/` – Directory per i tuoi file CSV
- `requirements.txt` – Dipendenze Python

## 📊 Funzionalità

### Analisi Automatiche
- **KPI Principali**: Win Rate, Payoff Ratio, R-Multiple, Expectancy
- **Performance**: P&L totale, drawdown massimo, equity curve
- **Analisi Temporale**: Performance mensile e trend
- **Analisi Setup**: Performance per strategia di trading

### Visualizzazioni
- 📈 Equity Curve con drawdown
- 📊 Distribuzioni P&L e R-Multiple
- 📅 Performance mensile
- 🎯 Analisi per setup di trading
- 🎛️ Dashboard interattiva completa

### Interfaccia Web
- ✅ Upload CSV o inserimento manuale
- 📊 Dashboard real-time
- 📈 Grafici interattivi
- 💾 Export dati e report
- 📋 Gestione trade log

## 🔧 Utilizzo

### 1. Dati CSV
Il file CSV deve contenere le colonne:
- `date`: Data trade (YYYY-MM-DD)
- `symbol`: Simbolo strumento
- `side`: long/short
- `entry_price`: Prezzo entrata
- `exit_price`: Prezzo uscita
- `quantity`: Quantità
- `commission`: Commissioni
- `risk_amount`: Capitale a rischio ($)
- `setup`: Strategia usata (opzionale)
- `notes`: Note (opzionale)

### 2. Analisi da Command Line
```python
from src.trade_analyzer import TradeAnalyzer

# Carica e analizza
analyzer = TradeAnalyzer("path/to/your/trades.csv")
analyzer.print_summary()

# Statistiche mensili
print(analyzer.get_monthly_stats())

# Analisi setup
print(analyzer.get_setup_analysis())
```

### 3. Interfaccia Web
```bash
streamlit run src/web_app.py
```
Apri http://localhost:8501 nel browser

## 📈 Metriche Calcolate

- **Win Rate**: % trade vincenti
- **Payoff Ratio**: Rapporto guadagno medio / perdita media
- **R-Multiple**: Rapporto P&L / Rischio per trade
- **Expectancy**: Valore atteso per trade
- **Drawdown**: Perdita massima dal picco
- **Equity Curve**: Andamento P&L cumulativo

## 🎯 Roadmap Future

- [ ] Export report PDF
- [ ] Integrazione broker API
- [ ] Database SQLite/PostgreSQL
- [ ] Analisi risk management avanzate
- [ ] Backtesting integration
- [ ] Mobile app
