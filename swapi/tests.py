from unittest.mock import Mock, patch

import requests
from django.test import SimpleTestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from swapi.models import Character, Film, Starship

from swapi.services.client import (
    SWAPIClient,
    SWAPIRequestError,
    SWAPIResponseError,
)

class CharacterListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("character-list")
        self.character1 = Character.objects.create(
            swapi_id=1,
            name="Luke Skywalker",
            height=172,
            mass=77,
            hair_color="blond",
            skin_color="fair",
            eye_color="blue",
            birth_year="19BBY",
            gender="male"
        )
        
    
    def test_returns_characters(self):
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["name"], self.character1.name
        )
        
    def test_searches_characters_by_name(self):
        Character.objects.create(
            swapi_id=4,
            name="Darth Vader",
            height=202,
            mass=136,
            hair_color="none",
            skin_color="white",
            eye_color="yellow",
            birth_year="41.9BBY",
            gender="male",
        )

        

        response = self.client.get(self.url, {"search": "Luke"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["name"],
            "Luke Skywalker",
        )
        
        
    def test_character_pagination(self):
        for i in range(2, 12):
            Character.objects.create(
                swapi_id=i,
                name=f"Character {i}",
                height=180 + i,
                mass=70 + i,
                hair_color="brown",
                skin_color="light",
                eye_color="green",
                birth_year=f"{i}BBY",
                gender="male",
            )
            
        response = self.client.get(self.url, {"page": 2})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 11)
        self.assertEqual(len(response.data["results"]), 1)
        
        
        first_page_response = self.client.get(self.url, {"page": 1})
        self.assertEqual(len(first_page_response.data["results"]), 10)
        
        
    def test_character_search_with_no_matches_returns_empty_results(self):
        response = self.client.get(self.url, {"search": "Yoda"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])
        
        
        
class FilmListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("film-list")
        self.film1 = Film.objects.create(
            swapi_id=1,
            title="A New Hope",
            episode_id=4,
            opening_crawl="It is a period of civil war...",
            director="George Lucas",
            producer="Gary Kurtz, Rick McCallum",
            release_date="1977-05-25"
        )
        
    def test_returns_films(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["title"], self.film1.title
        )
        
    
    def test_searches_films_by_title(self):
        Film.objects.create(
            swapi_id=2,
            title="The Empire Strikes Back",
            episode_id=5,
            opening_crawl="It is a dark time for the Rebellion...",
            director="Irvin Kershner",
            producer="Gary Kurtz, Rick McCallum",
            release_date="1980-05-21"
        )
        
        response = self.client.get(self.url, {"search": "Empire"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["title"],
            "The Empire Strikes Back",
        )
        
    
    
    
    def test_film_pagination(self):
        for i in range(2, 12):
            Film.objects.create(
                swapi_id=i,
                title=f"Film {i}",
                episode_id=i,
                opening_crawl=f"Opening crawl for film {i}...",
                director="Director Name",
                producer="Producer Name",
                release_date="1980-01-01"
            )
            
        response = self.client.get(self.url, {"page": 2})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 11)
        self.assertEqual(len(response.data["results"]), 1)
        
        first_page_response = self.client.get(self.url, {"page": 1})
        self.assertEqual(len(first_page_response.data["results"]), 10)
        
    
    
class StarshipListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("starship-list")
        self.starship1 = Starship.objects.create(
            swapi_id=1,
            name="X-wing",
            model="T-65 X-wing",
            manufacturer="Incom Corporation",
            cost_in_credits=149999,
            length=12.5,
            crew=1,
            passengers=0,
        )
        
    def test_returns_starships(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["name"], self.starship1.name
        )
        
    def test_searches_starships_by_name(self):
        Starship.objects.create(
            swapi_id=2,
            name="TIE Fighter",
            model="Twin Ion Engine/Ln Starfighter",
            manufacturer="Sienar Fleet Systems",
            cost_in_credits=75000,
            length=6.3,
            crew=1,
            passengers=0,
        )
        
        response = self.client.get(self.url, {"search": "TIE"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["name"],
            "TIE Fighter",
        )
    
    def test_searches_starships_by_model(self):
        Starship.objects.create(
            swapi_id=3,
            name="Millennium Falcon",
            model="YT-1300 light freighter",
            manufacturer="Corellian Engineering Corporation",
            cost_in_credits=100000,
            length=34.37,
            crew=4,
            passengers=6,
        )
        
        response = self.client.get(self.url, {"search": "YT-1300"})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["model"],
            "YT-1300 light freighter",
        )
        
    
    def test_starship_pagination(self):
        
        for i in range(2, 12):
            Starship.objects.create(
                swapi_id=i,
                name=f"Starship {i}",
                model=f"Model {i}",
                manufacturer="Manufacturer Name",
                cost_in_credits=100000 + i * 1000,
                length=30 + i,
                crew=5 + i,
                passengers=10 + i,
            )
            
        response = self.client.get(self.url, {"page": 2})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 11)
        self.assertEqual(len(response.data["results"]), 1)
        
        first_page_response = self.client.get(self.url, {"page": 1})
        self.assertEqual(len(first_page_response.data["results"]), 10)
        



class VotingTestCase(APITestCase):
    def setUp(self):
        self.character = Character.objects.create(
            swapi_id=1,
            name="Luke Skywalker",
            height=172,
            mass=77,
            hair_color="blond",
            skin_color="fair",
            eye_color="blue",
            birth_year="19BBY",
            gender="male"
        )
        self.film = Film.objects.create(
            swapi_id=1,
            title="A New Hope",
            episode_id=4,
            opening_crawl="It is a period of civil war...",
            director="George Lucas",
            producer="Gary Kurtz, Rick McCallum",
            release_date="1977-05-25"
        )
        self.starship = Starship.objects.create(
            swapi_id=1,
            name="X-wing",
            model="T-65 X-wing",
            manufacturer="Incom Corporation",
            cost_in_credits=149999,
            length=12.5,
            crew=1,
            passengers=0,
        )
        
        
    def test_upvote_character(self):
        url = reverse("character-upvote", args=[self.character.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.character.refresh_from_db()
        self.assertEqual(self.character.votes, 1)
        
    
    def test_upvote_character_multiple_times(self):
        url = reverse("character-upvote", args=[self.character.id])
        
        # Upvote the character twice
        self.client.post(url)
        self.client.post(url)
        
        self.character.refresh_from_db()
        self.assertEqual(self.character.votes, 2)
    
    
    def test_upvote_nonexistent_character(self):
        url = reverse("character-upvote", args=[999])  # Non-existent character ID
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    def test_upvote_film(self):
        url = reverse("film-upvote", args=[self.film.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.film.refresh_from_db()
        self.assertEqual(self.film.votes, 1)
        
    
    def test_upvote_starship(self):
        url = reverse("starship-upvote", args=[self.starship.id])
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.starship.refresh_from_db()
        self.assertEqual(self.starship.votes, 1)
        
    def test_upvote_nonexistent_film(self):
        
        url = reverse("film-upvote", args=[999])  # Non-existent film ID
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_upvote_nonexistent_starship(self):
        url = reverse("starship-upvote", args=[999])  # Non-existent starship ID
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        
    
    
    
class SWAPIImportTestCase(APITestCase):
    @patch("swapi.views.ImportService.import_all")
    def test_swapi_import(self, mock_import_all):
        expected_result = {
            "films": {"total": 1, "created": 1, "updated": 0},
            "characters": {"total": 1, "created": 1, "updated": 0},
            "starships": {"total": 1, "created": 1, "updated": 0},
        }
        mock_import_all.return_value = expected_result

        url = reverse("swapi-import")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_result)
        mock_import_all.assert_called_once_with()

    @patch("swapi.services.import_service.SWAPIClient.fetch_all")
    def test_swapi_import_idempotency(self, mock_fetch_all):
        resources = {
            "films/": [
                {
                    "url": "https://swapi.dev/api/films/1/",
                    "title": "A New Hope",
                    "director": "George Lucas",
                    "producer": "Gary Kurtz",
                    "episode_id": 4,
                    "opening_crawl": "It is a period of civil war...",
                    "release_date": "1977-05-25",
                }
            ],
            "people/": [
                {
                    "url": "https://swapi.dev/api/people/1/",
                    "name": "Luke Skywalker",
                    "height": "172",
                    "mass": "77",
                    "hair_color": "blond",
                    "skin_color": "fair",
                    "eye_color": "blue",
                    "birth_year": "19BBY",
                    "gender": "male",
                    "films": ["https://swapi.dev/api/films/1/"],
                }
            ],
            "starships/": [
                {
                    "url": "https://swapi.dev/api/starships/1/",
                    "name": "X-wing",
                    "model": "T-65 X-wing",
                    "cost_in_credits": "149999",
                    "length": "12.5",
                    "manufacturer": "Incom Corporation",
                    "crew": "1",
                    "passengers": "0",
                    "films": ["https://swapi.dev/api/films/1/"],
                }
            ],
        }
        mock_fetch_all.side_effect = lambda resource: resources[resource]

        url = reverse("swapi-import")

        response1 = self.client.post(url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        counts_after_first_import = (
            Character.objects.count(),
            Film.objects.count(),
            Starship.objects.count(),
        )
        self.assertEqual(counts_after_first_import, (1, 1, 1))

        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        counts_after_second_import = (
            Character.objects.count(),
            Film.objects.count(),
            Starship.objects.count(),
        )

        self.assertEqual(counts_after_second_import, counts_after_first_import)
        self.assertEqual(response1.data["films"]["created"], 1)
        self.assertEqual(response2.data["films"]["created"], 0)
        self.assertEqual(response2.data["films"]["updated"], 1)
        mock_fetch_all.assert_any_call("films/")
        mock_fetch_all.assert_any_call("people/")
        mock_fetch_all.assert_any_call("starships/")
        self.assertEqual(mock_fetch_all.call_count, 6)
    
    
    @patch("swapi.views.ImportService.import_all")
    def test_swapi_import_returns_503_when_request_fails(self, mock_import_all):
        mock_import_all.side_effect = SWAPIRequestError(
            "Could not retrieve data from SWAPI."
        )

        url = reverse("swapi-import")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Could not retrieve data from SWAPI."
        )
        mock_import_all.assert_called_once_with()

    @patch("swapi.views.ImportService.import_all")
    def test_swapi_import_returns_502_when_response_invalid(self, mock_import_all):
        mock_import_all.side_effect = SWAPIResponseError(
            "SWAPI returned an invalid JSON response."
        )

        url = reverse("swapi-import")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_502_BAD_GATEWAY)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "SWAPI returned an invalid JSON response."
        )
        mock_import_all.assert_called_once_with()



class SWAPIClientTestCase(SimpleTestCase):

    @patch("swapi.services.client.requests.get")
    def test_fetch_all_raises_request_error_on_timeout(self, mock_get):
        mock_get.side_effect = requests.Timeout()

        client = SWAPIClient()

        with self.assertRaisesRegex(
            SWAPIRequestError,
            "timed out",
        ):
            client.fetch_all("people/")

        mock_get.assert_called_once_with(
            "https://swapi.dev/api/people/",
            timeout=10,
        )

    @patch("swapi.services.client.requests.get")
    def test_fetch_all_raises_request_error_on_http_failure(
        self,
        mock_get,
    ):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        mock_get.return_value = mock_response

        client = SWAPIClient()

        with self.assertRaisesRegex(
            SWAPIRequestError,
            "Could not retrieve data",
        ):
            client.fetch_all("people/")

        mock_response.raise_for_status.assert_called_once_with()

    @patch("swapi.services.client.requests.get")
    def test_fetch_all_raises_response_error_for_invalid_json(
        self,
        mock_get,
    ):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError(
            "Invalid JSON",
            "",
            0,
        )
        mock_get.return_value = mock_response

        client = SWAPIClient()

        with self.assertRaisesRegex(
            SWAPIResponseError,
            "invalid JSON",
        ):
            client.fetch_all("people/")

    @patch("swapi.services.client.requests.get")
    def test_fetch_all_raises_response_error_for_invalid_structure(
        self,
        mock_get,
    ):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "next": None,
        }
        mock_get.return_value = mock_response

        client = SWAPIClient()

        with self.assertRaisesRegex(
            SWAPIResponseError,
            "unexpected response format",
        ):
            client.fetch_all("people/")