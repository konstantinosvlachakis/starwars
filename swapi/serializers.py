from rest_framework import serializers

from swapi.models import Character, Film, Starship

class CharacterSerializer(serializers.ModelSerializer):
    
    
    class Meta:
            model = Character
            fields = "__all__"
    
    
    
class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = "__all__"
        

class ImportResourceSummarySerializer(serializers.Serializer):
    total = serializers.IntegerField()
    created = serializers.IntegerField()
    updated = serializers.IntegerField()


class ImportResultSerializer(serializers.Serializer):
    films = ImportResourceSummarySerializer()
    characters = ImportResourceSummarySerializer()
    starships = ImportResourceSummarySerializer()


class VoteResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()


class StarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Starship
        fields = "__all__"
