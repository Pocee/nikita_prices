"""Test script for basic ammo trader info"""

from tarkov_client import TarkovClient
from ammo_helper import format_trader_info

client = TarkovClient()
# M855 is usually available at Peacekeeper LL1/LL2
ammo_name = "5.56x45mm M855" 

print(f"Querying API for: {ammo_name}")
items = client.get_ammo_market_data(ammo_name)

if items:
    item = items[0]
    buy_for = item.get('buyFor', [])
    
    print(f"\nRaw buyFor data count: {len(buy_for)}")
    
    traders = [x for x in buy_for if x['source'] != 'fleaMarket']
    for t in traders:
        vendor = t.get('vendor', {})
        print(f"\nTrader: {vendor.get('name')}")
        print(f"Level: {vendor.get('minTraderLevel')}")
        print(f"Price: {t.get('price')} {t.get('currency')}")
    
    print("\n" + "="*30)
    print("Formatted Output:")
    print("="*30)
    
    formatted = format_trader_info(buy_for)
    for line in formatted:
        print(line)
else:
    print("No items found")
