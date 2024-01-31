# elasticsearch_setup.py
from elasticsearch_dsl import Document, Text, Date, connections

# Define the Elasticsearch connection
connections.create_connection(hosts=['https://2b2811472db94c158c3aefb9da83eed0.us-central1.gcp.cloud.es.io:443'], timeout=20)

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
