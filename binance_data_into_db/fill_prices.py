import sqlite3
from binance import Client
from config import DB_FILE

# Create connection to DB
connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Call the DB to get IDs and pairs
query_all_pairs = "SELECT id, pair FROM currencies"
cursor.execute(query_all_pairs)
rows = cursor.fetchall()


# Get the timestamp of the last bar in the DB
def fetch_last_candle_in_DB(pair_id_to_insert, cursor):
    query_last_timestamp_in_DB = """SELECT open_time
                                    FROM pairs_price
                                    WHERE pair_id = ?
                                    ORDER BY open_time DESC LIMIT 1"""
    cursor.execute(query_last_timestamp_in_DB, (pair_id_to_insert,))
    last_timestamp_in_db = cursor.fetchone()
    return last_timestamp_in_db[0] if last_timestamp_in_db else None


# Create connection to Binance API
client = Client(requests_params={"timeout": 60})
pairs = [row["pair"] for row in rows]
pair_dict = {}
price_values = {}

# Create dicts with pair name as a key and pair id as value
# to use pair_id in DB
for row in rows:
    pair = row["pair"]
    pair_dict[pair] = row["id"]


insert_price_volume_data_into_pairs_price = """
                INSERT INTO pairs_price (pair_id, open_time, open, high, low, close, volume,
                quote_asset_volume, number_of_trades, taker_buy_base_asset_volume,
                taker_buy_quote_asset_volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """

earliest_date = "2017-08-01"


## Function which iterates over a dictionary with pair_id and price values,
## save each value as variable which are further made into tuple to insert it in DB

def tuple_price_column_to_insert(dict_values: list):
    open_time = value[0]
    open = value[1]
    high = value[2]
    low = value[3]
    close = value[4]
    volume = value[5]
    quote_asset_volume = value[7]
    number_of_trades = value[8]
    taker_buy_base_asset_volume = value[9]
    taker_buy_quote_asset_volume = value[10]

    tuple_to_insert = (pair_id, open_time, open, high, low, close,
                       volume, quote_asset_volume, number_of_trades,
                       taker_buy_base_asset_volume, taker_buy_quote_asset_volume)
    cursor.execute(insert_price_volume_data_into_pairs_price, tuple_to_insert)


# Get prices data, save it to dictionary
for i in range(0, len(pairs)):
    pair_name = pairs[i]
    ## Request data from binance and check the last available candle
    klines = client.get_historical_klines(pair_name, Client.KLINE_INTERVAL_1DAY, start_str=earliest_date)
    last_timestamp_binance = klines[-1][0]
    pair_id = pair_dict[pair_name]
    price_values[pair_id] = klines
    print(
        f"Processing pair: {pair_name}, Pair id: {pair_dict[pair_name]}, Counter of loaded pairs: {i + 1} of {len(pair_dict)}")

inv_pair_dict = {v: k for k, v in pair_dict.items()}
updated_pairs_list = []
added_pairs_list = []

for pair_id, list_of_prices in price_values.items():
    print(f"Check if {inv_pair_dict[pair_id]} is up to date.")
    last_timestamp_in_db = fetch_last_candle_in_DB(pair_id, cursor)
    if last_timestamp_binance == last_timestamp_in_db:
        pass
    else:
        for value in list_of_prices:
            if (last_timestamp_binance != last_timestamp_in_db) and (last_timestamp_in_db != None) and (
                    value[0] > last_timestamp_in_db):
                # Downloading and adding only the missing values to the DB
                tuple_price_column_to_insert(dict_values=value)
                if inv_pair_dict[pair_id] not in updated_pairs_list:
                    updated_pairs_list.append(inv_pair_dict[pair_id])

            elif (last_timestamp_binance != last_timestamp_in_db) and (last_timestamp_in_db == None):
                # Downloading and adding all the values to the DB
                tuple_price_column_to_insert(dict_values=value)
                if inv_pair_dict[pair_id] not in added_pairs_list:
                    added_pairs_list.append(inv_pair_dict[pair_id])

print(f"Updated pairs: {updated_pairs_list}")
print(f"New pairs: {added_pairs_list}")

connection.commit()