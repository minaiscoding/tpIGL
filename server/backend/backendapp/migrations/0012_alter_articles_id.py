# Generated by Django 4.1.7 on 2024-01-02 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0011_alter_articles_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
