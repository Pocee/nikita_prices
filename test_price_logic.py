from tarkov_client import TarkovClient

def test_price_logic():
    client = TarkovClient()
    # Test with an item that has both flea and trader prices (e.g., "Salewa" or "M4A1")
    item_name = "M4A1"
    print(f"Fetching price for: {item_name}")
    
    items = client.get_item_price(item_name)
    
    if not items:
        print("No items found.")
        return

    for item in items[:1]:
        name = item.get('name', 'Unknown')
        sell_for = item.get('sellFor', [])
        
        print(f"\nItem: {name}")
        print(f"Total sell entries: {len(sell_for)}")
        
        # Logic from bot.py
        best_sell = max(sell_for, key=lambda x: x['price']) if sell_for else None
        best_sell_str = f"{best_sell['price']} ({best_sell['source']})" if best_sell else "N/A"
        
        trader_prices = [x for x in sell_for if x['source'] != 'fleaMarket']
        best_trader = max(trader_prices, key=lambda x: x['price']) if trader_prices else None
        best_trader_str = f"{best_trader['price']} ({best_trader['source']})" if best_trader else "N/A"
        
        print(f"Best Sell (Overall): {best_sell_str}")
        print(f"Best Trader: {best_trader_str}")

        # Verify logic
        if best_sell:
            print(f"  -> Source: {best_sell['source']}")
        if best_trader:
            print(f"  -> Source: {best_trader['source']}")
            assert best_trader['source'] != 'fleaMarket', "Best trader source should not be fleaMarket"

if __name__ == "__main__":
    test_price_logic()
