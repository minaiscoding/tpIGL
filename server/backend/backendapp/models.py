from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from elasticsearch_dsl.connections import connections
from django.core.validators import FileExtensionValidator




connections.create_connection(hosts=['https://localhost:9200'], timeout=20)

class Utilisateurs(models.Model):
    NomUtilisateur = models.CharField(max_length=255, unique=True)
    Email = models.EmailField(unique=True)
    MotDePasse = models.CharField(max_length=255)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    ] #only accepts values from the specified choices
    Role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    

    def save(self, *args, **kwargs):
        # Hash the password before saving
        self.MotDePasse = make_password(self.MotDePasse)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.NomUtilisateur

<<<<<<< HEAD
class Articles(models.Model): 
    Titre = models.CharField(max_length=255,null=True,blank=True)
    Resume = models.TextField(null=True,blank=True)
    auteurs = models.CharField(max_length=255,null=True,blank=True)
    Institution = models.CharField(max_length=255,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    MotsCles = models.CharField(max_length=255,null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    URL_Pdf = models.URLField(max_length=255,null=True,blank=True)
    RefBib = models.CharField(max_length=255,null=True,blank=True)
    pdf_File = models.FileField(upload_to='article_pdfs/',null=True,blank=True,validators=[FileExtensionValidator( ['pdf'] )]) 
=======
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
>>>>>>> 586a27361392aa78c31e9ca12016ed8150528803

    def __str__(self):
        return self.Titre 

class Favoris(models.Model):
    UtilisateurID = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    ArticleID = models.ForeignKey(Articles, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('UtilisateurID', 'ArticleID')

    def __str__(self):
        return f'{self.UtilisateurID.NomUtilisateur} - {self.ArticleID.Titre}'

