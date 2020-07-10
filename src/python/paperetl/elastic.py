"""
Elasticsearch module
"""

from elasticsearch import Elasticsearch, helpers

from .database import Database

class Elastic(Database):
    """
    Defines data structures and methods to store article content in Elasticsearch.
    """

    # Articles index
    ARTICLES = {
        "settings" : {
            "number_of_shards" : 5,
            "number_of_replicas" : 0,
            "index.mapping.nested_objects.limit": 30000
        },
        "mappings": {
            "properties" : {
                "sections" : {"type" : "nested"}
            }
        }
    }

    # Citations index
    CITATIONS = {
        "settings" : {
            "number_of_shards" : 5,
            "number_of_replicas" : 0,
        }
    }

    # Articles schema
    ARTICLE = ("id", "source", "published", "publication", "authors", "title", "tags", "design",
               "size", "sample", "method", "reference", "entry")

    # Sections schema
    SECTION = ("name", "text", "labels")

    # Citations schema
    CITATION = ("title", "mentions")

    def __init__(self, url):
        # Connect to ES instance
        self.connection = Elasticsearch(hosts=[url], timeout=60, retry_on_timeout=True)

        # Row count
        self.rows = 0

        # Buffered actions
        self.buffer = []

        # Create indices
        self.connection.indices.create("articles", Elastic.ARTICLES)
        self.connection.indices.create("citations", Elastic.CITATIONS)

    def save(self, uid, article, sections, tags, design):
        # Create article
        article = dict(zip(Elastic.ARTICLE, article))

        # Create sections
        sections = [dict(zip(Elastic.SECTION, section)) for section in sections]

        # Add sections to article
        article["sections"] = sections
 
        # Bulk action fields
        article["_id"] = article["id"]
        article["_index"] = "articles"

        # Buffer article
        self.buffer.append(article)

        # Increment number of articles processed
        self.rows += 1

        # Bulk load every 1000 records
        if self.rows % 1000 == 0:
            helpers.bulk(self.connection, self.buffer)
            self.buffer = []

            print("Inserted {} articles".format(self.rows), end="\r")

    def complete(self, citations):
        # Load remaining buffered articles
        if self.buffer:
            helpers.bulk(self.connection, self.buffer)

        # Citation rows
        self.buffer = []
        for citation in citations.items():
            # Build citation
            citation = dict(zip(Elastic.CITATION, citation))
            citation["_index"]  = "citations"

            # Buffer citation
            self.buffer.append(citation)

            # Bulk load every 5000 records
            if len(self.buffer) >= 5000:
                helpers.bulk(self.connection, self.buffer)
                self.buffer = []

        # Final citation batch
        if self.buffer:
            helpers.bulk(self.connection, self.buffer)

        print("Total articles inserted: {}".format(self.rows))

        # Refresh indices
        self.connection.indices.refresh(index="articles")
        self.connection.indices.refresh(index="citations")

    def close(self):
        self.connection.close()
