#!/usr/bin/env python3
"""
Script di avvio per il Trade Log Analyzer
"""
import sys
import subprocess
import os

def check_dependencies():
    """Controlla se le dipendenze sono installate"""
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import plotly
        import streamlit
        return True
    except ImportError as e:
        print(f"❌ Dipendenza mancante: {e}")
        return False

def install_dependencies():
    """Installa le dipendenze automaticamente"""
    print("📦 Installazione dipendenze...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dipendenze installate con successo!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Errore nell'installazione delle dipendenze")
        return False

def run_analyzer():
    """Esegue l'analyzer da command line"""
    print("🔍 Esecuzione analisi...")
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from trade_analyzer import TradeAnalyzer
        
        analyzer = TradeAnalyzer("/workspace/tradelog_sample.csv")
        analyzer.print_summary()
        
        print("\n📊 ANALISI MENSILE:")
        monthly = analyzer.get_monthly_stats()
        print(monthly)
        
        print("\n🎯 ANALISI PER SETUP:")
        setup = analyzer.get_setup_analysis()
        print(setup)
        
        return True
    except Exception as e:
        print(f"❌ Errore nell'analisi: {e}")
        return False

def run_web_app():
    """Avvia l'interfaccia web"""
    print("🌐 Avvio interfaccia web...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/web_app.py", 
            "--server.port=8501",
            "--server.address=0.0.0.0"
        ])
    except KeyboardInterrupt:
        print("\n👋 Interfaccia web chiusa")
    except Exception as e:
        print(f"❌ Errore nell'avvio web app: {e}")

def main():
    print("📈 Trade Log Analyzer")
    print("=" * 30)
    
    # Controlla dipendenze
    if not check_dependencies():
        if input("Installare le dipendenze? (y/n): ").lower() == 'y':
            if not install_dependencies():
                return
        else:
            print("❌ Dipendenze richieste per continuare")
            return
    
    # Menu opzioni
    print("\nScegli un'opzione:")
    print("1. 🌐 Avvia interfaccia web (consigliato)")
    print("2. 🔍 Esegui analisi da command line")
    print("3. 📊 Mostra dati sample")
    print("4. ❌ Esci")
    
    choice = input("\nOpzione (1-4): ").strip()
    
    if choice == '1':
        run_web_app()
    elif choice == '2':
        run_analyzer()
    elif choice == '3':
        import pandas as pd
        df = pd.read_csv("/workspace/tradelog_sample.csv")
        print("\n📋 DATI SAMPLE:")
        print(df)
        print(f"\n📊 Totale trade: {len(df)}")
    elif choice == '4':
        print("👋 Arrivederci!")
    else:
        print("❌ Opzione non valida")

if __name__ == "__main__":
    main()