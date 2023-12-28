from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

es = Elasticsearch
//(['http://localhost:9200/'],  verify_certs=False)
index_name = 'articles'

dummy_data = [
    {'Titre': 'Dummy Article 1', 'Resume': 'Lorem ipsum...', 'auteurs': 'John Doe', 'Institution': 'ABC University', 'date': '2023-01-01', 'MotsCles': 'Lorem, Ipsum', 'text': 'Full article text...', 'URL_Pdf': 'http://example.com/pdf1', 'RefBib': 'Bib123'},
    {'Titre': 'Dummy Article 2', 'Resume': 'Dolor sit amet...', 'auteurs': 'Jane Smith', 'Institution': 'XYZ College', 'date': '2023-01-02', 'MotsCles': 'Dolor, Sit', 'text': 'Another article text...', 'URL_Pdf': 'http://example.com/pdf2', 'RefBib': 'Bib456'},
    # Add more dummy articles
]



actions = [
    {
        '_op_type': 'index',
        '_index': index_name,
        '_source': data
    }
    for data in dummy_data
]

bulk(es, actions)