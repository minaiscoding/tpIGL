from django.db import models
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from elasticsearch_dsl.connections import connections
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator




connections.create_connection(hosts=['https://localhost:9200'], timeout=20)

class Utilisateurs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
    NomUtilisateur = models.CharField(max_length=255, unique=True)
    Email = models.EmailField(unique=True)
    MotDePasse = models.CharField(max_length=255)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    ] #only accepts values from the specified choices
    Role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    favorite_articles = models.ManyToManyField('Favoris, related_name='favorited_by')
    

    USERNAME_FIELD = 'NomUtilisateur'  # Set this to the field used for authentication

    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password if it's a new instance
            self.MotDePasse = make_password(self.MotDePasse)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.NomUtilisateur

class Articles(models.Model): 
    id = models.CharField(max_length=255,primary_key=True)
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
    
class ArticleFile(models.Model): 
    id = models.AutoField(primary_key=True)
    URL_Pdf = models.URLField(max_length=255,null=True,blank=True)
    pdf_File = models.FileField(upload_to='article_pdfs/',null=True,blank=True,validators=[FileExtensionValidator( ['pdf'] )]) 

    def __str__(self):
        return self.pdf_File.name

class Favoris(models.Model):
    user = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    article_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.NomUtilisateur} - {self.article_id}"

