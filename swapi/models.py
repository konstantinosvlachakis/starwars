from django.db import models

# Create your models here.

class Character(models.Model):
    swapi_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    height = models.PositiveIntegerField()
    mass = models.PositiveIntegerField()
    hair_color = models.CharField(max_length=255)
    skin_color = models.CharField(max_length=255)
    eye_color = models.CharField(max_length=255)
    birth_year = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    films = models.ManyToManyField(
        "Film",
        related_name="characters",
        blank=True
    )
    
    def __str__(self):
        return self.name
    

class Film(models.Model):
    swapi_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    producer = models.CharField(max_length=255)
    episode_id = models.PositiveIntegerField()
    opening_crawl = models.TextField()
    release_date = models.DateField()
   
    def __str__(self):
       return self.title
   

class Starship(models.Model):
    swapi_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    cost_in_credits = models.BigIntegerField(
        null=True,
        blank=True
    )
    length = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    manufacturer = models.CharField(max_length=255)
    crew = models.CharField(max_length=100)
    passengers = models.CharField(max_length=100)
    films = models.ManyToManyField(
        "Film",
        related_name="starships",
        blank=True
    )
    
    def __str__(self):
        return self.name