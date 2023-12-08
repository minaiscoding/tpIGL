from elasticsearch_dsl import Document, Text

class ArticleDocument(Document):
    titre = Text()
    resume = Text()
    auteurs = Text()
    institution = Text()
    mots_cles = Text()
    text = Text()

    class Index:
        name = 'articles'
