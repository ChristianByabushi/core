from django.db import models

# Create your models here.
class Logement(models.Model):
    adresse = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=[('salle', 'Salle'), ('appartement', 'Appartement'), ('maison', 'Maison'),('terrain', 'Terrain'),]) 
    surface =models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)

    @classmethod
    def total_logements(cls):
        return cls.objects.count() 
    