# 📊 Trade Log Analyzer

Un sistema completo per analizzare i tuoi trades e migliorare le performance di trading.

## 🎯 Caratteristiche

- **📈 KPI Completi**: Win rate, payoff ratio, R-multiple, drawdown, Sharpe ratio
- **📊 Visualizzazioni Interattive**: Equity curve, distribuzioni, analisi per strategia
- **📋 Import CSV**: Carica facilmente i tuoi dati di trading
- **🌐 Web App**: Interfaccia web interattiva con Streamlit
- **📤 Report HTML**: Esporta report completi con grafici

## 🚀 Installazione

1. **Clona il repository**:
```bash
git clone <repository-url>
cd trade-log-analyzer
```

2. **Installa le dipendenze**:
```bash
pip install -r requirements.txt
```

## 📁 Struttura del Progetto

```
trade-log-analyzer/
├── src/
│   ├── trade_analyzer.py    # Classe principale per l'analisi
│   ├── main.py             # Script CLI
│   └── app.py              # Web app Streamlit
├── tradelog_sample.csv     # Template CSV con dati di esempio
├── requirements.txt        # Dipendenze Python
└── README.md              # Questo file
```

## 📊 Formato CSV

Il tuo file CSV deve contenere queste colonne:

| Colonna | Descrizione | Esempio |
|---------|-------------|---------|
| `date` | Data del trade | 2024-01-15 |
| `time` | Orario del trade | 09:30:00 |
| `symbol` | Simbolo/strumento | AAPL |
| `side` | Lato del trade | BUY/SELL |
| `entry_price` | Prezzo di entrata | 150.25 |
| `exit_price` | Prezzo di uscita | 152.50 |
| `quantity` | Quantità | 100 |
| `commission` | Commissioni | 1.50 |
| `notes` | Note (opzionale) | Strong earnings |
| `strategy` | Strategia usata | swing |
| `timeframe` | Timeframe | 1D |
| `stop_loss` | Stop loss | 148.00 |
| `take_profit` | Take profit | 155.00 |
| `exit_reason` | Motivo uscita | TAKE_PROFIT |

## 🎮 Utilizzo

### 1. Web App Interattiva (Raccomandato)

```bash
cd src
streamlit run app.py
```

Apri il browser su `http://localhost:8501` e:
- Carica il tuo file CSV
- Oppure usa i dati di esempio
- Esplora le metriche e i grafici interattivi

### 2. Script da Linea di Comando

```bash
cd src
python main.py tuo_file.csv
```

### 3. Uso Programmato

```python
from trade_analyzer import TradeAnalyzer

# Carica i tuoi trades
analyzer = TradeAnalyzer("tuo_file.csv")

# Calcola KPIs
kpis = analyzer.calculate_kpis()

# Stampa riassunto
analyzer.print_summary()

# Genera grafici
equity_fig = analyzer.plot_equity_curve()
dist_fig = analyzer.plot_returns_distribution()

# Esporta report completo
analyzer.export_analysis("mio_report.html")
```

## 📈 Metriche Calcolate

### KPI Principali
- **Win Rate**: Percentuale di trades vincenti
- **Payoff Ratio**: Rapporto tra vincita media e perdita media
- **R-Multiple**: Ritorno rispetto al rischio (1R = 1% rischio)
- **Max Drawdown**: Massima perdita consecutiva
- **Sharpe Ratio**: Rendimento aggiustato per il rischio

### Analisi per Strategia
- Performance per ogni strategia utilizzata
- Win rate per strategia
- P&L medio per strategia

### Visualizzazioni
- **Equity Curve**: Evoluzione del P&L nel tempo
- **Distribuzione Returns**: Istogramma dei rendimenti
- **Distribuzione R-Multiple**: Analisi del rischio/rendimento
- **Wins vs Losses**: Confronto trades vincenti/perdenti

## 🔧 Personalizzazione

### Aggiungere Nuove Metriche

Modifica `trade_analyzer.py` per aggiungere nuove metriche:

```python
def calculate_custom_metric(self):
    # La tua logica qui
    return custom_value
```

### Modificare i Grafici

Usa Plotly per personalizzare i grafici:

```python
def plot_custom_chart(self):
    fig = go.Figure()
    # Aggiungi i tuoi trace
    return fig
```

## 📤 Esportazione

### Report HTML
Il sistema genera automaticamente report HTML completi con:
- Metriche principali
- Grafici interattivi
- Tabelle riassuntive

### Grafici Separati
- `equity_curve.html`: Equity curve interattiva
- `distributions.html`: Grafici delle distribuzioni
- `trade_analysis_report.html`: Report completo

## 🛠️ Troubleshooting

### Errore: "File non trovato"
- Verifica che il percorso del file CSV sia corretto
- Assicurati che il file sia nella directory giusta

### Errore: "Colonne mancanti"
- Controlla che il CSV abbia tutte le colonne richieste
- Usa `tradelog_sample.csv` come template

### Errore: "Dati datetime non disponibili"
- Verifica che le colonne `date` e `time` siano nel formato corretto
- Esempio: `2024-01-15` e `09:30:00`

## 🚀 Roadmap

- [ ] Database SQLite/PostgreSQL
- [ ] API REST per integrazione
- [ ] Analisi avanzata (correlazioni, backtesting)
- [ ] Notifiche e alerting
- [ ] Integrazione con broker (MetaTrader, TradingView)

## 📝 Licenza

Questo progetto è rilasciato sotto licenza MIT.

## 🤝 Contributi

Contributi sono benvenuti! Apri una issue o una pull request.

---

**Buon Trading! 📈💰**