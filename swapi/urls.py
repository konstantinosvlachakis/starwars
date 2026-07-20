from django.urls import path

from swapi.views import SWAPIImportView


urlpatterns = [
    path("import/", SWAPIImportView.as_view(), name="swapi-import"),
]