from tarkov_client import TarkovClient

def test_price_query():
    client = TarkovClient()
    item_name = "Salewa"
    print(f"Querying for item: {item_name}")
    
    try:
        results = client.get_item_price(item_name)
        if results:
            print(f"Found {len(results)} items.")
            for item in results:
                print(f"Name: {item.get('name')}")
                print(f"Price: {item.get('avg24hPrice')}")
                print("-" * 20)
        else:
            print("No items found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_price_query()
