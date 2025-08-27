"""
Web App per il Trade Log - Interfaccia web con Streamlit
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import plotly.graph_objects as go
from trade_analyzer import TradeAnalyzer
from visualizations import TradingVisualizer
import os

# Configurazione pagina
st.set_page_config(
    page_title="Trade Log Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stile CSS personalizzato
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .positive {
        color: #00ff00;
        font-weight: bold;
    }
    .negative {
        color: #ff0000;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2E3192 0%, #1BFFFF 100%);
    }
</style>
""", unsafe_allow_html=True)

def load_sample_data():
    """Carica dati sample per demo"""
    return pd.read_csv("/workspace/tradelog_sample.csv")

def format_currency(value):
    """Formatta valori monetari"""
    if value >= 0:
        return f'<span class="positive">+${value:,.2f}</span>'
    else:
        return f'<span class="negative">-${abs(value):,.2f}</span>'

def format_percentage(value):
    """Formatta percentuali"""
    if value >= 0:
        return f'<span class="positive">+{value:.1f}%</span>'
    else:
        return f'<span class="negative">{value:.1f}%</span>'

def main():
    st.title("📈 Trade Log Analyzer")
    st.markdown("---")
    
    # Sidebar per upload e configurazioni
    st.sidebar.header("🔧 Configurazioni")
    
    # Upload file o usa sample data
    data_source = st.sidebar.radio(
        "Sorgente Dati:",
        ["Usa Dati Sample", "Carica CSV", "Inserimento Manuale"]
    )
    
    df = None
    
    if data_source == "Usa Dati Sample":
        df = load_sample_data()
        st.sidebar.success("✅ Dati sample caricati")
        
    elif data_source == "Carica CSV":
        uploaded_file = st.sidebar.file_uploader(
            "Carica il tuo file CSV",
            type=['csv'],
            help="Il CSV deve contenere le colonne: date, symbol, side, entry_price, exit_price, quantity, commission, risk_amount"
        )
        
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success(f"✅ File caricato: {len(df)} trade")
    
    elif data_source == "Inserimento Manuale":
        st.sidebar.info("Vai alla sezione 'Nuovo Trade' per inserire dati manualmente")
        
        # Controlla se esistono dati salvati
        if os.path.exists("/workspace/data/manual_trades.csv"):
            df = pd.read_csv("/workspace/data/manual_trades.csv")
            st.sidebar.success(f"✅ Dati esistenti: {len(df)} trade")
    
    # Tabs principali
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "📈 Analisi", "📋 Trade Log", "➕ Nuovo Trade", "📋 Gestione Dati"
    ])
    
    # TAB 1: Dashboard
    with tab1:
        if df is not None:
            try:
                analyzer = TradeAnalyzer(df=df)
                stats = analyzer.get_basic_stats()
                
                st.header("📊 Performance Overview")
                
                # Metriche principali in colonne
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>P&L Totale</h3>
                        <h2>{format_currency(stats['total_pnl'])}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>Win Rate</h3>
                        <h2>{stats['win_rate']}%</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>R-Multiple</h3>
                        <h2>{stats['avg_r_multiple']}R</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>Payoff Ratio</h3>
                        <h2>{stats['payoff_ratio']:.2f}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Seconda riga di metriche
                col5, col6, col7, col8 = st.columns(4)
                
                with col5:
                    st.metric("Totale Trade", stats['total_trades'])
                
                with col6:
                    st.metric("Trade Vincenti", stats['winning_trades'])
                
                with col7:
                    st.metric("Expectancy", f"${stats['expectancy']:.2f}")
                
                with col8:
                    st.metric("Max Drawdown", f"{format_percentage(stats['max_drawdown_pct'])}", unsafe_allow_html=True)
                
                # Grafici principali
                st.markdown("---")
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.subheader("📈 Equity Curve")
                    visualizer = TradingVisualizer(analyzer.df)
                    equity_fig = visualizer.plot_equity_curve(interactive=True)
                    st.plotly_chart(equity_fig, use_container_width=True)
                
                with col_right:
                    st.subheader("📊 Distribuzione P&L")
                    pnl_fig = visualizer.plot_pnl_distribution(interactive=True)
                    st.plotly_chart(pnl_fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Errore nell'analisi dei dati: {str(e)}")
        else:
            st.info("👆 Seleziona una sorgente dati nella sidebar per iniziare")
    
    # TAB 2: Analisi Avanzata
    with tab2:
        if df is not None:
            try:
                analyzer = TradeAnalyzer(df=df)
                visualizer = TradingVisualizer(analyzer.df)
                
                st.header("📈 Analisi Avanzata")
                
                # Analisi per setup
                if 'setup' in df.columns:
                    st.subheader("🎯 Performance per Setup")
                    setup_stats = analyzer.get_setup_analysis()
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.dataframe(setup_stats)
                    
                    with col2:
                        setup_fig = visualizer.plot_setup_performance(interactive=True)
                        st.plotly_chart(setup_fig, use_container_width=True)
                
                # Analisi mensile
                st.subheader("📅 Performance Mensile")
                monthly_stats = analyzer.get_monthly_stats()
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.dataframe(monthly_stats)
                
                with col2:
                    monthly_fig = visualizer.plot_monthly_performance(interactive=True)
                    st.plotly_chart(monthly_fig, use_container_width=True)
                
                # Dashboard completa
                st.subheader("🎛️ Dashboard Completa")
                dashboard = visualizer.create_dashboard()
                st.plotly_chart(dashboard, use_container_width=True)
                
            except Exception as e:
                st.error(f"Errore nell'analisi avanzata: {str(e)}")
        else:
            st.info("👆 Carica i dati per vedere l'analisi avanzata")
    
    # TAB 3: Trade Log
    with tab3:
        if df is not None:
            st.header("📋 Trade Log")
            
            # Filtri
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'symbol' in df.columns:
                    symbols = st.multiselect("Simboli", df['symbol'].unique())
                    if symbols:
                        df = df[df['symbol'].isin(symbols)]
            
            with col2:
                if 'side' in df.columns:
                    sides = st.multiselect("Lato", df['side'].unique())
                    if sides:
                        df = df[df['side'].isin(sides)]
            
            with col3:
                if 'setup' in df.columns:
                    setups = st.multiselect("Setup", df['setup'].unique())
                    if setups:
                        df = df[df['setup'].isin(setups)]
            
            # Mostra tabella trade
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )
            
            # Statistiche filtrate
            if len(df) > 0:
                filtered_analyzer = TradeAnalyzer(df=df)
                filtered_stats = filtered_analyzer.get_basic_stats()
                
                st.subheader("📊 Statistiche Trade Filtrati")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("P&L Totale", f"${filtered_stats['total_pnl']:.2f}")
                
                with col2:
                    st.metric("Win Rate", f"{filtered_stats['win_rate']:.1f}%")
                
                with col3:
                    st.metric("R-Multiple Medio", f"{filtered_stats['avg_r_multiple']:.2f}R")
        else:
            st.info("👆 Carica i dati per vedere il trade log")
    
    # TAB 4: Nuovo Trade
    with tab4:
        st.header("➕ Aggiungi Nuovo Trade")
        
        with st.form("new_trade_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                trade_date = st.date_input("Data", value=date.today())
                symbol = st.text_input("Simbolo", placeholder="es. AAPL")
                side = st.selectbox("Lato", ["long", "short"])
                entry_price = st.number_input("Prezzo Entrata", min_value=0.0, step=0.01)
                exit_price = st.number_input("Prezzo Uscita", min_value=0.0, step=0.01)
            
            with col2:
                quantity = st.number_input("Quantità", min_value=0, step=1)
                commission = st.number_input("Commissioni", min_value=0.0, step=0.01, value=2.0)
                risk_amount = st.number_input("Rischio ($)", min_value=0.0, step=1.0)
                setup = st.text_input("Setup", placeholder="es. breakout, pullback")
                notes = st.text_area("Note", placeholder="Note aggiuntive...")
            
            submitted = st.form_submit_button("💾 Salva Trade")
            
            if submitted:
                if all([symbol, entry_price, exit_price, quantity]):
                    new_trade = {
                        'date': trade_date.strftime('%Y-%m-%d'),
                        'symbol': symbol.upper(),
                        'side': side,
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'quantity': quantity,
                        'commission': commission,
                        'risk_amount': risk_amount,
                        'setup': setup if setup else 'manual',
                        'notes': notes
                    }
                    
                    # Salva su file
                    manual_file = "/workspace/data/manual_trades.csv"
                    
                    if os.path.exists(manual_file):
                        existing_df = pd.read_csv(manual_file)
                        updated_df = pd.concat([existing_df, pd.DataFrame([new_trade])], ignore_index=True)
                    else:
                        updated_df = pd.DataFrame([new_trade])
                    
                    updated_df.to_csv(manual_file, index=False)
                    st.success("✅ Trade salvato con successo!")
                    st.rerun()
                else:
                    st.error("❌ Compila tutti i campi obbligatori")
    
    # TAB 5: Gestione Dati
    with tab5:
        st.header("📋 Gestione Dati")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Export Dati")
            if df is not None:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="💾 Scarica CSV",
                    data=csv,
                    file_name=f"tradelog_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
                if st.button("📊 Genera Report PDF"):
                    st.info("Feature in sviluppo - Report PDF")
        
        with col2:
            st.subheader("🗑️ Gestione File")
            if os.path.exists("/workspace/data/manual_trades.csv"):
                if st.button("🗑️ Cancella Dati Manuali", type="secondary"):
                    os.remove("/workspace/data/manual_trades.csv")
                    st.success("✅ Dati manuali cancellati")
                    st.rerun()
        
        # Template CSV
        st.subheader("📋 Template CSV")
        st.info("Struttura richiesta per il file CSV:")
        
        template_df = pd.DataFrame({
            'date': ['2024-01-15'],
            'symbol': ['AAPL'],
            'side': ['long'],
            'entry_price': [150.25],
            'exit_price': [155.80],
            'quantity': [100],
            'commission': [2.50],
            'risk_amount': [500.00],
            'setup': ['breakout'],
            'notes': ['Strong momentum']
        })
        
        st.dataframe(template_df)
        
        template_csv = template_df.to_csv(index=False)
        st.download_button(
            label="💾 Scarica Template",
            data=template_csv,
            file_name="tradelog_template.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()