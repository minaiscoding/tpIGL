from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Articles

@registry.register_document
class ArticleDocument(Document):
    
    
    class Index:
        name = 'articles'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Articles # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'Titre',
            'Resume',
            'auteurs',
            'Institution',
           
        ]

