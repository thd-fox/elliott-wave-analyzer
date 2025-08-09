#!/usr/bin/env python3
"""
elliott_wave_analyzer.py

A small heuristic Elliott wave analyzer.
Uses Yahoo Finance via yfinance so no API key is required.

Functions:
- load prices
- detect ZigZag swings
- try a simple 5 3 wave labeling
- measure Fibonacci retracements and extensions
- print a report and optionally plot

Install:
    pip install yfinance pandas numpy matplotlib

Example:
    python elliott_wave_analyzer.py --ticker AAPL --period 2y --interval 1d --zigzag 5

Note:
This is a heuristic tool for education. Elliott counting is interpretive.
"""

import argparse
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


@dataclass
class Swing:
    idx: pd.Timestamp
    price: float
    direction: int  # +1 up, -1 down


def fetch_data(ticker: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if df.empty:
        raise RuntimeError(f"No data for {ticker}")
    
    # Handle multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    
    return df


def zigzag(prices: pd.Series, pct: float = 5.0) -> List[Swing]:
    """
    Very simple ZigZag on close prices.
    pct is the minimum percent reversal per swing.
    """
    if prices.empty:
        return []

    pct = pct / 100.0
    idxs = prices.index
    last_pivot_price = float(prices.iloc[0])
    last_pivot_idx = idxs[0]

    direction = 0  # 0 unknown, +1 up, -1 down
    swings: List[Swing] = [Swing(last_pivot_idx, last_pivot_price, 0)]

    for i in range(1, len(prices)):
        price = float(prices.iloc[i])
        idx = idxs[i]

        if direction >= 0:
            high_since = float(prices.loc[last_pivot_idx:idx].max())
            down_change = (price - high_since) / high_since
            if direction == 0:
                change = (price - last_pivot_price) / last_pivot_price
                if abs(change) >= pct:
                    direction = 1 if change > 0 else -1
            elif direction == 1 and down_change <= -pct:
                pivot_idx = prices.loc[last_pivot_idx:idx].idxmax()
                pivot_price = float(prices.loc[pivot_idx])
                swings.append(Swing(pivot_idx, pivot_price, +1))
                last_pivot_idx, last_pivot_price = pivot_idx, pivot_price
                direction = -1

        if direction <= 0:
            low_since = float(prices.loc[last_pivot_idx:idx].min())
            up_change = (price - low_since) / low_since if low_since != 0 else 0.0
            if direction == 0:
                change = (price - last_pivot_price) / last_pivot_price
                if abs(change) >= pct:
                    direction = 1 if change > 0 else -1
            elif direction == -1 and up_change >= pct:
                pivot_idx = prices.loc[last_pivot_idx:idx].idxmin()
                pivot_price = float(prices.loc[pivot_idx])
                swings.append(Swing(pivot_idx, pivot_price, -1))
                last_pivot_idx, last_pivot_price = pivot_idx, pivot_price
                direction = +1

    swings.append(Swing(prices.index[-1], float(prices.iloc[-1]), direction))

    cleaned: List[Swing] = []
    for s in swings:
        if not cleaned or s.idx != cleaned[-1].idx:
            cleaned.append(s)
    return cleaned


def fib_levels(a: float, b: float) -> Dict[str, float]:
    """
    Common Fibonacci retracement levels between a and b.
    """
    diff = b - a
    return {
        "0.236": b - 0.236 * diff,
        "0.382": b - 0.382 * diff,
        "0.5": b - 0.5 * diff,
        "0.618": b - 0.618 * diff,
        "0.786": b - 0.786 * diff,
        "1.0": a,
    }


def try_label_5_3(swings: List[Swing]) -> Dict[str, object]:
    """
    Try to label the last swings as a 5 3 pattern.
    Heuristic: use the last eight pivot points and basic rules.
    """
    if len(swings) < 8:
        return {"ok": False, "reason": "too few swings", "labels": []}

    pts = swings[-9:-1]
    prices = [s.price for s in pts]

    trend_up = prices[5] > prices[0]
    trend_down = prices[5] < prices[0]
    if not (trend_up or trend_down):
        return {"ok": False, "reason": "unclear trend", "labels": []}

    ok_impulse = True
    if trend_up:
        ok_impulse &= prices[1] > prices[0] and prices[2] < prices[1] and prices[3] > prices[2] and prices[4] < prices[3] and prices[5] > prices[4]
    else:
        ok_impulse &= prices[1] < prices[0] and prices[2] > prices[1] and prices[3] < prices[2] and prices[4] > prices[3] and prices[5] < prices[4]

    if trend_up:
        ok_correction = prices[6] < prices[5] and prices[7] > prices[6]
    else:
        ok_correction = prices[6] > prices[5] and prices[7] < prices[6]

    labels = ["1","2","3","4","5","A","B","C"]
    return {
        "ok": bool(ok_impulse and ok_correction),
        "trend": "up" if trend_up else "down",
        "labels": [(pts[i].idx, prices[i], labels[i]) for i in range(8)],
        "points": pts
    }


def analyze(ticker: str, period: str = "2y", interval: str = "1d", zigzag_pct: float = 5.0, plot: bool = False) -> Dict[str, object]:
    df = fetch_data(ticker, period=period, interval=interval)
    close = df["Close"].dropna()
    swings = zigzag(close, pct=zigzag_pct)
    labeling = try_label_5_3(swings)

    report = {
        "ticker": ticker,
        "period": period,
        "interval": interval,
        "zigzag_pct": zigzag_pct,
        "last_price": float(close.iloc[-1]),
        "num_swings": len(swings),
        "elliott_5_3_match": labeling["ok"],
        "trend": labeling.get("trend"),
        "labels": labeling.get("labels", [])
    }

    if plot:
        plt.figure(figsize=(10, 6))
        plt.plot(close.index, close.values, linewidth=1.2)
        x = [s.idx for s in swings]
        y = [s.price for s in swings]
        plt.scatter(x, y, s=30)
        for idx, price, lab in labeling.get("labels", []):
            plt.annotate(lab, xy=(idx, price), xytext=(0, 8), textcoords="offset points", fontsize=9)
        plt.title(f"{ticker} closes with ZigZag {zigzag_pct} percent and Elliott labels")
        plt.xlabel("date")
        plt.ylabel("price")
        plt.tight_layout()
        plt.show()

    return report


def main():
    parser = argparse.ArgumentParser(description="Heuristic Elliott wave analysis with Yahoo Finance data")
    parser.add_argument("--ticker", type=str, required=True, help="Ticker like AAPL GOOGL PYPL UNH")
    parser.add_argument("--period", type=str, default="2y", help="Range like 6mo 1y 2y 5y max")
    parser.add_argument("--interval", type=str, default="1d", help="Interval like 1d 1h 30m")
    parser.add_argument("--zigzag", type=float, default=5.0, help="ZigZag threshold in percent")
    parser.add_argument("--plot", action="store_true", help="Show chart")
    args = parser.parse_args()

    rep = analyze(args.ticker, period=args.period, interval=args.interval, zigzag_pct=args.zigzag, plot=args.plot)
    print("=== Report ===")
    print(f"Ticker: {rep['ticker']}")
    print(f"Last price: {rep['last_price']:.2f}")
    print(f"Period: {rep['period']}  Interval: {rep['interval']}  ZigZag: {rep['zigzag_pct']} percent")
    print(f"Swings: {rep['num_swings']}")
    print(f"Elliott 5 3 pattern found: {rep['elliott_5_3_match']}  Trend: {rep.get('trend')}")
    if rep["labels"]:
        print("Labels:")
        for idx, price, lab in rep["labels"]:
            print(f"  {lab}: {idx.date()}  {price:.2f}")


if __name__ == "__main__":
    main()
