from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from swapi.models import Character, Film, Starship
# Create your tests here.


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
        url = reverse("character-list")
        response = self.client.get(url)
        
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

        url = reverse("character-list")

        response = self.client.get(url, {"search": "Luke"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["name"],
            "Luke Skywalker",
        )   