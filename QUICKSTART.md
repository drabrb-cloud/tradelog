# 🚀 Quick Start - Trade Log Analyzer

## ⚡ Avvio Rapido

### 1. Web App (Raccomandato)
```bash
./run_analyzer.sh web
```
Apri il browser su `http://localhost:8501`

### 2. Analisi da Linea di Comando
```bash
# Con dati di esempio
./run_analyzer.sh cli

# Con il tuo file CSV
./run_analyzer.sh cli tuo_file.csv
```

### 3. Test del Sistema
```bash
./run_analyzer.sh test
```

## 📊 Cosa Ottieni

### KPI Principali
- **Win Rate**: Percentuale trades vincenti
- **Payoff Ratio**: Rapporto vincita/perdita media
- **R-Multiple**: Rendimento vs rischio
- **Max Drawdown**: Massima perdita consecutiva
- **Sharpe Ratio**: Rendimento aggiustato per rischio

### Visualizzazioni
- 📈 **Equity Curve**: Evoluzione P&L nel tempo
- 📊 **Distribuzioni**: Returns e R-multiple
- 📋 **Tabelle**: Dettaglio trades e strategie

### Report
- 📄 **HTML Completo**: Report con grafici interattivi
- 📈 **Grafici Separati**: Equity curve e distribuzioni

## 📁 Formato CSV Richiesto

Il tuo file CSV deve avere queste colonne:

```csv
date,time,symbol,side,entry_price,exit_price,quantity,commission,notes,strategy,timeframe,stop_loss,take_profit,exit_reason
2024-01-15,09:30:00,AAPL,BUY,150.25,152.50,100,1.50,Note,swing,1D,148.00,155.00,TAKE_PROFIT
```

## 🎯 Prossimi Passi

1. **Prepara i tuoi dati** nel formato CSV
2. **Avvia la web app** per analisi interattiva
3. **Esplora le metriche** per capire le performance
4. **Identifica le strategie** più profittevoli
5. **Migliora il trading** basandoti sui dati

## 💡 Suggerimenti

- Usa la web app per esplorazioni interattive
- Esporta i report per condividerli
- Analizza le performance per strategia
- Monitora il drawdown per gestire il rischio

---

**Buon Trading! 📈💰**