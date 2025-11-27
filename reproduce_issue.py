from tarkov_client import TarkovClient
import json

client = TarkovClient()
ammo_name = "M61"

print(f"Testing query for: {ammo_name}")

try:
    items = client.get_ammo_market_data(ammo_name)
    if items:
        item = items[0]
        print(f"Found item: {item['name']}")
        buy_for = item.get('buyFor', [])
        print(f"Buy offers: {len(buy_for)}")
        if not buy_for:
            print("Confirmed: No buy offers. This triggers the 'Not available for purchase' block.")
    else:
        print("No items found.")

except Exception as e:
    print(f"Error: {e}")
