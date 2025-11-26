"""Test script for ammo command functionality"""

from tarkov_client import TarkovClient
from ammo_helper import find_ammo_stats, format_armor_effectiveness, format_trader_info

# Test 1: Find ammo stats
print("=" * 50)
print("TEST 1: Finding ammo stats")
print("=" * 50)

test_ammos = ["M855A1", "bp", "m80", "RIP"]

for ammo in test_ammos:
    full_name, stats = find_ammo_stats(ammo)
    if stats:
        print(f"\n✅ Found: {full_name}")
        print(f"   Caliber: {stats['caliber']}")
        print(f"   Damage: {stats['damage']}, Pen: {stats['pen']}")
        print(f"   Armor Eff: {format_armor_effectiveness(stats['armor'])}")
    else:
        print(f"\n❌ Not found: {ammo}")

# Test 2: Get market data from API
print("\n" + "=" * 50)
print("TEST 2: Getting market data from API")
print("=" * 50)

client = TarkovClient()

test_api_ammos = ["5.56x45mm M855A1", "7.62x51mm M80"]

for ammo in test_api_ammos:
    print(f"\n🔍 Querying API for: {ammo}")
    try:
        items = client.get_ammo_market_data(ammo)
        if items:
            item = items[0]
            print(f"   ✅ Found: {item.get('name')}")
            print(f"   Avg 24h Price: {item.get('avg24hPrice', 'N/A')} ₽")
            
            buy_for = item.get('buyFor', [])
            if buy_for:
                print(f"   Purchase options: {len(buy_for)}")
                trader_info = format_trader_info(buy_for)
                for info in trader_info[:3]:
                    print(f"      {info}")
            else:
                print("   ❌ No purchase options")
        else:
            print(f"   ❌ No items found")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
print("✅ All tests completed!")
print("=" * 50)
