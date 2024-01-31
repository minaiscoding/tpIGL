from elasticsearch import Elasticsearch

# Define the Elasticsearch connection
es = Elasticsearch(
  "https://2b2811472db94c158c3aefb9da83eed0.us-central1.gcp.cloud.es.io:443",
  api_key="WVFFWFg0MEJ0SWNEVmxWd0Rab2E6NEZkbGpTb0lUdTJNY0w5aTdWOXpXUQ=="
)
# Dummy data
dummy_data = [
    {'Titre': 'Dummy Article 1', 'Resume': 'Lorem ipsum...', 'auteurs': 'John Doe', 'Institution': 'ABC University', 'date': '2023-01-01', 'MotsCles': 'Lorem, Ipsum', 'text': 'Full article text...', 'URL_Pdf': 'http://example.com/pdf1', 'RefBib': 'Bib123'},
    {'Titre': 'Dummy Article 2', 'Resume': 'Dolor sit amet...', 'auteurs': 'Jane Smith', 'Institution': 'XYZ College', 'date': '2023-01-02', 'MotsCles': 'Dolor, Sit', 'text': 'Another article text...', 'URL_Pdf': 'http://example.com/pdf2', 'RefBib': 'Bib456'},
    # Add more dummy articles
]

# Index dummy data
for data in dummy_data:
    # Specify the index and document type
    index_name = 'search-article'
   

    # Index the document
    es.index(index=index_name, body=data)

print("Successfully indexed dummy data.")
