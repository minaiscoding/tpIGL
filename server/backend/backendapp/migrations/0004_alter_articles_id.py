# Generated by Django 5.0 on 2023-12-25 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendapp', '0003_alter_articles_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
