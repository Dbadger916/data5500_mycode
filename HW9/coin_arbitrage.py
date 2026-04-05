

import requests
import networkx as nx



API_KEY = "CG-jonPyb73MamvJyG56xufdHCQ"  

#coin name mapped to the ticker name 
COIN_IDS = {"bitcoin": "btc", "ethereum":"eth", "litecoin":"ltc", "ripple": "xrp", "cardano": "ada", "bitcoin-cash": "bch", "eos": "eos",}

#strings for the url so that it workds
IDS           = ",".join(COIN_IDS.keys())
VS_CURRENCIES = ",".join(COIN_IDS.values())

URL = (
    f"https://api.coingecko.com/api/v3/simple/price"
    f"?ids={IDS}"
    f"&vs_currencies={VS_CURRENCIES}"
    f"&x_cg_demo_api_key={API_KEY}"
)


#get that live data from coin gecko


response = requests.get(URL)
price_data = response.json()

#make the graph and print the exchange rates and make it a little pretty like the example output

edges = []

print(f"{'From':<6} {'To':<6} {'Rate':>16}")
print("-" * 30)

for coin_id, vs_prices in price_data.items():
    from_ticker = COIN_IDS[coin_id]
    for to_ticker, rate in vs_prices.items():
        if from_ticker == to_ticker:
            #if its weight is the same then it dont matter
            continue  
        print(f"{from_ticker:<6} {to_ticker:<6} {rate:>16.8f}")
        edges.append((from_ticker, to_ticker, rate))



g = nx.DiGraph()
g.add_weighted_edges_from(edges)

tickers = list(COIN_IDS.values())


#do that calculations theat it says it do

def path_weight(graph, path):
    """Return the product of all edge weights along a given path."""
    weight = 1.0
    for i in range(len(path) - 1):
        weight *= graph[path[i]][path[i + 1]]['weight']
    return weight


# Track global best and worst factor for all the different pairs and the likes
greatest_factor       = 0.0
greatest_forward_path = None
greatest_reverse_path = None

smallest_factor       = float('inf')
smallest_forward_path = None
smallest_reverse_path = None

# iterate over all of the pairs 
for src in tickers:
    for dst in tickers:
        if src == dst:
            continue

        # Find all simple paths in botht directions but dont repeat the nodes
        forward_paths = list(nx.all_simple_paths(g, src, dst))
        reverse_paths = list(nx.all_simple_paths(g, dst, src))

        if not forward_paths or not reverse_paths:
            continue

        print(f"paths from  {src} to {dst} ----------------------------------")

        # Compare every forward path with every reverse path
        for fwd_path in forward_paths:
            fwd_weight = path_weight(g, fwd_path)

            for rev_path in reverse_paths:
                rev_weight = path_weight(g, rev_path)


                factor = fwd_weight * rev_weight

                # Print the path pair and factor like the output example has in it you know
                print(f"{fwd_path} {fwd_weight}")
                print(f"{rev_path} {rev_weight}")
                print(factor)
                print()

                # Update greatest factor, the biggest one is the best 1
                if factor > greatest_factor:
                    greatest_factor       = factor
                    greatest_forward_path = fwd_path
                    greatest_reverse_path = rev_path

                # Update smallest factor the lowest one you know the least from 1
                if factor < smallest_factor:
                    smallest_factor       = factor
                    smallest_forward_path = fwd_path
                    smallest_reverse_path = rev_path

#report best and worst paths that are available out ther you know them

print("=" * 60)
print(f"Smallest Paths weight factor:  {smallest_factor}")
print(f"Paths:  {smallest_forward_path} {smallest_reverse_path}")
print()
print(f"Greatest Paths weight factor:  {greatest_factor}")
print(f"Paths:  {greatest_forward_path} {greatest_reverse_path}")
print("=" * 60) 