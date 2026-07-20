from django.core.management.base import BaseCommand

from swapi.services.import_service import ImportService

class Command(BaseCommand):
    help = "Import films, characters and starships from SWAPI"
    
    def handle(self, *args, **options):
        service = ImportService()
        result = service.import_all()
        
        self.stdout.write(
            self.style.SUCCESS(f"SWAPI import completed: {result}")
        )
    