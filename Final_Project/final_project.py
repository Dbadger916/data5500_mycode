import requests
import networkx as nx
import alpaca_trade_api as tradeapi
import os
import json
from datetime import datetime
import time


API_KEY = "CG-jonPyb73MamvJyG56xufdHCQ" 
ALPACA_KEY = "PKZNZZLCDWHCHXO25BHQDIHMLF"
ALPACA_SECRET_KEY = "DcYL1v3RaZE4Q5T8jQp88Las19idHzVBP3kLbrBnNV14"

base_url = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(ALPACA_KEY, ALPACA_SECRET_KEY, base_url, api_version='v2')


#coin name mapped to the ticker name
COIN_IDS = {"bitcoin": "btc", "ethereum":"eth", "litecoin":"ltc", "bitcoin-cash": "bch", "dogecoin": "doge", "chainlink": "link", "uniswap": "uni", "avalanche-2": "avax", "aave": "aave", "polkadot": "dot"}

IDS           = ",".join(COIN_IDS.keys())
VS_CURRENCIES = ",".join(COIN_IDS.values())

#get the coins from coin gecko
CROSS_URL = (
    f"https://api.coingecko.com/api/v3/simple/price"
    f"?ids={IDS}"
    f"&vs_currencies={VS_CURRENCIES}"
    f"&x_cg_demo_api_key={API_KEY}"
)

#also get usd prices cause we gotta fo back and forth for alpaca
USD_URL = (
    f"https://api.coingecko.com/api/v3/simple/price"
    f"?ids={IDS}"
    f"&vs_currencies=usd"
    f"&x_cg_demo_api_key={API_KEY}"
)

response = requests.get(CROSS_URL)
price_data = response.json()

response = requests.get(USD_URL)
usd_data = response.json()

#the usd prices from coin geckooooo
usd_prices = {}
for coin_id, prices in usd_data.items():
    usd_prices[COIN_IDS[coin_id]] = prices["usd"]

#make the edges and print the exchange rates

ticker_to_id = {v: k for k, v in COIN_IDS.items()}
edges = []

print(f"{'From':<6} {'To':<6} {'Rate':>16}")
print("-" * 30)
#making the data files 
timestamp = datetime.now().strftime("%Y.%m.%d:%H.%M")
filename = f"/home/ubuntu/data5500_mycode/Final_Project/data/currency_pair_{timestamp}.txt"
os.makedirs(os.path.dirname(filename), exist_ok=True)

with open(filename, "w") as f:
    f.write("currency_from,currency_to,exchange_rate\n")

    for coin_id, vs_prices in price_data.items():
        from_ticker = COIN_IDS[coin_id]
        for to_ticker in COIN_IDS.values():
            if from_ticker == to_ticker:
                continue
            #use default rate if coingecko gave it, otherwise compute from usd
            if to_ticker in vs_prices:
                rate = vs_prices[to_ticker]
            else:
                rate = usd_prices[from_ticker] / usd_prices[to_ticker]
            print(f"{from_ticker:<6} {to_ticker:<6} {rate:>16.8f}")
            f.write(f"{from_ticker},{to_ticker},{rate}\n")
            edges.append((from_ticker, to_ticker, rate))


g = nx.DiGraph()
g.add_weighted_edges_from(edges)

tickers = list(COIN_IDS.values())


def path_weight(graph, path):
    """Return the product of all edge weights along a given path."""
    weight = 1.0
    for i in range(len(path) - 1):
        weight *= graph[path[i]][path[i + 1]]['weight']
    return weight


# Track global best and worst factor
greatest_factor       = 0.0
greatest_forward_path = None
greatest_reverse_path = None

smallest_factor       = float('inf')
smallest_forward_path = None
smallest_reverse_path = None

# iterate over all of the pairs, with a max path length cause this instance keeps crashing from how many coins i got
for src in tickers:
    for dst in tickers:
        if src == dst:
            continue

        forward_paths = list(nx.all_simple_paths(g, src, dst, cutoff=4))
        reverse_paths = list(nx.all_simple_paths(g, dst, src, cutoff=4))

        if not forward_paths or not reverse_paths:
            continue

        for fwd_path in forward_paths:
            fwd_weight = path_weight(g, fwd_path)

            for rev_path in reverse_paths:
                rev_weight = path_weight(g, rev_path)
                factor = fwd_weight * rev_weight

                # Update greatest factor, the biggest one is the best
                if factor > greatest_factor:
                    greatest_factor       = factor
                    greatest_forward_path = fwd_path
                    greatest_reverse_path = rev_path

                # Update smallest factor
                if factor < smallest_factor:
                    smallest_factor       = factor
                    smallest_forward_path = fwd_path
                    smallest_reverse_path = rev_path

#report best and worst paths
print(f"Greatest Paths weight factor:  {greatest_factor}")
print(f"Paths:  {greatest_forward_path} {greatest_reverse_path}")
print("=" * 60)

#makes it so when i try and buy and sell quickly it waits so i dont sell coins that i dont actually have
def wait_for_fill(api, order, poll_interval=0.5, timeout=30):
    """Poll until order fills, return the filled order."""
    start = time.time()
    while True:
        updated = api.get_order(order.id)
        if updated.status == "filled":
            return updated
        if updated.status in ("canceled", "expired", "rejected"):
            raise RuntimeError(f"Order {order.id} status: {updated.status}")
        if time.time() - start > timeout:
            raise TimeoutError(f"Order {order.id} not filled in time")
        time.sleep(poll_interval)


def execute_trades(api, path, starting_usd):
    """
    Walk the cycle path trading through Alpaca.
    Alpaca crypto is all vs USD, so A->B means sell A for USD then buy B with USD.
    """
    trade_log = []
    usd = starting_usd

    #snapshot pre-existing positions so we only sell what THIS run bought cause i got random coins in my thing from previous runs
    pre_existing = {}
    for coin in set(path):
        try:
            pos = api.get_position(f"{coin.upper()}USD")
            pre_existing[coin] = float(pos.qty)
        except Exception:
            pre_existing[coin] = 0.0

    for i, coin in enumerate(path):
        symbol = f"{coin.upper()}/USD"

        if i == 0:
            #first step: buy the starting coin with our usd
            order = api.submit_order(symbol=symbol, notional=round(usd, 2),
                                     side="buy", type="market", time_in_force="gtc")
            filled = wait_for_fill(api, order)
            held_coin = coin
            held_qty = float(filled.filled_qty)
            print(f"BUY  {symbol}: {held_qty} @ ${float(filled.filled_avg_price):.4f}")

        else:
            #sell what we're holding
            sell_symbol = f"{held_coin.upper()}/USD"
            try:
                pos = api.get_position(f"{held_coin.upper()}USD")
                sell_qty = float(pos.qty) - pre_existing.get(held_coin, 0.0)
            except Exception:
                sell_qty = held_qty
            if sell_qty <= 0:
                sell_qty = held_qty * 0.995

            order = api.submit_order(symbol=sell_symbol, qty=sell_qty,
                                     side="sell", type="market", time_in_force="gtc")
            filled = wait_for_fill(api, order)
            usd = float(filled.filled_qty) * float(filled.filled_avg_price)
            print(f"SELL {sell_symbol}: {filled.filled_qty} @ ${float(filled.filled_avg_price):.4f} = ${usd:.2f}")

            trade_log.append({"side": "sell", "symbol": sell_symbol, "qty": float(filled.filled_qty), "usd": usd})

            if i < len(path) - 1:
                #buy the next coin
                order = api.submit_order(symbol=symbol, notional=round(usd, 2),
                                         side="buy", type="market", time_in_force="gtc")
                filled = wait_for_fill(api, order)
                held_coin = coin
                held_qty = float(filled.filled_qty)
                print(f"BUY  {symbol}: {held_qty} @ ${float(filled.filled_avg_price):.4f}")

                trade_log.append({"side": "buy", "symbol": symbol, "qty": held_qty, "usd": usd})

    print(f"\nStarted: ${starting_usd:.2f}  Ended: ${usd:.2f}  P/L: ${usd - starting_usd:.2f}")
    return usd, trade_log


full_path = greatest_forward_path + greatest_reverse_path[1:]
print(f"Full cycle: {' -> '.join(full_path)}")

final_usd, trade_log = execute_trades(api, full_path, starting_usd=1000)


#save results.json
results = {
    "timestamp": datetime.now().isoformat(),
    "usd_prices": usd_prices,
    "greatest_factor": greatest_factor,
    "greatest_forward_path": greatest_forward_path,
    "greatest_reverse_path": greatest_reverse_path,
    "full_cycle_path": full_path,
    "smallest_factor": smallest_factor,
    "smallest_forward_path": smallest_forward_path,
    "smallest_reverse_path": smallest_reverse_path,
    "starting_usd": 1000,
    "final_usd": final_usd,
    "profit_loss": final_usd - 1000,
    "trades": trade_log,
}

results_path = "/home/ubuntu/data5500_mycode/Final_Project/results.json"
os.makedirs(os.path.dirname(results_path), exist_ok=True)

with open(results_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"Results saved to: {results_path}")