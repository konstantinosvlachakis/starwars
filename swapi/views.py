from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from django.db.models import F
from swapi.services.import_service import ImportService
from .models import Character, Film, Starship
from .serializers import CharacterSerializer, FilmSerializer, StarshipSerializer
# Create your views here.


class SWAPIImportAPIView(APIView):
    
    def post(self, request):
        service = ImportService()
        result = service.import_all()
        
        return Response(result, status=status.HTTP_200_OK)
    
class CharacterListAPIView(ListAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer    
    filter_backends = [SearchFilter]
    search_fields = ["name"]
    

class FilmListAPIView(ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer    
    filter_backends = [SearchFilter]
    search_fields = ["title"]

    

class StarshipListAPIView(ListAPIView):
    queryset = Starship.objects.all()
    serializer_class = StarshipSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "model"]
    

class CharacterVoteAPIView(APIView):
    
    def post(self, request, character_id):
        try:
            character = Character.objects.get(id=character_id)
        except Character.DoesNotExist:
            return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)

        Character.objects.filter(id=character_id).update(votes=F("votes") + 1)

        return Response({"message": f"Vote registered for {character.name}."}, status=status.HTTP_200_OK)
    

class FilmVoteAPIView(APIView):
    
    def post(self, request, film_id):
        try:
            film = Film.objects.get(id=film_id)
        except Film.DoesNotExist:
            return Response({"error": "Film not found."}, status=status.HTTP_404_NOT_FOUND)

        Film.objects.filter(id=film_id).update(votes=F("votes") + 1)

        return Response({"message": f"Vote registered for {film.title}."}, status=status.HTTP_200_OK)
    
class StarshipVoteAPIView(APIView):
    
    def post(self, request, starship_id):
        try:
            starship = Starship.objects.get(id=starship_id)
        except Starship.DoesNotExist:
            return Response({"error": "Starship not found."}, status=status.HTTP_404_NOT_FOUND)

        Starship.objects.filter(id=starship_id).update(votes=F("votes") + 1)

        return Response({"message": f"Vote registered for {starship.name}."}, status=status.HTTP_200_OK)