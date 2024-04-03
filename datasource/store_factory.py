from langchain_community.embeddings import OpenAIEmbeddings

from .pg_vector_store import AsnyPgVector, ExtendedPgVector
from langchain.indexes import SQLRecordManager


def get_vector_store(
    connection_string: str,
    embeddings: OpenAIEmbeddings,
    collection_name: str,
    mode: str = "sync",
):
    if mode == "sync":
        vector_store = ExtendedPgVector(
            connection_string=connection_string,
            embedding_function=embeddings,
            collection_name=collection_name,
        )
    elif mode == "async":
        vector_store = AsnyPgVector(
            connection_string=connection_string,
            embedding_function=embeddings,
            collection_name=collection_name,
        )
    else:
        raise ValueError("Invalid mode specified. Choose 'sync' or 'async'.")

    return vector_store
