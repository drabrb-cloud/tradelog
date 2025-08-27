"""
Modulo per la visualizzazione dei dati di trading
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configura stile matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TradingVisualizer:
    """Classe per creare visualizzazioni dei dati di trading"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inizializza con DataFrame dei trade
        
        Args:
            df: DataFrame con i dati dei trade processati
        """
        self.df = df.copy()
        
    def plot_equity_curve(self, interactive: bool = True):
        """
        Crea grafico della equity curve
        
        Args:
            interactive: Se True usa Plotly, altrimenti matplotlib
        """
        if interactive:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=self.df['date'],
                y=self.df['cumulative_pnl'],
                mode='lines',
                name='Equity Curve',
                line=dict(color='blue', width=2)
            ))
            
            # Aggiungi drawdown
            fig.add_trace(go.Scatter(
                x=self.df['date'],
                y=self.df['drawdown'],
                fill='tonexty',
                mode='lines',
                name='Drawdown',
                line=dict(color='red', width=1),
                fillcolor='rgba(255,0,0,0.2)'
            ))
            
            fig.update_layout(
                title='Equity Curve e Drawdown',
                xaxis_title='Data',
                yaxis_title='P&L Cumulativo ($)',
                hovermode='x unified'
            )
            
            return fig
        else:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            
            # Equity curve
            ax1.plot(self.df['date'], self.df['cumulative_pnl'], 'b-', linewidth=2)
            ax1.set_title('Equity Curve')
            ax1.set_ylabel('P&L Cumulativo ($)')
            ax1.grid(True, alpha=0.3)
            
            # Drawdown
            ax2.fill_between(self.df['date'], self.df['drawdown'], 0, 
                           color='red', alpha=0.3, label='Drawdown')
            ax2.plot(self.df['date'], self.df['drawdown'], 'r-', linewidth=1)
            ax2.set_title('Drawdown')
            ax2.set_ylabel('Drawdown ($)')
            ax2.set_xlabel('Data')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            return fig
    
    def plot_pnl_distribution(self, interactive: bool = True):
        """Distribuzioni dei P&L"""
        if interactive:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Distribuzione P&L', 'P&L per Trade', 
                              'R-Multiple Distribution', 'Win/Loss Ratio'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"type": "pie"}]]
            )
            
            # Distribuzione P&L
            fig.add_trace(
                go.Histogram(x=self.df['net_pnl'], nbinsx=20, name='P&L Distribution'),
                row=1, col=1
            )
            
            # P&L per trade nel tempo
            colors = ['green' if x > 0 else 'red' for x in self.df['net_pnl']]
            fig.add_trace(
                go.Bar(x=self.df.index, y=self.df['net_pnl'], 
                      marker_color=colors, name='P&L per Trade'),
                row=1, col=2
            )
            
            # R-Multiple distribution
            fig.add_trace(
                go.Histogram(x=self.df['r_multiple'], nbinsx=20, name='R-Multiple'),
                row=2, col=1
            )
            
            # Win/Loss pie chart
            win_count = self.df['is_winner'].sum()
            loss_count = len(self.df) - win_count
            fig.add_trace(
                go.Pie(labels=['Winning Trades', 'Losing Trades'], 
                      values=[win_count, loss_count],
                      marker_colors=['green', 'red']),
                row=2, col=2
            )
            
            fig.update_layout(height=800, showlegend=False)
            return fig
            
        else:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # Distribuzione P&L
            self.df['net_pnl'].hist(bins=20, ax=ax1, alpha=0.7, color='skyblue')
            ax1.axvline(self.df['net_pnl'].mean(), color='red', linestyle='--', 
                       label=f'Media: ${self.df["net_pnl"].mean():.2f}')
            ax1.set_title('Distribuzione P&L')
            ax1.set_xlabel('P&L ($)')
            ax1.set_ylabel('Frequenza')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # P&L per trade
            colors = ['green' if x > 0 else 'red' for x in self.df['net_pnl']]
            ax2.bar(range(len(self.df)), self.df['net_pnl'], color=colors, alpha=0.7)
            ax2.set_title('P&L per Trade')
            ax2.set_xlabel('Trade #')
            ax2.set_ylabel('P&L ($)')
            ax2.grid(True, alpha=0.3)
            
            # R-Multiple distribution
            self.df['r_multiple'].hist(bins=20, ax=ax3, alpha=0.7, color='lightgreen')
            ax3.axvline(self.df['r_multiple'].mean(), color='red', linestyle='--',
                       label=f'Media: {self.df["r_multiple"].mean():.2f}R')
            ax3.set_title('Distribuzione R-Multiple')
            ax3.set_xlabel('R-Multiple')
            ax3.set_ylabel('Frequenza')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
            # Win/Loss pie chart
            win_count = self.df['is_winner'].sum()
            loss_count = len(self.df) - win_count
            ax4.pie([win_count, loss_count], labels=['Vincenti', 'Perdenti'], 
                   colors=['green', 'red'], autopct='%1.1f%%', startangle=90)
            ax4.set_title('Rapporto Win/Loss')
            
            plt.tight_layout()
            return fig
    
    def plot_setup_performance(self, interactive: bool = True):
        """Performance per setup di trading"""
        if 'setup' not in self.df.columns:
            print("Colonna 'setup' non trovata nei dati")
            return None
            
        setup_stats = self.df.groupby('setup').agg({
            'net_pnl': ['sum', 'mean', 'count'],
            'is_winner': 'sum'
        })
        
        setup_stats.columns = ['total_pnl', 'avg_pnl', 'count', 'winners']
        setup_stats['win_rate'] = (setup_stats['winners'] / setup_stats['count']) * 100
        
        if interactive:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('P&L Totale per Setup', 'Win Rate per Setup',
                              'Trade Count per Setup', 'P&L Medio per Setup')
            )
            
            # P&L totale
            fig.add_trace(
                go.Bar(x=setup_stats.index, y=setup_stats['total_pnl'], name='P&L Totale'),
                row=1, col=1
            )
            
            # Win rate
            fig.add_trace(
                go.Bar(x=setup_stats.index, y=setup_stats['win_rate'], name='Win Rate %'),
                row=1, col=2
            )
            
            # Count
            fig.add_trace(
                go.Bar(x=setup_stats.index, y=setup_stats['count'], name='# Trade'),
                row=2, col=1
            )
            
            # P&L medio
            fig.add_trace(
                go.Bar(x=setup_stats.index, y=setup_stats['avg_pnl'], name='P&L Medio'),
                row=2, col=2
            )
            
            fig.update_layout(height=800, showlegend=False)
            return fig
            
        else:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # P&L totale
            setup_stats['total_pnl'].plot(kind='bar', ax=ax1, color='steelblue')
            ax1.set_title('P&L Totale per Setup')
            ax1.set_ylabel('P&L ($)')
            ax1.tick_params(axis='x', rotation=45)
            
            # Win rate
            setup_stats['win_rate'].plot(kind='bar', ax=ax2, color='lightgreen')
            ax2.set_title('Win Rate per Setup')
            ax2.set_ylabel('Win Rate (%)')
            ax2.tick_params(axis='x', rotation=45)
            
            # Count
            setup_stats['count'].plot(kind='bar', ax=ax3, color='orange')
            ax3.set_title('Numero Trade per Setup')
            ax3.set_ylabel('# Trade')
            ax3.tick_params(axis='x', rotation=45)
            
            # P&L medio
            setup_stats['avg_pnl'].plot(kind='bar', ax=ax4, color='purple')
            ax4.set_title('P&L Medio per Setup')
            ax4.set_ylabel('P&L Medio ($)')
            ax4.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            return fig
    
    def plot_monthly_performance(self, interactive: bool = True):
        """Performance mensile"""
        monthly = self.df.copy()
        monthly['year_month'] = monthly['date'].dt.to_period('M')
        
        monthly_stats = monthly.groupby('year_month').agg({
            'net_pnl': 'sum',
            'is_winner': ['sum', 'count']
        })
        
        monthly_stats.columns = ['monthly_pnl', 'winners', 'total_trades']
        monthly_stats['win_rate'] = (monthly_stats['winners'] / monthly_stats['total_trades']) * 100
        
        if interactive:
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('P&L Mensile', 'Win Rate Mensile'),
                shared_xaxes=True
            )
            
            # P&L mensile
            colors = ['green' if x > 0 else 'red' for x in monthly_stats['monthly_pnl']]
            fig.add_trace(
                go.Bar(x=monthly_stats.index.astype(str), y=monthly_stats['monthly_pnl'],
                      marker_color=colors, name='P&L Mensile'),
                row=1, col=1
            )
            
            # Win rate mensile
            fig.add_trace(
                go.Scatter(x=monthly_stats.index.astype(str), y=monthly_stats['win_rate'],
                          mode='lines+markers', name='Win Rate %'),
                row=2, col=1
            )
            
            fig.update_layout(height=600, showlegend=False)
            return fig
            
        else:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
            
            # P&L mensile
            colors = ['green' if x > 0 else 'red' for x in monthly_stats['monthly_pnl']]
            monthly_stats['monthly_pnl'].plot(kind='bar', ax=ax1, color=colors)
            ax1.set_title('P&L Mensile')
            ax1.set_ylabel('P&L ($)')
            ax1.grid(True, alpha=0.3)
            
            # Win rate mensile
            monthly_stats['win_rate'].plot(kind='line', ax=ax2, marker='o', color='blue')
            ax2.set_title('Win Rate Mensile')
            ax2.set_ylabel('Win Rate (%)')
            ax2.set_xlabel('Mese')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            return fig
    
    def create_dashboard(self):
        """Crea una dashboard completa interattiva"""
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        
        # Calcola metriche principali
        total_pnl = self.df['net_pnl'].sum()
        win_rate = (self.df['is_winner'].sum() / len(self.df)) * 100
        avg_r = self.df['r_multiple'].mean()
        max_dd = self.df['drawdown'].min()
        
        # Crea dashboard con subplot
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Equity Curve', 'Distribuzione P&L',
                'P&L per Trade', 'Setup Performance',
                'Performance Mensile', 'Metriche Chiave'
            ),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "table"}]]
        )
        
        # Equity curve
        fig.add_trace(
            go.Scatter(x=self.df['date'], y=self.df['cumulative_pnl'],
                      mode='lines', name='Equity', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Distribuzione P&L
        fig.add_trace(
            go.Histogram(x=self.df['net_pnl'], name='P&L Dist', 
                        marker_color='lightblue'),
            row=1, col=2
        )
        
        # P&L per trade
        colors = ['green' if x > 0 else 'red' for x in self.df['net_pnl']]
        fig.add_trace(
            go.Bar(x=self.df.index, y=self.df['net_pnl'],
                  marker_color=colors, name='P&L Trade'),
            row=2, col=1
        )
        
        # Setup performance (se disponibile)
        if 'setup' in self.df.columns:
            setup_pnl = self.df.groupby('setup')['net_pnl'].sum()
            fig.add_trace(
                go.Bar(x=setup_pnl.index, y=setup_pnl.values, name='Setup P&L'),
                row=2, col=2
            )
        
        # Performance mensile
        monthly = self.df.groupby(self.df['date'].dt.to_period('M'))['net_pnl'].sum()
        fig.add_trace(
            go.Bar(x=monthly.index.astype(str), y=monthly.values, name='Monthly P&L'),
            row=3, col=1
        )
        
        # Tabella metriche
        fig.add_trace(
            go.Table(
                header=dict(values=['Metrica', 'Valore']),
                cells=dict(values=[
                    ['P&L Totale', 'Win Rate', 'R-Multiple Medio', 'Max Drawdown', 'Totale Trade'],
                    [f'${total_pnl:.2f}', f'{win_rate:.1f}%', f'{avg_r:.2f}R', 
                     f'${max_dd:.2f}', f'{len(self.df)}']
                ])
            ),
            row=3, col=2
        )
        
        fig.update_layout(
            height=1200,
            title_text="Trading Performance Dashboard",
            showlegend=False
        )
        
        return fig

def save_plots(visualizer: TradingVisualizer, output_dir: str = "/workspace/charts/"):
    """Salva tutti i grafici in formato PNG e HTML"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Matplotlib plots
    equity_fig = visualizer.plot_equity_curve(interactive=False)
    equity_fig.savefig(f"{output_dir}/equity_curve.png", dpi=300, bbox_inches='tight')
    
    pnl_fig = visualizer.plot_pnl_distribution(interactive=False)
    pnl_fig.savefig(f"{output_dir}/pnl_distribution.png", dpi=300, bbox_inches='tight')
    
    if 'setup' in visualizer.df.columns:
        setup_fig = visualizer.plot_setup_performance(interactive=False)
        setup_fig.savefig(f"{output_dir}/setup_performance.png", dpi=300, bbox_inches='tight')
    
    monthly_fig = visualizer.plot_monthly_performance(interactive=False)
    monthly_fig.savefig(f"{output_dir}/monthly_performance.png", dpi=300, bbox_inches='tight')
    
    # Plotly interactive plots
    dashboard = visualizer.create_dashboard()
    dashboard.write_html(f"{output_dir}/dashboard.html")
    
    print(f"Grafici salvati in {output_dir}")

if __name__ == "__main__":
    # Test con dati sample
    from trade_analyzer import TradeAnalyzer
    
    analyzer = TradeAnalyzer("/workspace/tradelog_sample.csv")
    visualizer = TradingVisualizer(analyzer.df)
    
    # Crea alcuni grafici di test
    equity_fig = visualizer.plot_equity_curve(interactive=False)
    plt.show()
    
    pnl_fig = visualizer.plot_pnl_distribution(interactive=False)
    plt.show()