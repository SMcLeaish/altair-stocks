# Altair-Stocks

Wrapper for Altair. Pulls data from Yahoo Finance and creates an Altair chart and a Polars DataFrame for the corresponding time period.

Example usage:
```py
from altair_stocks import Stock


appl_today = Stock.today('APPL') # Creates Altair Chart object
appl.show() # Displays candlestick chart
appl.df # The corresponding DataFrame

appl_six_months = Stock.months('APPL', num_months=6) # Gets 6 months of data, daily intervals
appl.show() # Displays a line chart

appl_ytd = Stocks.ytd('APPL') # Gets year to date data, daily intervals
appl.show() # Displays a line chart
```
