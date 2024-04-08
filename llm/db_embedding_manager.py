from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.indexes import SQLRecordManager, index
from langchain.indexes.base import RecordManager
from langchain.vectorstores import VectorStore
from langchain.vectorstores.pgvector import PGVector
from langchain_core.vectorstores import VectorStoreRetriever


class DBEmbeddingManager:
    def __init__(
        self,
        connection_string: str,
        collection_name: str,
        embeddings=OpenAIEmbeddings(),
    ):
        self.connection_string: str = connection_string
        self.collection_name: str = collection_name
        self.embeddings = embeddings
        self.record_manager: SQLRecordManager | None = None
        self.vector_store: VectorStore | None = None
        self.retriever: VectorStoreRetriever | None = None
        self.initialize()

    def initialize(self):
        self.record_manager = SQLRecordManager(
            namespace=f"pgvector/{self.collection_name}", db_url=self.connection_string
        )
        self.record_manager.create_schema()

        self.vector_store = PGVector(
            connection_string=self.connection_string,
            embedding_function=self.embeddings,
            collection_name=self.collection_name,
        )
        self.retriever = self.vector_store.as_retriever()
