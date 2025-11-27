from tarkov_client import TarkovClient
import json

client = TarkovClient()
item_name = "Salewa First Aid Kit" # Salewa is craftable, but ammo might not be.
# Let's try to find an ammo that is craftable.
# "7.62x54mm R SNB" is often craftable.
# "9x19mm AP 6.3"
# "M61"

print(f"Testing client.get_ammo_market_data...")

# We need to use an ammo name that exists in the API
# The client method filters by "pack" and sorts by length.
# Let's try "AP 6.3"
ammo_name = "AP 6.3" 

print(f"Fetching data for: {ammo_name}")
try:
    items = client.get_ammo_market_data(ammo_name)
    if items:
        item = items[0]
        print(f"Found item: {item['name']}")
        print("Crafts:", json.dumps(item.get('craftsFor', []), indent=2))
    else:
        print("No items found.")

except Exception as e:
    print(f"Error: {e}")
