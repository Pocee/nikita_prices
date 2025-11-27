"""Test improved ammo search logic"""

from ammo_helper import find_ammo_stats

# Test cases
test_searches = ["PS", "FMJ", "BP", "M855"]

for search in test_searches:
    print(f"\n{'='*50}")
    print(f"Searching for: '{search}'")
    print('='*50)
    
    matches = find_ammo_stats(search)
    
    if not matches:
        print("No matches found")
    elif len(matches) == 1:
        print(f"✅ Single match: {matches[0][0]}")
    else:
        print(f"Found {len(matches)} matches (showing first 10):")
        for i, (name, _) in enumerate(matches[:10], 1):
            print(f"  {i}. {name}")
        
        if len(matches) > 10:
            print(f"  ... and {len(matches)-10} more")

print("\n" + "="*50)
print("Testing complete!")
