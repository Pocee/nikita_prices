from tarkov_client import TarkovClient

def test_maps_query():
    client = TarkovClient()
    
    # Test maps query
    query = """
    {
        maps {
            name
            normalizedName
            bosses {
                name
                normalizedName
                spawnChance
                spawnLocations {
                    name
                    chance
                }
            }
        }
    }
    """
    
    try:
        result = client.run_query(query)
        print("Maps query result:")
        import json
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_maps_query()
