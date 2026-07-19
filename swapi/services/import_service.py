from swapi.models import Film, Character, Starship
from swapi.services.client import SWAPIClient

def extract_swapi_id(url):
    return int(url.rstrip("/").split("/")[-1])
    
def parse_integer(value):
    if not value or value == "unknown":
        return None
    clean_value = value.replace(",", "")
    return int(clean_value)
    
class ImportService:
    
    def __init__(self):
        self.client = SWAPIClient()
        
    def import_films(self):
        films = self.client.fetc_all("films/")
        
        for film in films:
            url = film["url"]
            film_obj, created = Film.objects.update_or_create(
                swapi_id = extract_swapi_id(url),
                defaults={
                    "title": film["title"],
                    "director": film["director"],
                    "producer": film["producer"],
                    "episode_id": film["episode_id"],
                    "opening_crawl": film["opening_crawl"],
                    "release_date": film["release_date"],
                },
            )
            
    
    def import_characters(self):
        characters = self.client.fetch_all("people/")
        
        for character in characters:
            url = character["url"]
            character_obj, created = Character.objects.update_or_create(
                swapi_id = extract_swapi_id(url),
                defaults={
                    "name": character["name"],
                    "height": parse_integer(character["height"]),
                    "mass": parse_integer(character["mass"]),
                    "hair_color": character["hair_color"],
                    "skin_color": character["skin_color"],
                    "eye_color": character["eye_color"],
                    "birth_year": character["birth_year"],
                    "gender": character["gender"],
                },
            )
            
            film_ids = [
                extract_swapi_id(film_url)
                for film_url in character["films"]
            ]
            
            films = Film.objects.filter(swapi_id__in=film_ids)
            
            character_obj.films.set(films)