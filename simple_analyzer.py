#!/usr/bin/env python3
"""
Versione semplificata del Trade Analyzer che funziona solo con librerie standard
"""
import csv
import json
from datetime import datetime
from collections import defaultdict
import statistics

class SimpleTradeAnalyzer:
    """Analyzer semplificato che usa solo librerie standard"""
    
    def __init__(self, csv_file):
        self.trades = []
        self.load_trades(csv_file)
        self.calculate_metrics()
    
    def load_trades(self, csv_file):
        """Carica trade da CSV"""
        try:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Converte stringhe in numeri
                    trade = {
                        'date': row['date'],
                        'symbol': row['symbol'],
                        'side': row['side'],
                        'entry_price': float(row['entry_price']),
                        'exit_price': float(row['exit_price']),
                        'quantity': int(row['quantity']),
                        'commission': float(row['commission']),
                        'risk_amount': float(row['risk_amount']),
                        'setup': row.get('setup', ''),
                        'notes': row.get('notes', '')
                    }
                    self.trades.append(trade)
            print(f"✅ Caricati {len(self.trades)} trade da {csv_file}")
        except Exception as e:
            print(f"❌ Errore nel caricamento: {e}")
    
    def calculate_metrics(self):
        """Calcola metriche per ogni trade"""
        for trade in self.trades:
            # Calcola P&L lordo
            if trade['side'].lower() == 'long':
                gross_pnl = (trade['exit_price'] - trade['entry_price']) * trade['quantity']
            else:  # short
                gross_pnl = (trade['entry_price'] - trade['exit_price']) * trade['quantity']
            
            # P&L netto
            trade['gross_pnl'] = gross_pnl
            trade['net_pnl'] = gross_pnl - trade['commission']
            trade['is_winner'] = trade['net_pnl'] > 0
            
            # R-multiple
            if trade['risk_amount'] > 0:
                trade['r_multiple'] = gross_pnl / trade['risk_amount']
            else:
                trade['r_multiple'] = 0
        
        # Calcola equity curve
        cumulative_pnl = 0
        peak = 0
        for trade in sorted(self.trades, key=lambda x: x['date']):
            cumulative_pnl += trade['net_pnl']
            trade['cumulative_pnl'] = cumulative_pnl
            peak = max(peak, cumulative_pnl)
            trade['drawdown'] = cumulative_pnl - peak
    
    def get_basic_stats(self):
        """Calcola statistiche di base"""
        if not self.trades:
            return {}
        
        total_trades = len(self.trades)
        winners = [t for t in self.trades if t['is_winner']]
        losers = [t for t in self.trades if not t['is_winner']]
        
        winning_trades = len(winners)
        losing_trades = len(losers)
        win_rate = (winning_trades / total_trades) * 100
        
        avg_win = statistics.mean([t['net_pnl'] for t in winners]) if winners else 0
        avg_loss = statistics.mean([t['net_pnl'] for t in losers]) if losers else 0
        
        payoff_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        
        total_pnl = sum(t['net_pnl'] for t in self.trades)
        total_commission = sum(t['commission'] for t in self.trades)
        
        # Expectancy
        expectancy = (win_rate/100 * avg_win) + ((100-win_rate)/100 * avg_loss)
        
        # R-multiple medio
        avg_r = statistics.mean([t['r_multiple'] for t in self.trades])
        
        # Drawdown massimo
        max_drawdown = min([t['drawdown'] for t in self.trades])
        max_dd_pct = (max_drawdown / max([t['cumulative_pnl'] for t in self.trades if t['cumulative_pnl'] > 0] or [1])) * 100
        
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
            'avg_r_multiple': round(avg_r, 2),
            'max_drawdown': round(max_drawdown, 2),
            'max_drawdown_pct': round(max_dd_pct, 2)
        }
    
    def get_setup_stats(self):
        """Statistiche per setup"""
        setup_data = defaultdict(list)
        
        for trade in self.trades:
            setup = trade['setup'] or 'no_setup'
            setup_data[setup].append(trade)
        
        results = {}
        for setup, trades in setup_data.items():
            winners = [t for t in trades if t['is_winner']]
            total_pnl = sum(t['net_pnl'] for t in trades)
            avg_pnl = total_pnl / len(trades)
            win_rate = (len(winners) / len(trades)) * 100
            avg_r = statistics.mean([t['r_multiple'] for t in trades])
            
            results[setup] = {
                'trades': len(trades),
                'winners': len(winners),
                'total_pnl': round(total_pnl, 2),
                'avg_pnl': round(avg_pnl, 2),
                'win_rate': round(win_rate, 2),
                'avg_r': round(avg_r, 2)
            }
        
        return results
    
    def print_summary(self):
        """Stampa riassunto completo"""
        stats = self.get_basic_stats()
        
        print("=" * 60)
        print("📈 TRADE LOG ANALYZER - ANALISI PERFORMANCE")
        print("=" * 60)
        print(f"📊 Totale Trade: {stats['total_trades']}")
        print(f"🏆 Trade Vincenti: {stats['winning_trades']}")
        print(f"📉 Trade Perdenti: {stats['losing_trades']}")
        print(f"🎯 Win Rate: {stats['win_rate']}%")
        print(f"⚖️  Payoff Ratio: {stats['payoff_ratio']}")
        print(f"💡 Expectancy: ${stats['expectancy']}")
        print(f"📈 R-Multiple Medio: {stats['avg_r_multiple']}")
        print("-" * 40)
        print(f"💰 P&L Totale: ${stats['total_pnl']}")
        print(f"💸 Commissioni Totali: ${stats['total_commission']}")
        print(f"🟢 Guadagno Medio: ${stats['avg_win']}")
        print(f"🔴 Perdita Media: ${stats['avg_loss']}")
        print("-" * 40)
        print(f"📊 Max Drawdown: ${stats['max_drawdown']} ({stats['max_drawdown_pct']}%)")
        print("=" * 60)
        
        # Setup analysis
        setup_stats = self.get_setup_stats()
        if setup_stats:
            print("\n🎯 ANALISI PER SETUP:")
            print("-" * 60)
            for setup, data in setup_stats.items():
                print(f"\n📋 Setup: {setup}")
                print(f"   Trade: {data['trades']}")
                print(f"   Vincenti: {data['winners']}")
                print(f"   P&L Totale: ${data['total_pnl']}")
                print(f"   P&L Medio: ${data['avg_pnl']}")
                print(f"   Win Rate: {data['win_rate']}%")
                print(f"   R-Multiple: {data['avg_r']}")
        
        # Trade list
        print(f"\n📋 ELENCO TRADE:")
        print("-" * 80)
        print(f"{'Data':<12} {'Symbol':<8} {'Side':<6} {'P&L':<10} {'R-Mult':<8} {'Setup':<12}")
        print("-" * 80)
        
        for trade in sorted(self.trades, key=lambda x: x['date']):
            pnl_str = f"${trade['net_pnl']:>7.2f}"
            r_str = f"{trade['r_multiple']:>6.2f}R"
            print(f"{trade['date']:<12} {trade['symbol']:<8} {trade['side']:<6} "
                  f"{pnl_str:<10} {r_str:<8} {trade['setup']:<12}")
        
        print("=" * 60)
        
        # Equity curve data
        print("\n📈 EQUITY CURVE:")
        print("-" * 40)
        for trade in sorted(self.trades, key=lambda x: x['date']):
            print(f"{trade['date']}: ${trade['cumulative_pnl']:>8.2f}")
    
    def export_to_json(self, filename):
        """Esporta risultati in JSON"""
        data = {
            'summary': self.get_basic_stats(),
            'setup_analysis': self.get_setup_stats(),
            'trades': self.trades
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"📁 Dati esportati in {filename}")

def main():
    """Funzione principale"""
    print("🚀 Avvio Trade Log Analyzer...")
    
    try:
        # Carica e analizza i dati sample
        analyzer = SimpleTradeAnalyzer("/workspace/tradelog_sample.csv")
        analyzer.print_summary()
        
        # Esporta risultati
        analyzer.export_to_json("/workspace/trade_analysis.json")
        
        print("\n✅ Analisi completata!")
        print("\n💡 Per usare con i tuoi dati:")
        print("   python3 simple_analyzer.py")
        print("   Oppure modifica il path del CSV nel codice")
        
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    main()