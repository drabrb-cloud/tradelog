#!/usr/bin/env python3
"""
Test script per il Trade Log Analyzer
Dimostra le funzionalità principali del sistema
"""

import sys
import os

# Add src directory to path
sys.path.append('src')

from trade_analyzer import TradeAnalyzer

def test_analyzer():
    print("🧪 TESTING TRADE LOG ANALYZER")
    print("=" * 50)
    
    # Test with sample data
    sample_file = "tradelog_sample.csv"
    
    if not os.path.exists(sample_file):
        print(f"❌ File di test non trovato: {sample_file}")
        return
    
    # Initialize analyzer
    print("📊 Inizializzazione analyzer...")
    analyzer = TradeAnalyzer(sample_file)
    
    if analyzer.trades is None:
        print("❌ Errore nel caricamento dei dati di test")
        return
    
    print(f"✅ Caricati {len(analyzer.trades)} trades di test")
    
    # Calculate KPIs
    print("\n📈 Calcolo KPIs...")
    kpis = analyzer.calculate_kpis()
    
    # Print summary
    analyzer.print_summary()
    
    # Test visualizations
    print("\n📊 Test visualizzazioni...")
    
    # Equity curve
    equity_fig = analyzer.plot_equity_curve("test_equity_curve.html")
    print("✅ Equity curve generata: test_equity_curve.html")
    
    # Distribution plots
    dist_fig = analyzer.plot_returns_distribution("test_distributions.html")
    print("✅ Grafici distribuzioni generati: test_distributions.html")
    
    # Export report
    report_file = analyzer.export_analysis("test_report.html")
    print(f"✅ Report di test generato: {report_file}")
    
    print("\n🎉 Test completato con successo!")
    print("📁 File generati:")
    print("   - test_equity_curve.html")
    print("   - test_distributions.html")
    print("   - test_report.html")
    
    # Show some sample data
    print("\n📋 Anteprima dati:")
    print(analyzer.trades[['date', 'symbol', 'side', 'entry_price', 'exit_price', 'net_pnl']].head())

if __name__ == "__main__":
    test_analyzer()