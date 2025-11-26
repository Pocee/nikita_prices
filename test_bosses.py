from tarkov_client import TarkovClient

def test_bosses():
    client = TarkovClient()
    print("Testing bosses query...")
    
    try:
        maps_data = client.get_maps_and_bosses()
        print(f"Found {len(maps_data)} maps")
        
        # Test finding a specific map
        for map_data in maps_data:
            if map_data['name'] == 'Customs':
                print(f"\nCustoms bosses:")
                for boss in map_data.get('bosses', []):
                    spawn_chance = int(boss['spawnChance'] * 100)
                    print(f"  - {boss['name']}: {spawn_chance}%")
                break
        
        # Test finding a boss
        print("\nSearching for 'Reshala':")
        for map_data in maps_data:
            for boss in map_data.get('bosses', []):
                if boss['name'].lower() == 'reshala':
                    print(f"  Found in {map_data['name']}: {int(boss['spawnChance'] * 100)}%")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_bosses()
