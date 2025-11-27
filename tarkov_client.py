import requests

class TarkovClient:
    def __init__(self):
        self.url = "https://api.tarkov.dev/graphql"
        self.headers = {"Content-Type": "application/json"}

    def run_query(self, query):
        response = requests.post(self.url, headers=self.headers, json={'query': query})
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

    def get_item_price(self, item_name):
        query = f"""
        {{
            itemsByName(name: "{item_name}") {{
                name
                shortName
                avg24hPrice
                basePrice
                changeLast48hPercent
                link
                sellFor {{
                    price
                    source
                }}
            }}
        }}
        """
        result = self.run_query(query)
        return result.get('data', {}).get('itemsByName', [])
    
    def get_maps_and_bosses(self):
        """Get all maps with their boss spawn information"""
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
        result = self.run_query(query)
        return result.get('data', {}).get('maps', [])
    
    def get_ammo_market_data(self, ammo_name):
        """Get market data for ammo including trader prices and levels"""
        query = f"""
        {{
            items(name: "{ammo_name}") {{
                name
                shortName
                avg24hPrice
                buyFor {{
                    price
                    currency
                    source
                    priceRUB
                    vendor {{
                        name
                        ... on TraderOffer {{
                            minTraderLevel
                            taskUnlock {{
                                name
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
        result = self.run_query(query)
        items = result.get('data', {}).get('items', [])
        
        if not items:
            return []
            
        # Filter out "pack" items unless specifically requested
        # and prioritize exact matches or base items
        filtered_items = [i for i in items if "pack" not in i['name'].lower()]
        
        if filtered_items:
            # Sort by name length (shortest is usually the base item)
            filtered_items.sort(key=lambda x: len(x['name']))
            return filtered_items
            
        return items

