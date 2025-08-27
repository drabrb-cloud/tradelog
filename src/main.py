#!/usr/bin/env python3
"""
Trade Log Analyzer - Main Script
Analizza i tuoi trades e genera report dettagliati
"""

import sys
import os
from trade_analyzer import TradeAnalyzer

def main():
    print("📊 TRADE LOG ANALYZER")
    print("=" * 50)
    
    # Check if CSV file is provided as argument
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        # Default to sample file
        csv_file = "../tradelog_sample.csv"
        print(f"📁 Usando file di esempio: {csv_file}")
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"❌ File non trovato: {csv_file}")
        print("💡 Usa: python main.py <tuo_file.csv>")
        return
    
    # Initialize analyzer
    analyzer = TradeAnalyzer(csv_file)
    
    if analyzer.trades is None:
        print("❌ Errore nel caricamento dei dati")
        return
    
    # Calculate and display KPIs
    analyzer.calculate_kpis()
    analyzer.print_summary()
    
    # Generate visualizations
    print("\n📈 Generazione grafici...")
    
    # Equity curve
    equity_fig = analyzer.plot_equity_curve("equity_curve.html")
    print("✅ Equity curve salvata in: equity_curve.html")
    
    # Distribution plots
    dist_fig = analyzer.plot_returns_distribution("distributions.html")
    print("✅ Grafici distribuzioni salvati in: distributions.html")
    
    # Export comprehensive report
    report_file = analyzer.export_analysis("trade_analysis_report.html")
    print(f"✅ Report completo esportato in: {report_file}")
    
    print("\n🎉 Analisi completata! Apri i file HTML nel browser per visualizzare i grafici.")

if __name__ == "__main__":
    main()