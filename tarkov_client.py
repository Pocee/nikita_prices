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
