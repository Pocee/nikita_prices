"""Debug search logic"""

from ammo_helper import find_ammo_stats
from ammo_data import AMMO_DATA

name = "PS"
name_lower = name.lower()

exact_name_matches = []
exact_word_matches = []

for key in AMMO_DATA:
    parts = key.split()
    if len(parts) > 1:
        ammo_name_only = ' '.join(parts[1:])
        
        # Check exact name start
        if ammo_name_only.lower().startswith(name_lower + ' ') or ammo_name_only.lower() == name_lower:
            exact_name_matches.append(key)
            print(f"EXACT NAME: {key} (ammo name: '{ammo_name_only}')")
        # Check exact word
        elif any(word.lower() == name_lower for word in ammo_name_only.split()):
            exact_word_matches.append(key)
            print(f"EXACT WORD: {key}")

print("\n" + "="*50)
print("EXACT NAME MATCHES (sorted by length):")
exact_name_matches.sort(key=len)
for m in exact_name_matches[:5]:
    print(f"  {m} (len={len(m)})")

print("\nEXACT WORD MATCHES (sorted by length):")
exact_word_matches.sort(key=len)
for m in exact_word_matches[:5]:
    print(f"  {m} (len={len(m)})")
