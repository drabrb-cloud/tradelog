import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class TradeAnalyzer:
    def __init__(self, csv_file=None):
        """Initialize the trade analyzer with optional CSV file"""
        self.trades = None
        self.analysis_results = {}
        
        if csv_file:
            self.load_trades(csv_file)
    
    def load_trades(self, csv_file):
        """Load trades from CSV file"""
        try:
            self.trades = pd.read_csv(csv_file)
            self.trades['date'] = pd.to_datetime(self.trades['date'])
            self.trades['datetime'] = pd.to_datetime(self.trades['date'].astype(str) + ' ' + self.trades['time'])
            self._calculate_trade_metrics()
            print(f"✅ Caricati {len(self.trades)} trades da {csv_file}")
        except Exception as e:
            print(f"❌ Errore nel caricamento del file: {e}")
    
    def _calculate_trade_metrics(self):
        """Calculate basic trade metrics"""
        if self.trades is None:
            return
            
        # Calculate P&L
        self.trades['price_diff'] = self.trades['exit_price'] - self.trades['entry_price']
        self.trades['gross_pnl'] = self.trades['price_diff'] * self.trades['quantity']
        self.trades['net_pnl'] = self.trades['gross_pnl'] - self.trades['commission']
        
        # Calculate percentage returns
        self.trades['return_pct'] = (self.trades['price_diff'] / self.trades['entry_price']) * 100
        
        # Calculate R-multiple (assuming 1R = 1% risk)
        self.trades['risk_pct'] = abs(self.trades['entry_price'] - self.trades['stop_loss']) / self.trades['entry_price'] * 100
        self.trades['r_multiple'] = self.trades['return_pct'] / self.trades['risk_pct']
        
        # Win/Loss classification
        self.trades['is_win'] = self.trades['net_pnl'] > 0
        self.trades['is_loss'] = self.trades['net_pnl'] < 0
        
        # Trade duration (if time data available)
        if 'datetime' in self.trades.columns:
            self.trades = self.trades.sort_values('datetime')
    
    def calculate_kpis(self):
        """Calculate comprehensive KPIs"""
        if self.trades is None or len(self.trades) == 0:
            return {}
        
        total_trades = len(self.trades)
        winning_trades = len(self.trades[self.trades['is_win']])
        losing_trades = len(self.trades[self.trades['is_loss']])
        
        # Win rate
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        # Profit metrics
        total_pnl = self.trades['net_pnl'].sum()
        avg_win = self.trades[self.trades['is_win']]['net_pnl'].mean() if winning_trades > 0 else 0
        avg_loss = self.trades[self.trades['is_loss']]['net_pnl'].mean() if losing_trades > 0 else 0
        
        # Payoff ratio
        payoff_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
        
        # R-multiple metrics
        avg_r_multiple = self.trades['r_multiple'].mean()
        max_r_multiple = self.trades['r_multiple'].max()
        min_r_multiple = self.trades['r_multiple'].min()
        
        # Risk metrics
        max_drawdown = self._calculate_max_drawdown()
        sharpe_ratio = self._calculate_sharpe_ratio()
        
        # Strategy performance
        strategy_performance = self.trades.groupby('strategy').agg({
            'net_pnl': ['sum', 'mean', 'count'],
            'is_win': 'sum'
        }).round(2)
        
        self.analysis_results = {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'payoff_ratio': payoff_ratio,
            'avg_r_multiple': avg_r_multiple,
            'max_r_multiple': max_r_multiple,
            'min_r_multiple': min_r_multiple,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'strategy_performance': strategy_performance
        }
        
        return self.analysis_results
    
    def _calculate_max_drawdown(self):
        """Calculate maximum drawdown"""
        if 'datetime' not in self.trades.columns:
            return 0
            
        cumulative_pnl = self.trades.sort_values('datetime')['net_pnl'].cumsum()
        running_max = cumulative_pnl.expanding().max()
        drawdown = (cumulative_pnl - running_max) / running_max * 100
        return drawdown.min()
    
    def _calculate_sharpe_ratio(self):
        """Calculate Sharpe ratio (simplified)"""
        if len(self.trades) < 2:
            return 0
            
        returns = self.trades['net_pnl']
        avg_return = returns.mean()
        std_return = returns.std()
        
        if std_return == 0:
            return 0
            
        return avg_return / std_return
    
    def print_summary(self):
        """Print a comprehensive summary of trading performance"""
        if not self.analysis_results:
            self.calculate_kpis()
        
        print("\n" + "="*60)
        print("📊 ANALISI PERFORMANCE TRADING")
        print("="*60)
        
        results = self.analysis_results
        print(f"📈 Trades Totali: {results['total_trades']}")
        print(f"✅ Trades Vincenti: {results['winning_trades']}")
        print(f"❌ Trades Perdenti: {results['losing_trades']}")
        print(f"🎯 Win Rate: {results['win_rate']:.2f}%")
        print(f"💰 P&L Totale: €{results['total_pnl']:,.2f}")
        print(f"📊 P&L Medio Vincente: €{results['avg_win']:,.2f}")
        print(f"📉 P&L Medio Perdente: €{results['avg_loss']:,.2f}")
        print(f"⚖️ Payoff Ratio: {results['payoff_ratio']:.2f}")
        print(f"🎲 R-Multiple Medio: {results['avg_r_multiple']:.2f}")
        print(f"🚀 R-Multiple Max: {results['max_r_multiple']:.2f}")
        print(f"📉 R-Multiple Min: {results['min_r_multiple']:.2f}")
        print(f"💸 Max Drawdown: {results['max_drawdown']:.2f}%")
        print(f"📊 Sharpe Ratio: {results['sharpe_ratio']:.2f}")
        
        print("\n📋 PERFORMANCE PER STRATEGIA:")
        print(results['strategy_performance'])
    
    def plot_equity_curve(self, save_path=None):
        """Plot equity curve"""
        if self.trades is None or 'datetime' not in self.trades.columns:
            print("❌ Dati datetime non disponibili per il grafico")
            return
        
        fig = go.Figure()
        
        # Sort by datetime and calculate cumulative P&L
        sorted_trades = self.trades.sort_values('datetime')
        cumulative_pnl = sorted_trades['net_pnl'].cumsum()
        
        fig.add_trace(go.Scatter(
            x=sorted_trades['datetime'],
            y=cumulative_pnl,
            mode='lines+markers',
            name='Equity Curve',
            line=dict(color='#2E8B57', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title='📈 Equity Curve - Evoluzione P&L',
            xaxis_title='Data',
            yaxis_title='P&L Cumulativo (€)',
            template='plotly_white',
            height=500
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def plot_returns_distribution(self, save_path=None):
        """Plot returns distribution"""
        if self.trades is None:
            return
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distribuzione Returns', 'Distribuzione R-Multiple', 'Wins vs Losses', 'P&L per Trade'),
            specs=[[{"type": "histogram"}, {"type": "histogram"}],
                   [{"type": "bar"}, {"type": "scatter"}]]
        )
        
        # Returns distribution
        fig.add_trace(
            go.Histogram(x=self.trades['return_pct'], name='Returns %', nbinsx=20),
            row=1, col=1
        )
        
        # R-multiple distribution
        fig.add_trace(
            go.Histogram(x=self.trades['r_multiple'], name='R-Multiple', nbinsx=20),
            row=1, col=2
        )
        
        # Wins vs Losses
        win_loss_counts = [len(self.trades[self.trades['is_win']]), len(self.trades[self.trades['is_loss']])]
        fig.add_trace(
            go.Bar(x=['Wins', 'Losses'], y=win_loss_counts, name='Win/Loss Count'),
            row=2, col=1
        )
        
        # P&L scatter
        fig.add_trace(
            go.Scatter(x=list(range(len(self.trades))), y=self.trades['net_pnl'], 
                      mode='markers', name='P&L per Trade'),
            row=2, col=2
        )
        
        fig.update_layout(
            title='📊 Analisi Distribuzioni Trading',
            template='plotly_white',
            height=600
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def export_analysis(self, filename='trade_analysis_report.html'):
        """Export comprehensive analysis to HTML"""
        if not self.analysis_results:
            self.calculate_kpis()
        
        # Create equity curve
        equity_fig = self.plot_equity_curve()
        
        # Create distribution plots
        dist_fig = self.plot_returns_distribution()
        
        # Create HTML report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Trade Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 10px; }}
                .metric {{ background-color: #e8f4f8; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .chart {{ margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Report Analisi Trading</h1>
                <p>Generato il: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="metric">
                <h2>📈 Metriche Principali</h2>
                <p><strong>Total Trades:</strong> {self.analysis_results['total_trades']}</p>
                <p><strong>Win Rate:</strong> {self.analysis_results['win_rate']:.2f}%</p>
                <p><strong>Total P&L:</strong> €{self.analysis_results['total_pnl']:,.2f}</p>
                <p><strong>Payoff Ratio:</strong> {self.analysis_results['payoff_ratio']:.2f}</p>
                <p><strong>Max Drawdown:</strong> {self.analysis_results['max_drawdown']:.2f}%</p>
            </div>
            
            <div class="chart">
                {equity_fig.to_html(full_html=False)}
            </div>
            
            <div class="chart">
                {dist_fig.to_html(full_html=False)}
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Report esportato in: {filename}")
        return filename