# elasticsearch_setup.py
from elasticsearch_dsl import Document, Text, Date, connections

# Define the Elasticsearch connection
connections.create_connection(hosts=['https://localhost:9200'], timeout=20)

# Define the Elasticsearch index and mapping
class ArticleIndex(Document):
    Titre = Text()
    Resume = Text()
    auteurs = Text()
    Institution = Text()
    date = Date()
    MotsCles = Text()
    text = Text()
    URL_Pdf = Text()
    RefBib = Text()

    class Index:
        name = 'articles'
