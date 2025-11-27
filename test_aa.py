"""Test the !aa command functionality"""

from ammo_helper import get_ammo_by_caliber, format_ammo_compact, get_available_calibers

# Test 1: Get ammo by caliber
print("="*60)
print("TEST 1: Get ammo by caliber '5.45'")
print("="*60)

matches = get_ammo_by_caliber("5.45")
print(f"Found {len(matches)} ammo types\n")

for i, (name, stats) in enumerate(matches[:5], 1):
    print(f"{i}. {format_ammo_compact(name, stats)}")

print("\n" + "="*60)
print("TEST 2: Get ammo by caliber '7.62x39'")
print("="*60)

matches = get_ammo_by_caliber("7.62x39")
print(f"Found {len(matches)} ammo types\n")

for i, (name, stats) in enumerate(matches[:5], 1):
    print(f"{i}. {format_ammo_compact(name, stats)}")

print("\n" + "="*60)
print("TEST 3: Get available calibers")
print("="*60)

calibers = get_available_calibers()
print(f"Total calibers: {len(calibers)}\n")
print("First 10:")
for i, cal in enumerate(calibers[:10], 1):
    print(f"  {i}. {cal}")

print("\n" + "="*60)
print("✅ All tests completed!")
print("="*60)
