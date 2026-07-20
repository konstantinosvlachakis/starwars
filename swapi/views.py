from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from swapi.services.import_service import ImportService
# Create your views here.


class SWAPIImportView(APIView):
    
    def post(self, request):
        service = ImportService()
        result = service.import_all()
        
        return Response(result, status=status.HTTP_200_OK)