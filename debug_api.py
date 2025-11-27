"""Deep diagnostic for GraphQL query"""

from tarkov_client import TarkovClient
import json

client = TarkovClient()
ammo_name = "5.56x45mm M855"

print(f"Diagnosing API for: {ammo_name}")

# Query without inline fragments first to see what we get
query = f"""
{{
    items(name: "{ammo_name}") {{
        name
        buyFor {{
            price
            source
            vendor {{
                name
                normalizedName
            }}
        }}
    }}
}}
"""

print("\nRunning diagnostic query...")
try:
    result = client.run_query(query)
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"Error: {e}")
