from django.urls import path

from swapi.views import CharacterListAPIView, FilmListAPIView, FilmVoteAPIView, SWAPIImportAPIView, StarshipListAPIView, CharacterVoteAPIView, StarshipVoteAPIView


urlpatterns = [
    path("import/", SWAPIImportAPIView.as_view(), name="swapi-import"),
    path("characters/", CharacterListAPIView.as_view(), name="character-list"),
    path("films/", FilmListAPIView.as_view(), name="film-list"),
    path("starships/", StarshipListAPIView.as_view(), name="starship-list"),
    path("characters/<int:character_id>/vote/", CharacterVoteAPIView.as_view(), name="vote"),
    path("films/<int:film_id>/vote/", FilmVoteAPIView.as_view(), name="vote"),
    path("starships/<int:starship_id>/vote/", StarshipVoteAPIView.as_view(), name="vote"),
]