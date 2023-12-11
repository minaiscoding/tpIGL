from django.db import models
from django.contrib.auth.hashers import make_password

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
    Titre = models.CharField(max_length=255)#null=False,blank=False
    Resume = models.TextField(null=True,blank=True)
    auteurs = models.CharField(max_length=255)#null=False,blank=False
    Institution = models.CharField(max_length=255)
    date = models.DateField()#null=False,blank=False
    MotsCles = models.CharField(max_length=255,null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    URL_Pdf = models.URLField(max_length=255,null=True,blank=True)
    RefBib = models.CharField(max_length=255,null=True,blank=True)
    pdf_File = models.FileField(upload_to='article_pdfs/',null=True)#null=False,blank=False

    def __str__(self):
        return self.Titre 

class Favoris(models.Model):
    UtilisateurID = models.ForeignKey(Utilisateurs, on_delete=models.CASCADE)
    ArticleID = models.ForeignKey(Articles, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('UtilisateurID', 'ArticleID')

    def __str__(self):
        return f'{self.UtilisateurID.NomUtilisateur} - {self.ArticleID.Titre}'
