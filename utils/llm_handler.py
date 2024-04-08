from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables.base import RunnableSerializable
from typing import Any
from langchain.indexes import SQLRecordManager, index
from fastapi import Depends, Request
from langchain_core.vectorstores import VectorStore


class LLMDependancy:
    def __init__(self, request: Request):
        self.request = request

    def get_chain(self) -> RunnableSerializable[Any, str]:
        return self.request.app.state.model_chain.chain

    def get_retriever(self) -> VectorStoreRetriever:
        return self.request.app.state.db_embedding_manager.retriever

    def get_vectorstore(self) -> VectorStore:
        return self.request.app.state.db_embedding_manager.vector_store

    def get_record_manager(self) -> SQLRecordManager:
        return self.request.app.state.db_embedding_manager.record_manager


def get_llm_dependancy(request: Request) -> LLMDependancy:
    return LLMDependancy(request)
