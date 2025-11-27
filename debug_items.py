"""Diagnostic to list all matches"""

from tarkov_client import TarkovClient
import json

client = TarkovClient()
# Try searching for just "M855" to see everything
ammo_name = "M80"

query = f"""
{{
    items(name: "{ammo_name}") {{
        name
        shortName
        buyFor {{
            source
            price
            vendor {{
                name
            }}
        }}
    }}
}}
"""

print("\nRunning diagnostic query...")
try:
    result = client.run_query(query)
    items = result.get('data', {}).get('items', [])
    print(f"Found {len(items)} items")
    for item in items:
        print(f"\nName: {item['name']}")
        print(f"ShortName: {item['shortName']}")
        traders = [x for x in item.get('buyFor', []) if x['source'] != 'fleaMarket']
        print(f"Trader Offers: {len(traders)}")
        if traders:
            print(f"First Trader: {traders[0]['vendor']['name']}")
            
except Exception as e:
    print(f"Error: {e}")
