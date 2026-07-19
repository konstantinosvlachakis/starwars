import requests

BASE_URL = "https://swapi.dev/api/"

class SWAPIClient:
    def fetch_all(self,resource):
        url = BASE_URL + resource
        all_results = []
        
        while url:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            all_results.extend(data["results"])
            url = data["next"]
               
        return all_results