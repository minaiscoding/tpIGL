# Generated by Django 4.2 on 2023-12-25 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0005_rename_id_articles_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articles',
            old_name='uuid',
            new_name='id',
        ),
    ]
