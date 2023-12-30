from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from elasticsearch_dsl.connections import connections
from django.contrib.auth.models import User


connections.create_connection(hosts=['https://localhost:9200'], timeout=20)

class Utilisateurs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    NomUtilisateur = models.CharField(max_length=255, unique=True)
    Email = models.EmailField(unique=True)
    MotDePasse = models.CharField(max_length=255)
    Role = models.CharField(max_length=50)  # "admin," "moderator," "user"

    USERNAME_FIELD = 'NomUtilisateur'  # Set this to the field used for authentication

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password if it's a new instance
            self.MotDePasse = make_password(self.MotDePasse)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.NomUtilisateur


class Articles(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    Titre = models.CharField(max_length=255)
    Resume = models.TextField()
    auteurs = models.CharField(max_length=255)
    Institution = models.CharField(max_length=255)
    date = models.DateField()
    MotsCles = models.CharField(max_length=255)
    text = models.TextField()
    URL_Pdf = models.CharField(max_length=255)
    RefBib = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.Titre
    
    
class Favoris(models.Model):
    UtilisateurID = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    ArticleID = models.ForeignKey(Articles, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('UtilisateurID', 'ArticleID')

    def __str__(self):
        return f'{self.UtilisateurID.NomUtilisateur} - {self.ArticleID.Titre}'

