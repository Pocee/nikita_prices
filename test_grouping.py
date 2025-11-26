from tarkov_client import TarkovClient

def group_bosses(boss_list):
    """Group bosses by name and combine their spawn locations"""
    grouped = {}
    for boss in boss_list:
        name = boss['name']
        if name not in grouped:
            grouped[name] = {
                'name': name,
                'spawnChance': boss['spawnChance'],
                'spawnLocations': []
            }
        # Add locations from this boss entry
        grouped[name]['spawnLocations'].extend(boss.get('spawnLocations', []))
    
    return list(grouped.values())

def test_grouping():
    client = TarkovClient()
    maps_data = client.get_maps_and_bosses()
    
    # Test Lighthouse (has multiple Rogue entries)
    for map_data in maps_data:
        if map_data['name'] == 'Lighthouse':
            print(f"Lighthouse - Before grouping: {len(map_data['bosses'])} boss entries")
            grouped = group_bosses(map_data['bosses'])
            print(f"Lighthouse - After grouping: {len(grouped)} unique bosses")
            
            for boss in grouped:
                print(f"\n{boss['name']}: {int(boss['spawnChance'] * 100)}%")
                print(f"  Locations: {len(boss['spawnLocations'])}")
                for loc in boss['spawnLocations'][:3]:  # Show first 3
                    print(f"    - {loc['name']}")
            break

if __name__ == "__main__":
    test_grouping()
