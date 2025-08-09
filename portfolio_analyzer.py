#!/usr/bin/env python3
"""
portfolio_analyzer.py

Runs Elliott Wave analysis on a portfolio of stocks from a CSV file.
Uses the elliott_wave_analyzer module to analyze each stock.

Usage:
    python portfolio_analyzer.py --portfolio portfolio.csv --output results.csv
"""

import argparse
import csv
import pandas as pd
from datetime import datetime
import sys
import os

# Import the analyzer functions from the main script
from elliott_wave_analyzer import analyze


def load_portfolio(csv_file: str) -> list:
    """Load portfolio from CSV file."""
    portfolio = []
    try:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Handle ticker name corrections
                ticker = row['ticker']
                if ticker == 'PALO-ALTO-NETWORKS':
                    ticker = 'PANW'  # Correct ticker for Palo Alto Networks
                
                portfolio.append({
                    'ticker': ticker,
                    'period': row['period'],
                    'interval': row['interval'],
                    'zigzag': float(row['zigzag'])
                })
    except FileNotFoundError:
        print(f"Error: Portfolio file '{csv_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading portfolio file: {e}")
        sys.exit(1)
    
    return portfolio


def analyze_portfolio(portfolio: list, output_file: str = None) -> pd.DataFrame:
    """Analyze all stocks in the portfolio."""
    results = []
    total_stocks = len(portfolio)
    
    print(f"Analyzing {total_stocks} stocks from portfolio...")
    print("=" * 60)
    
    for i, stock in enumerate(portfolio, 1):
        ticker = stock['ticker']
        period = stock['period']
        interval = stock['interval']
        zigzag_pct = stock['zigzag']
        
        print(f"[{i}/{total_stocks}] Analyzing {ticker}...")
        
        try:
            # Run the analysis
            report = analyze(
                ticker=ticker,
                period=period,
                interval=interval,
                zigzag_pct=zigzag_pct,
                plot=False
            )
            
            # Add to results
            result = {
                'ticker': ticker,
                'last_price': report['last_price'],
                'period': period,
                'interval': interval,
                'zigzag_pct': zigzag_pct,
                'num_swings': report['num_swings'],
                'elliott_5_3_match': report['elliott_5_3_match'],
                'trend': report.get('trend', 'N/A'),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'Success'
            }
            
            # Add wave labels if available
            if report['labels']:
                for idx, (date, price, label) in enumerate(report['labels']):
                    result[f'wave_{label}_date'] = date.strftime('%Y-%m-%d')
                    result[f'wave_{label}_price'] = price
            
            results.append(result)
            
            # Print summary
            status = "✓ FOUND" if report['elliott_5_3_match'] else "✗ Not found"
            trend_info = f"({report.get('trend', 'N/A')} trend)" if report.get('trend') else ""
            print(f"    Elliott 5-3 pattern: {status} {trend_info}")
            print(f"    Last price: ${report['last_price']:.2f}, Swings: {report['num_swings']}")
            
        except Exception as e:
            print(f"    ✗ Error analyzing {ticker}: {str(e)}")
            results.append({
                'ticker': ticker,
                'last_price': 0,
                'period': period,
                'interval': interval,
                'zigzag_pct': zigzag_pct,
                'num_swings': 0,
                'elliott_5_3_match': False,
                'trend': 'Error',
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'status': f'Error: {str(e)}'
            })
        
        print()
    
    # Convert to DataFrame
    df_results = pd.DataFrame(results)
    
    # Save to CSV if output file specified
    if output_file:
        df_results.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")
    
    return df_results


def print_summary(df_results: pd.DataFrame):
    """Print analysis summary."""
    total_stocks = len(df_results)
    successful_analyses = len(df_results[df_results['status'] == 'Success'])
    elliott_matches = len(df_results[df_results['elliott_5_3_match'] == True])
    
    print("=" * 60)
    print("PORTFOLIO ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total stocks analyzed: {total_stocks}")
    print(f"Successful analyses: {successful_analyses}")
    print(f"Failed analyses: {total_stocks - successful_analyses}")
    print(f"Elliott 5-3 patterns found: {elliott_matches}")
    print(f"Success rate: {(elliott_matches/successful_analyses*100):.1f}%" if successful_analyses > 0 else "N/A")
    
    if elliott_matches > 0:
        print("\nStocks with Elliott 5-3 patterns:")
        elliott_stocks = df_results[df_results['elliott_5_3_match'] == True]
        for _, stock in elliott_stocks.iterrows():
            trend_info = f" ({stock['trend']} trend)" if stock['trend'] != 'N/A' else ""
            print(f"  • {stock['ticker']}: ${stock['last_price']:.2f}{trend_info}")
    
    if successful_analyses < total_stocks:
        print("\nFailed analyses:")
        failed_stocks = df_results[df_results['status'] != 'Success']
        for _, stock in failed_stocks.iterrows():
            print(f"  • {stock['ticker']}: {stock['status']}")


def main():
    parser = argparse.ArgumentParser(description="Analyze a portfolio of stocks for Elliott Wave patterns")
    parser.add_argument("--portfolio", type=str, default="portfolio.csv", 
                       help="CSV file containing portfolio (default: portfolio.csv)")
    parser.add_argument("--output", type=str, 
                       help="Output CSV file for results (optional)")
    parser.add_argument("--summary-only", action="store_true", 
                       help="Show only summary, not individual stock details")
    
    args = parser.parse_args()
    
    # Load portfolio
    portfolio = load_portfolio(args.portfolio)
    
    # Analyze portfolio
    results_df = analyze_portfolio(portfolio, args.output)
    
    # Print summary
    print_summary(results_df)
    
    return results_df


if __name__ == "__main__":
    main()
