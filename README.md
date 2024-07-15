# sma_interecation

**The purposes of this project are:**

**1. Show techniques and skills of handling large datasets of financial data.**

**2. Develop and test trading idea build on SMA intersection.**


_Steps of work with data:_
- Create SQLite3 DB which consists of tables (create_db.py):
  currencies: id, pair, base_asset, quote_asset, exchange
  pairs_price: 

Dowloading data
- Request all tradeable pairs from binance.com exhange with "USDT" quoteAsset and add them into currencies table in db. Deletes delisted pairs and all data connected to the pair (add_pairs.py).
- Request data for pairs from db and add price and volume data into pairs_pirce table. (fill_prices.py)

Prepearing the data:
- Read the data from db's currencies and pairs-price tables into a multiindex dataframe.
- Check for missing dates values in dataframe for each symbol.
- Replace the missing valeus with previoues one if the amount of missing data is less then 1% of tickers' lenght.
- Check of NaN's values in the parameter space.
- Group the pairs into bins of 1 year to identify the length of history to work with and plot the results.
- Filter the dataframe removing pairs with less then 1 year of history.
- Calculate correlation between numerical columns in the dataset and plot heatmap.
- Apply Shapiro-Wilk and Anderson-Darling tests to identify if the distribution of values in columns are normal.
- Plot a few random pair's and column distibuition to confirm the results of tests.
- Identify outliers, in the colume data columns, using DBSCAN and Box-Cox techniques and replace them with the average of the previous 30 days.
- Create simple moving averages in range from 10 to 370 with step of 10 for each pair in the dataset.
- Create columns with additional volume indicators.
- Normalize SMAs and volume indicaotrs' values with StandatrdScaler.
- identify bounds of minimum and maximum SMA's and volume indicators' values in a user-defined range of time for a specific symbol.
- Compare this bounds to other symbols in the dataframe and identify similarities.

Plan:
- Plot symbols and periods from history where symbols had been inside the bounds measured for user-defined symbol.
- Analyze data to improve the intersection logic.
- Calculate the probabilities of returns based on the "states of the prices" relatively to SMAs.

_Trading idea:_
Assuming that a cryptocurrencies market moves through accumulation and distrubution cycles in a four years cycles, the aim of this project is to quantify the current position of the price relatively to the positions in the previous cycles.
Example from BTCUSD, comparing june 2024 data it's history. It shows that with 90% of similarity this period is close to march and july 2017.
![image](https://github.com/user-attachments/assets/6c6cbfe9-fa0b-4756-af4e-aff13e1482fb)


