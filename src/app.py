import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import sys
from trade_analyzer import TradeAnalyzer

# Page config
st.set_page_config(
    page_title="Trade Log Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📊 Trade Log Analyzer")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("📁 Carica i tuoi dati")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Scegli un file CSV con i tuoi trades",
        type=['csv'],
        help="Il file deve contenere le colonne: date, time, symbol, side, entry_price, exit_price, quantity, commission"
    )
    
    # Or use sample data
    use_sample = st.sidebar.checkbox("Usa dati di esempio", value=True)
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_trades.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        analyzer = TradeAnalyzer("temp_trades.csv")
        st.success(f"✅ Caricati {len(analyzer.trades)} trades dal file uploadato")
        
    elif use_sample:
        sample_file = "../tradelog_sample.csv"
        if os.path.exists(sample_file):
            analyzer = TradeAnalyzer(sample_file)
            st.info(f"📊 Analizzando {len(analyzer.trades)} trades di esempio")
        else:
            st.error("❌ File di esempio non trovato")
            return
    else:
        st.warning("⚠️ Carica un file CSV o usa i dati di esempio")
        return
    
    if analyzer.trades is None:
        st.error("❌ Errore nel caricamento dei dati")
        return
    
    # Calculate KPIs
    kpis = analyzer.calculate_kpis()
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Total Trades", kpis['total_trades'])
    
    with col2:
        st.metric("🎯 Win Rate", f"{kpis['win_rate']:.1f}%")
    
    with col3:
        st.metric("💰 Total P&L", f"€{kpis['total_pnl']:,.0f}")
    
    with col4:
        st.metric("⚖️ Payoff Ratio", f"{kpis['payoff_ratio']:.2f}")
    
    # More metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("✅ Winning Trades", kpis['winning_trades'])
    
    with col2:
        st.metric("❌ Losing Trades", kpis['losing_trades'])
    
    with col3:
        st.metric("💸 Max Drawdown", f"{kpis['max_drawdown']:.1f}%")
    
    with col4:
        st.metric("📊 Sharpe Ratio", f"{kpis['sharpe_ratio']:.2f}")
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Equity Curve", "📊 Distribuzioni", "📋 Dati Trades", "📈 Strategie"])
    
    with tab1:
        st.subheader("📈 Equity Curve")
        equity_fig = analyzer.plot_equity_curve()
        st.plotly_chart(equity_fig, use_container_width=True)
        
        # Additional equity metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🚀 R-Multiple Max", f"{kpis['max_r_multiple']:.2f}")
        with col2:
            st.metric("📉 R-Multiple Min", f"{kpis['min_r_multiple']:.2f}")
    
    with tab2:
        st.subheader("📊 Analisi Distribuzioni")
        dist_fig = analyzer.plot_returns_distribution()
        st.plotly_chart(dist_fig, use_container_width=True)
        
        # Additional distribution metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 R-Multiple Medio", f"{kpis['avg_r_multiple']:.2f}")
        with col2:
            st.metric("📈 Return Medio", f"{analyzer.trades['return_pct'].mean():.2f}%")
    
    with tab3:
        st.subheader("📋 Dettaglio Trades")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_strategy = st.selectbox(
                "Strategia",
                ["Tutte"] + list(analyzer.trades['strategy'].unique())
            )
        
        with col2:
            selected_side = st.selectbox(
                "Side",
                ["Tutte", "BUY", "SELL"]
            )
        
        with col3:
            selected_outcome = st.selectbox(
                "Risultato",
                ["Tutti", "Win", "Loss"]
            )
        
        # Apply filters
        filtered_trades = analyzer.trades.copy()
        
        if selected_strategy != "Tutte":
            filtered_trades = filtered_trades[filtered_trades['strategy'] == selected_strategy]
        
        if selected_side != "Tutte":
            filtered_trades = filtered_trades[filtered_trades['side'] == selected_side]
        
        if selected_outcome == "Win":
            filtered_trades = filtered_trades[filtered_trades['is_win']]
        elif selected_outcome == "Loss":
            filtered_trades = filtered_trades[filtered_trades['is_loss']]
        
        # Display filtered trades
        st.dataframe(
            filtered_trades[['date', 'symbol', 'side', 'entry_price', 'exit_price', 
                           'quantity', 'net_pnl', 'return_pct', 'r_multiple', 'strategy']].round(2),
            use_container_width=True
        )
    
    with tab4:
        st.subheader("📈 Performance per Strategia")
        
        # Strategy performance chart
        strategy_data = analyzer.trades.groupby('strategy').agg({
            'net_pnl': ['sum', 'mean', 'count'],
            'is_win': 'sum'
        }).round(2)
        
        strategy_data.columns = ['Total P&L', 'Avg P&L', 'Trade Count', 'Wins']
        strategy_data['Win Rate'] = (strategy_data['Wins'] / strategy_data['Trade Count'] * 100).round(1)
        
        # Create strategy performance chart
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total P&L per Strategia', 'Win Rate per Strategia', 
                          'Numero Trades per Strategia', 'P&L Medio per Strategia'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Total P&L
        fig.add_trace(
            go.Bar(x=strategy_data.index, y=strategy_data['Total P&L'], name='Total P&L'),
            row=1, col=1
        )
        
        # Win Rate
        fig.add_trace(
            go.Bar(x=strategy_data.index, y=strategy_data['Win Rate'], name='Win Rate %'),
            row=1, col=2
        )
        
        # Trade Count
        fig.add_trace(
            go.Bar(x=strategy_data.index, y=strategy_data['Trade Count'], name='Trade Count'),
            row=2, col=1
        )
        
        # Avg P&L
        fig.add_trace(
            go.Bar(x=strategy_data.index, y=strategy_data['Avg P&L'], name='Avg P&L'),
            row=2, col=2
        )
        
        fig.update_layout(
            title='Performance per Strategia',
            template='plotly_white',
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Strategy table
        st.dataframe(strategy_data, use_container_width=True)
    
    # Export section
    st.markdown("---")
    st.subheader("📤 Esporta Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Genera Report HTML"):
            report_file = analyzer.export_analysis("trade_report.html")
            st.success(f"✅ Report generato: {report_file}")
    
    with col2:
        if st.button("📈 Scarica Equity Curve"):
            equity_fig = analyzer.plot_equity_curve()
            st.plotly_chart(equity_fig, use_container_width=True)

if __name__ == "__main__":
    main()