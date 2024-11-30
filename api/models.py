from django.db import models

class Animal(models.Model):
    """
    Model to store information about an animal, including its name and location.
    """
    name = models.CharField(max_length=10, help_text="Name of the animal")
    latitude = models.FloatField(help_text="Latitude of the animal's location")
    longitude = models.FloatField(help_text="Longitude of the animal's location")

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"
