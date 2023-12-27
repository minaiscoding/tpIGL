from elasticsearch import Elasticsearch

# Define the Elasticsearch connection
es = Elasticsearch(['http://localhost:9200'],  verify_certs=False)

# Dummy data
dummy_data = [
    {'Titre': 'Dummy Article 1', 'Resume': 'Lorem ipsum...', 'auteurs': 'John Doe', 'Institution': 'ABC University', 'date': '2023-01-01', 'MotsCles': 'Lorem, Ipsum', 'text': 'Full article text...', 'URL_Pdf': 'http://example.com/pdf1', 'RefBib': 'Bib123'},
    {'Titre': 'Dummy Article 2', 'Resume': 'Dolor sit amet...', 'auteurs': 'Jane Smith', 'Institution': 'XYZ College', 'date': '2023-01-02', 'MotsCles': 'Dolor, Sit', 'text': 'Another article text...', 'URL_Pdf': 'http://example.com/pdf2', 'RefBib': 'Bib456'},
    # Add more dummy articles
]

# Index dummy data
for data in dummy_data:
    # Specify the index and document type
    index_name = 'articles'
   

    # Index the document
    es.index(index=index_name, body=data)

print("Successfully indexed dummy data.")
