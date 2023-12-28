# Generated by Django 4.2 on 2023-12-27 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backendapp', '0010_customuser_alter_favoris_utilisateurid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NomUtilisateur', models.CharField(max_length=255, unique=True)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('MotDePasse', models.CharField(max_length=255)),
                ('Role', models.CharField(max_length=50)),
                ('user', models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='favoris',
            name='UtilisateurID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backendapp.utilisateurs'),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
