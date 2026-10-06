# Backtesting Methodology

The project includes a simple backtesting module to compare recommendations against historical returns.

## Method

- Use historical price data only up to the prediction time.
- Do not use future information after the decision point.
- Generate buy/hold/avoid signals using the same rule engine as the live workflow.
- Evaluate forward returns over a fixed horizon.
- Measure number of signals, win rate, average return, cumulative return, and maximum drawdown.

## Limitations

This is a research-oriented approach and is not a production-grade trading strategy. It is best used to explain methodology and demonstration in a university environment.
