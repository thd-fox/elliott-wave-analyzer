# Elliott Wave Analyzer

A heuristic Elliott Wave analysis tool that uses Yahoo Finance data to detect potential Elliott Wave patterns in stock price movements. This educational tool helps identify 5-3 wave patterns and provides Fibonacci analysis without requiring any API keys.

## Features

- **ZigZag Pattern Detection**: Identifies significant price swings based on percentage thresholds
- **Elliott Wave Labeling**: Attempts to label the last 8 pivot points as a 5-3 Elliott Wave pattern
- **Fibonacci Analysis**: Calculates common Fibonacci retracement levels
- **Visual Charts**: Optional plotting with wave labels
- **No API Keys Required**: Uses Yahoo Finance via yfinance library

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the script**

   ```bash
   # If you have the script file, navigate to the directory containing it
   cd /path/to/elliott-analyzer
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python3 -m venv elliott_venv
   ```

3. **Activate the virtual environment**

   ```bash
   # On macOS/Linux:
   source elliott_venv/bin/activate

   # On Windows:
   elliott_venv\Scripts\activate
   ```

4. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
python elliott_wave_analyzer.py --ticker AAPL
```

### Advanced Usage

```bash
python elliott_wave_analyzer.py --ticker AAPL --period 2y --interval 1d --zigzag 5 --plot
```

### Command Line Arguments

| Argument     | Type   | Default      | Description                                           |
| ------------ | ------ | ------------ | ----------------------------------------------------- |
| `--ticker`   | string | **Required** | Stock ticker symbol (e.g., AAPL, GOOGL, TSLA)         |
| `--period`   | string | `2y`         | Time period for data (`6mo`, `1y`, `2y`, `5y`, `max`) |
| `--interval` | string | `1d`         | Data interval (`1d`, `1h`, `30m`, `5m`)               |
| `--zigzag`   | float  | `5.0`        | ZigZag threshold percentage for swing detection       |
| `--plot`     | flag   | `False`      | Show interactive chart with wave labels               |

### Examples

1. **Analyze Apple stock with default settings:**

   ```bash
   python elliott_wave_analyzer.py --ticker AAPL
   ```

2. **Analyze Tesla with 6-month data and 3% ZigZag threshold:**

   ```bash
   python elliott_wave_analyzer.py --ticker TSLA --period 6mo --zigzag 3.0
   ```

3. **Analyze Google with hourly data and show chart:**

   ```bash
   python elliott_wave_analyzer.py --ticker GOOGL --interval 1h --plot
   ```

4. **Analyze Microsoft with maximum historical data:**
   ```bash
   python elliott_wave_analyzer.py --ticker MSFT --period max --plot
   ```

## Understanding the Output

### Sample Output

```
=== Report ===
Ticker: AAPL
Last price: 150.25
Period: 2y  Interval: 1d  ZigZag: 5.0 percent
Swings: 23
Elliott 5 3 pattern found: True  Trend: up
Labels:
  1: 2023-01-15  120.50
  2: 2023-02-10  135.75
  3: 2023-03-05  125.30
  4: 2023-04-12  140.20
  5: 2023-05-08  155.80
  A: 2023-06-15  145.60
  B: 2023-07-20  160.30
  C: 2023-08-10  150.25
```

### Output Explanation

- **Ticker**: The analyzed stock symbol
- **Last price**: Most recent closing price
- **Period/Interval**: Time range and data frequency used
- **ZigZag**: Percentage threshold used for swing detection
- **Swings**: Total number of significant price swings detected
- **Elliott 5 3 pattern found**: Whether a valid 5-3 wave pattern was identified
- **Trend**: Overall trend direction (up/down)
- **Labels**: Wave labels with dates and prices (1-5 for impulse waves, A-C for corrective waves)

## Elliott Wave Theory Basics

### 5-3 Wave Pattern

- **Waves 1-5**: Impulse waves in the direction of the main trend
- **Waves A-C**: Corrective waves against the main trend

### Wave Characteristics

- **Wave 1**: Initial move in trend direction
- **Wave 2**: First correction (typically 50-61.8% retracement)
- **Wave 3**: Usually the strongest wave (often 161.8% extension of Wave 1)
- **Wave 4**: Second correction (typically 23.6-38.2% retracement)
- **Wave 5**: Final wave in trend direction
- **Wave A**: First corrective wave
- **Wave B**: Counter-trend bounce
- **Wave C**: Final corrective wave

## Technical Details

### ZigZag Algorithm

The ZigZag function identifies significant price swings by:

1. Setting a minimum percentage threshold for reversals
2. Tracking price movements until the threshold is exceeded
3. Marking pivot points at local highs and lows
4. Filtering out minor fluctuations

### Elliott Wave Detection

The algorithm attempts to identify 5-3 patterns by:

1. Analyzing the last 8 pivot points
2. Checking for alternating up/down movements
3. Validating wave relationships and proportions
4. Labeling waves according to Elliott Wave theory

### Fibonacci Levels

Common retracement levels calculated:

- 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%

## Limitations and Disclaimers

⚠️ **Important Notes:**

1. **Educational Purpose**: This tool is for educational and research purposes only
2. **Heuristic Analysis**: Elliott Wave counting is subjective and interpretive
3. **Not Financial Advice**: Do not use this tool as the sole basis for investment decisions
4. **Market Volatility**: Results may vary significantly with different market conditions
5. **Data Dependency**: Analysis quality depends on Yahoo Finance data availability and accuracy

## Troubleshooting

### Common Issues

1. **No data for ticker**

   - Verify the ticker symbol is correct
   - Check if the stock is actively traded
   - Try a different time period

2. **Too few swings detected**

   - Reduce the ZigZag percentage threshold
   - Increase the time period
   - Try a different interval

3. **Import errors**

   - Ensure virtual environment is activated
   - Reinstall packages: `pip install -r requirements.txt --upgrade`

4. **Chart not displaying**
   - Install additional GUI backend: `pip install tkinter` (usually included with Python)
   - Try running without `--plot` flag first

### Getting Help

If you encounter issues:

1. Check that all dependencies are installed correctly
2. Verify your Python version is 3.7 or higher
3. Ensure your internet connection is stable (required for Yahoo Finance data)

## Contributing

This is an educational tool. Improvements and suggestions are welcome for:

- Enhanced wave detection algorithms
- Additional technical indicators
- Better visualization features
- More robust error handling

## License

This tool is provided as-is for educational purposes. Use at your own risk.
