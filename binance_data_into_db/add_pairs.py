import sqlite3
from binance import Client
from config import DB_FILE


# Create connection to DB
connection = sqlite3.connect(DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

# Prepare SELECT statement for getting pairs from DB
select_pairs_stmt = "SELECT pair FROM currencies"

# Execute SELECT statement and get list of pairs from DB
cursor.execute(select_pairs_stmt)
rows = cursor.fetchall()
# Query pairs in DB

query_all_pairs = "SELECT id, pair FROM currencies"
cursor.execute(query_all_pairs)
rows = cursor.fetchall()

pairs = [row["pair"] for row in rows]
pair_dict = {}
price_values = {}

# Create dicts with pair name as a key and pair id as value
# to use pair_id in DB
for row in rows:
    pair = row["pair"]
    pair_dict[pair] = row["id"]


# Create connection to Binance API
client = Client()

# Get data: timezone, ServerTime, rateLimits, exchangeFilters, symbols in dict type
info = client.get_exchange_info()

# Get data only from symbols dict
symbols = info["symbols"]

exchange = "BINANCE"
number_of_added_pairs = 0
number_of_delisted_pairs = 0

# Prepare INSERT statement for inserting new pairs
insert_pairs_stmt = "INSERT INTO currencies (pair, base_asset, quote_asset, exchange) VALUES (?, ?, ?, ?)"

# Prepare DELETE statement for deleting delisted pairs
delist_pairs_stmt = "DELETE FROM currencies WHERE pair = ?"

# Delete all the values from the "pairs_price" table
del_pairs_price_stmt = "DELETE FROM pairs_price WHERE pair_id = ?;"

for symbol in symbols:
    try:
        # check if the symbol is trading and not in DB, then insert
        if symbol["status"] == "TRADING" and symbol["quoteAsset"] == "USDT" and symbol["symbol"] not in pair_dict.keys():
            print(f"Added a new pair: {symbol['symbol']}")
            number_of_added_pairs += 1
            cursor.execute(insert_pairs_stmt, (symbol["symbol"], symbol["baseAsset"], symbol["quoteAsset"], exchange))
        # check if the symbol is delisted and in DB, then delete
        elif symbol["status"] == "BREAK" and symbol["symbol"] in pair_dict.keys():
            print(f"Exchange delisted a pair: {symbol['symbol']}")
            number_of_delisted_pairs += 1
            cursor.execute(delist_pairs_stmt, (symbol["symbol"],))
            cursor.execute(del_pairs_price_stmt, (pair_dict[symbol["symbol"]],))
    except Exception as e:
        print(symbol["symbol"])
        print(e)

if number_of_added_pairs == 0:
    print("No new pairs were listed on exchange")
if number_of_delisted_pairs == 0:
    print("No pairs were delisted from exchange")

connection.commit()