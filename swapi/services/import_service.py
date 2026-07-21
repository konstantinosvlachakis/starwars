from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError
from django.db import transaction

from swapi.models import Film, Character, Starship
from swapi.services.client import SWAPIClient, SWAPIResponseError

def extract_swapi_id(url):
    return int(url.rstrip("/").split("/")[-1])
    
def parse_integer(value):
    if not value or value == "unknown":
        return None
    try:
        clean_value = value.replace(",", "")
        return int(clean_value)
    except ValueError:
        return None
    
def parse_decimal(value):
    if not value or value == 'unknown':
        return None
    try:
        return Decimal(value.replace(',', ''))
    except InvalidOperation:
        return None


class ImportService:
    
    def __init__(self):
        self.client = SWAPIClient()
        
    def import_films(self):
        films = self.client.fetch_all("films/")

        created_count = 0
        updated_count = 0

        for film in films:

            _, created = Film.objects.update_or_create(
                swapi_id=extract_swapi_id(film["url"]),
                defaults={
                    "title": film["title"],
                    "director": film["director"],
                    "producer": film["producer"],
                    "episode_id": film["episode_id"],
                    "opening_crawl": film["opening_crawl"],
                    "release_date": film["release_date"],
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        return {
            "total": len(films),
            "created": created_count,
            "updated": updated_count,
        }
        
            
    
    def import_characters(self):
        characters = self.client.fetch_all("people/")
        
        created_count = 0
        updated_count = 0
        
        for character in characters:
            
            character_obj, created = Character.objects.update_or_create(
                swapi_id=extract_swapi_id(character["url"]),
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
            
            if created:
                created_count += 1
            else:
                updated_count += 1
            
        return {
            "total": len(characters),
            "created": created_count,
            "updated": updated_count,
        }
            
        
    def import_starships(self):
        starships = self.client.fetch_all("starships/")
        
        
        created_count = 0
        updated_count = 0
        
        for starship in starships:
            
            starship_obj, created = Starship.objects.update_or_create(
                swapi_id=extract_swapi_id(starship["url"]),
                defaults={
                    "name": starship["name"],
                    "model": starship["model"],
                    "cost_in_credits": parse_integer(starship["cost_in_credits"]),
                    "length": parse_decimal(starship["length"]),
                    "manufacturer": starship["manufacturer"],
                    "crew": starship["crew"],
                    "passengers": starship["passengers"],
                },
            )
            
            film_ids = [
                extract_swapi_id(film_url)
                for film_url in starship["films"]
            ]
            
            films = Film.objects.filter(swapi_id__in=film_ids)
            
            starship_obj.films.set(films)
            
            
            if created:
                created_count += 1
            else:
                updated_count += 1
            
        return {
            "total": len(starships),
            "created": created_count,
            "updated": updated_count,
        }
        
    @transaction.atomic       
    def import_all(self):
        try:
            films_result = self.import_films()
            characters_result = self.import_characters()
            starships_result = self.import_starships()
        except (KeyError, TypeError, ValueError, ValidationError) as exc:
            raise SWAPIResponseError(
                "SWAPI returned incomplete or invalid resource data."
            ) from exc

        return {
            "films": films_result,
            "characters": characters_result,
            "starships": starships_result,
        }
