# sma_interecation
Assuming that a cryptocurrencies market moves through accumulation and distrubution cycles in a four years cycles, the aim of this project is to quantify the current position of the price relatively to the positions in the prcious cycles.

What this code does:
- Requests BTCUSD data from Bitstamp exchange and saves it to csv file
- Calculates moving averages from with length from 10 to 740, with the step of 10.
- Scales the values of SMAs with StandardScaler.
- Measures the state of the price relatively to the moving avareges by finding the high and low values' borders for user-defined period.
- Compares the "current state" with the historical values where the price was in the same bounds within some degree of certainity, which is alos user defined.
- Plots the chart with highlited periods which fall into the "current state" category.
- Calculates the probabilities of the returns within 1, 2 standard deviations above and below for the next 3, 7 and 15 days
- Plots heatmap chart

Improvements:
- Create SQLite3 db.
- Populate it with ohlc, volume and some other data for all tradable pairs from binance exchange.

Plan:
- Conduct the research of cyclical logic on altcoins within shorter timeperiods then 4 years.
- Calculate the probabilities of returns based on the "states of the prices" relatively to SMAs.
