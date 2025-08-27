"""
Trade Analyzer - Analizza le performance dei trade
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradeAnalyzer:
    """Classe principale per l'analisi dei trade"""
    
    def __init__(self, csv_file: str = None, df: pd.DataFrame = None):
        """
        Inizializza l'analyzer con dati da CSV o DataFrame
        
        Args:
            csv_file: Path al file CSV dei trade
            df: DataFrame pandas con i trade
        """
        if csv_file:
            self.df = self.load_trades_from_csv(csv_file)
        elif df is not None:
            self.df = df.copy()
        else:
            raise ValueError("Fornisci csv_file o df")
            
        self.prepare_data()
        
    def load_trades_from_csv(self, csv_file: str) -> pd.DataFrame:
        """Carica i trade da file CSV"""
        try:
            df = pd.read_csv(csv_file)
            logger.info(f"Caricati {len(df)} trade da {csv_file}")
            return df
        except Exception as e:
            logger.error(f"Errore nel caricamento del CSV: {e}")
            raise
            
    def prepare_data(self):
        """Prepara e pulisce i dati per l'analisi"""
        # Converti la data
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Calcola P&L per trade
        self.df['gross_pnl'] = self.calculate_gross_pnl()
        self.df['net_pnl'] = self.df['gross_pnl'] - self.df['commission']
        
        # Calcola R-multiple (rapporto rischio/rendimento)
        self.df['r_multiple'] = self.calculate_r_multiple()
        
        # Determina win/loss
        self.df['is_winner'] = self.df['net_pnl'] > 0
        
        # Calcola equity curve cumulativa
        self.df = self.df.sort_values('date')
        self.df['cumulative_pnl'] = self.df['net_pnl'].cumsum()
        
        # Calcola drawdown
        self.df['peak'] = self.df['cumulative_pnl'].cummax()
        self.df['drawdown'] = self.df['cumulative_pnl'] - self.df['peak']
        self.df['drawdown_pct'] = (self.df['drawdown'] / self.df['peak'].replace(0, 1)) * 100
        
    def calculate_gross_pnl(self) -> pd.Series:
        """Calcola il P&L lordo per ogni trade"""
        pnl = []
        for _, row in self.df.iterrows():
            if row['side'].lower() == 'long':
                gross = (row['exit_price'] - row['entry_price']) * row['quantity']
            else:  # short
                gross = (row['entry_price'] - row['exit_price']) * row['quantity']
            pnl.append(gross)
        return pd.Series(pnl)
    
    def calculate_r_multiple(self) -> pd.Series:
        """Calcola l'R-multiple per ogni trade"""
        r_multiples = []
        for _, row in self.df.iterrows():
            if row['risk_amount'] > 0:
                r_mult = row['gross_pnl'] / row['risk_amount']
            else:
                r_mult = 0
            r_multiples.append(r_mult)
        return pd.Series(r_multiples)
    
    def get_basic_stats(self) -> Dict:
        """Calcola statistiche di base"""
        total_trades = len(self.df)
        winning_trades = self.df['is_winner'].sum()
        losing_trades = total_trades - winning_trades
        
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        avg_win = self.df[self.df['is_winner']]['net_pnl'].mean() if winning_trades > 0 else 0
        avg_loss = self.df[~self.df['is_winner']]['net_pnl'].mean() if losing_trades > 0 else 0
        
        payoff_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        
        total_pnl = self.df['net_pnl'].sum()
        total_commission = self.df['commission'].sum()
        
        # Expectancy
        expectancy = (win_rate/100 * avg_win) + ((100-win_rate)/100 * avg_loss)
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'payoff_ratio': round(payoff_ratio, 2),
            'total_pnl': round(total_pnl, 2),
            'total_commission': round(total_commission, 2),
            'expectancy': round(expectancy, 2),
            'avg_r_multiple': round(self.df['r_multiple'].mean(), 2),
            'max_drawdown': round(self.df['drawdown'].min(), 2),
            'max_drawdown_pct': round(self.df['drawdown_pct'].min(), 2)
        }
    
    def get_monthly_stats(self) -> pd.DataFrame:
        """Analisi mensile delle performance"""
        monthly = self.df.copy()
        monthly['year_month'] = monthly['date'].dt.to_period('M')
        
        monthly_stats = monthly.groupby('year_month').agg({
            'net_pnl': ['sum', 'mean', 'count'],
            'is_winner': 'sum',
            'r_multiple': 'mean'
        }).round(2)
        
        # Flatten column names
        monthly_stats.columns = ['total_pnl', 'avg_pnl', 'trades', 'winners', 'avg_r']
        monthly_stats['win_rate'] = ((monthly_stats['winners'] / monthly_stats['trades']) * 100).round(2)
        
        return monthly_stats
    
    def get_setup_analysis(self) -> pd.DataFrame:
        """Analisi per setup di trading"""
        if 'setup' not in self.df.columns:
            return pd.DataFrame()
            
        setup_stats = self.df.groupby('setup').agg({
            'net_pnl': ['sum', 'mean', 'count'],
            'is_winner': 'sum',
            'r_multiple': 'mean'
        }).round(2)
        
        # Flatten column names
        setup_stats.columns = ['total_pnl', 'avg_pnl', 'trades', 'winners', 'avg_r']
        setup_stats['win_rate'] = ((setup_stats['winners'] / setup_stats['trades']) * 100).round(2)
        
        return setup_stats.sort_values('total_pnl', ascending=False)
    
    def print_summary(self):
        """Stampa un riassunto delle performance"""
        stats = self.get_basic_stats()
        
        print("=" * 50)
        print("ANALISI PERFORMANCE TRADING")
        print("=" * 50)
        print(f"Totale Trade: {stats['total_trades']}")
        print(f"Trade Vincenti: {stats['winning_trades']}")
        print(f"Trade Perdenti: {stats['losing_trades']}")
        print(f"Win Rate: {stats['win_rate']}%")
        print(f"Payoff Ratio: {stats['payoff_ratio']}")
        print(f"Expectancy: ${stats['expectancy']}")
        print(f"R-Multiple Medio: {stats['avg_r_multiple']}")
        print("-" * 30)
        print(f"P&L Totale: ${stats['total_pnl']}")
        print(f"Commissioni Totali: ${stats['total_commission']}")
        print(f"Guadagno Medio: ${stats['avg_win']}")
        print(f"Perdita Media: ${stats['avg_loss']}")
        print("-" * 30)
        print(f"Max Drawdown: ${stats['max_drawdown']} ({stats['max_drawdown_pct']}%)")
        print("=" * 50)

if __name__ == "__main__":
    # Test con dati sample
    try:
        analyzer = TradeAnalyzer("/workspace/tradelog_sample.csv")
        analyzer.print_summary()
        
        print("\nANALISI MENSILE:")
        print(analyzer.get_monthly_stats())
        
        print("\nANALISI PER SETUP:")
        print(analyzer.get_setup_analysis())
        
    except Exception as e:
        print(f"Errore: {e}")