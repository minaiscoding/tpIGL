# admin.py
from django.contrib import admin
from .models import Articles, Utilisateurs, Favoris


admin.site.register(Articles)
admin.site.register(Utilisateurs)
admin.site.register(Favoris)
