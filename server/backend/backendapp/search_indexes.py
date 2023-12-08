from elasticsearch_dsl import Document, Text, Date, Keyword

class ArticleDocument(Document):
    Titre = Text()
    Resume = Text()
    auteurs = Text()
    Institution = Text()
    date = Date()
    MotsCles = Text()
    text = Text()
    URL_Pdf = Text()
    RefBib = Keyword()

    class Index:
        name = 'articles_index'
