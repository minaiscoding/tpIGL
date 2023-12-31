from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from elasticsearch_dsl.connections import connections
from django.core.validators import FileExtensionValidator
import uuid



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

class Articles(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)# auto string generator for unique id of the articles better than char feild
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

    def __str__(self):
        return self.Titre 

class Favoris(models.Model):
    UtilisateurID = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    ArticleID = models.ForeignKey(Articles, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('UtilisateurID', 'ArticleID')

    def __str__(self):
        return f'{self.UtilisateurID.NomUtilisateur} - {self.ArticleID.Titre}'

