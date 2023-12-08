# backendapp/management/commands/populate_data.py

from django.core.management.base import BaseCommand
from backendapp.models import Articles

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        # Create a sample article
        article = Articles(
            Titre='Sample Article',
            Resume='This is the summary of the article',
            auteurs='Author',
            Institution='Institution',
            date='2023-01-01',
            MotsCles='Keyword1, Keyword2',
            text='Content of the article',
            URL_Pdf='http://example.com/article.pdf',
            RefBib='Bib'
        )
        article.save()

        # Display success message
        self.stdout.write(self.style.SUCCESS('Sample data has been successfully added to the database.'))
