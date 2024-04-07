from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.indexes import SQLRecordManager, index
from langchain.indexes.base import RecordManager
from langchain.vectorstores.pgvector import PGVector


class DBEmbeddingManager:
    def __init__(
        self, connection_string, collection_name, embeddings=OpenAIEmbeddings()
    ):
        self.connection_string = connection_string
        self.collection_name = collection_name
        self.embeddings = embeddings
        self.record_manager = None
        self.pgvector_store = None
        self.retriever = None
        self.initialize()

    def initialize(self):
        self.record_manager = SQLRecordManager(
            namespace=f"pgvector/{self.collection_name}", db_url=self.connection_string
        )
        self.record_manager.create_schema()

        self.pgvector_store = PGVector(
            connection_string=self.connection_string,
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
        )
        self.retriever = self.pgvector_store.as_retriever()
