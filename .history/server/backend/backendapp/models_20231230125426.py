from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from elasticsearch_dsl.connections import connections


connections.create_connection(hosts=['https://localhost:9200'], timeout=20)

class Utilisateurs(models.Model):
    NomUtilisateur = models.CharField(max_length=255, unique=True)
    Email = models.EmailField(unique=True)
    MotDePasse = models.CharField(max_length=255)
    Role = models.CharField(max_length=50)  # "admin," "moderator," "user"

    def save(self, *args, **kwargs):
        # Hash the password before saving
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

    def __str__(self):
        return f'{self.UtilisateurID.NomUtilisateur} - {self.ArticleID.Titre}'

