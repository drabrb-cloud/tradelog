#!/bin/bash

# Trade Log Analyzer Launcher
# Script per avviare facilmente l'analizzatore di trades

echo "📊 TRADE LOG ANALYZER"
echo "===================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🔧 Creazione ambiente virtuale..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installazione dipendenze..."
    pip install pandas numpy matplotlib seaborn plotly dash dash-bootstrap-components streamlit
else
    echo "✅ Ambiente virtuale trovato"
    source venv/bin/activate
fi

# Check command line arguments
if [ "$1" = "web" ]; then
    echo "🌐 Avvio web app..."
    cd src
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0
elif [ "$1" = "cli" ]; then
    if [ -n "$2" ]; then
        echo "📊 Analisi file: $2"
        cd src
        python main.py "../$2"
    else
        echo "📊 Analisi con dati di esempio"
        cd src
        python main.py
    fi
elif [ "$1" = "test" ]; then
    echo "🧪 Esecuzione test..."
    python test_analyzer.py
else
    echo "📋 USAGE:"
    echo "  ./run_analyzer.sh web     - Avvia web app"
    echo "  ./run_analyzer.sh cli     - Analisi CLI con dati di esempio"
    echo "  ./run_analyzer.sh cli file.csv - Analisi CLI con file specifico"
    echo "  ./run_analyzer.sh test    - Esegue test del sistema"
    echo ""
    echo "💡 Esempi:"
    echo "  ./run_analyzer.sh web"
    echo "  ./run_analyzer.sh cli mio_trades.csv"
    echo "  ./run_analyzer.sh test"
fi